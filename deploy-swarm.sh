#!/bin/bash

# set up number of nodes
num_nodes=4

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