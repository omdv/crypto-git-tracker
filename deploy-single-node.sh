#!/bin/bash

node_name=cryptosite

# create node
docker-machine create --driver digitalocean \
--digitalocean-image ubuntu-16-04-x64 \
--digitalocean-size 2gb \
--digitalocean-access-token $DOTOKEN $node_name

# update firewall
docker-machine ssh $node_name 'ufw allow 22/tcp
							   ufw allow 80/tcp
                               ufw allow 2377/tcp
                               ufw allow 2376/tcp
                               ufw allow 7946/tcp
                               ufw allow 7946/tcp
                               ufw allow 7946/udp
                               ufw allow 4789/udp
                               ufw reload
                               ufw --force enable'
docker-machine ssh $node_name systemctl restart docker

# update system
docker-machine ssh $node_name 'apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && reboot'

# install monitoring
docker-machine ssh $node_name 'curl -sSL https://agent.digitalocean.com/install.sh | sh'

# push built images to docker HUB
for i in `docker images | grep '^omdv/crypto'| awk '{print $1}'`; do
    docker push $i
done

# switch to node and deploy
eval $(docker-machine env $node_name) && \
export REACT_APP_GIT_SERVICE_URL=$(docker-machine ip $node_name) &&\
docker-compose -f docker-compose-prod-node.yml up -d --build

# initiate a db
#docker-machine ssh node-1 "docker exec -it $(docker ps -a | grep 'analytics' | head -n1 | awk '{print $NF}') python manage.py recreate_db
#                           docker exec -it $(docker ps -a | grep 'analytics' | head -n1 | awk '{print $NF}') python manage.py add_repos -f coins_list_full"


# kill all nodes
# for i in `seq 1 $num_nodes`; do
#     docker-machine rm node_name
# done
