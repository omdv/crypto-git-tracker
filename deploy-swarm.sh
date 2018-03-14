#!/bin/bash

# set up number of nodes
num_nodes=2

# create nodes
for i in `seq 1 $num_nodes`; do docker-machine create --driver digitalocean \
  --digitalocean-image ubuntu-16-04-x64 \
  --digitalocean-access-token $DOTOKEN node-$i; done

# update firewall
for i in `seq 1 $num_nodes`; do 
    if [ "$i" == "1" ]; then docker-machine ssh node-$i ufw allow 2377/tcp; fi
    docker-machine ssh node-$i 'ufw allow 22/tcp
                                ufw allow 2376/tcp
                                ufw allow 7946/tcp
                                ufw allow 7946/tcp
                                ufw allow 7946/udp
                                ufw allow 4789/udp
                                ufw reload
                                ufw --force enable'
    docker-machine ssh node-$i systemctl restart docker
done

# update system
for i in `seq 1 $num_nodes`; do
    docker-machine ssh node-$i 'apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && reboot'
done

# install monitoring
for i in `seq 1 $num_nodes`; do
    docker-machine ssh node-$i 'curl -sSL https://agent.digitalocean.com/install.sh | sh'
done

# create swarm
for i in `seq 1 $num_nodes`; do
    if [ "$i" == "1" ]; then
        manager_ip=$(docker-machine ip node-$i)
        eval $(docker-machine env node-$i) && \
          docker swarm init --advertise-addr "$manager_ip"
        worker_token=$(docker swarm join-token worker -q)
    else
        eval $(docker-machine env node-$i) && \
          docker swarm join --token "$worker_token" "$manager_ip:2377"
    fi
done

# create registry
# docker-machine ssh node-1 'docker service create --name registry --publish published=5000,target=5000 registry:2'

# push built images to docker HUB
for i in `docker images | grep '^omdv/crypto'| awk '{print $1}'`; do
    docker push $i
done

# switch to node-1 and deploy
eval $(docker-machine env node-1) && \
export REACT_APP_GIT_SERVICE_URL=$(docker-machine ip node-1) && \
docker stack deploy -c docker-compose-deploy.yml cryptosite

# initiate a db
#docker-machine ssh node-1 "docker exec -it $(docker ps -a | grep 'analytics' | head -n1 | awk '{print $NF}') python manage.py recreate_db
#                           docker exec -it $(docker ps -a | grep 'analytics' | head -n1 | awk '{print $NF}') python manage.py add_repos -f coins_list_full"


# kill all nodes
# for i in `seq 1 $num_nodes`; do
#     docker-machine rm node-$i
# done
