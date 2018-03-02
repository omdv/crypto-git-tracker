#!/bin/bash

# set up number of nodes
node=cryptosite-db-ocean

# create node
docker-machine create --driver digitalocean \
  --digitalocean-image ubuntu-16-04-x64 \
  --digitalocean-access-token $DOTOKEN $node

# update firewall
docker-machine ssh $node 'ufw allow 22/tcp
                          ufw allow 2376/tcp
                          ufw allow 5432/tcp
                          ufw reload
                          ufw --force enable'
docker-machine ssh $node systemctl restart docker

# update system
docker-machine ssh $node 'apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && reboot'

# install monitoring
docker-machine ssh $node 'curl -sSL https://agent.digitalocean.com/install.sh | sh'

# deploy image
eval $(docker-machine env $node)
docker build -t omdv/$node .
docker run --name $node -p 5432:5432 -d \
 -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
 -e POSTGRES_USER=$POSTGRES_USER \
 -e POSTGRES_DB=analytics omdv/$node