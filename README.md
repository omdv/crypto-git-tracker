Full-stack website to track the development of open-sources cryptocurrencies, built with microservices.

## Stack

### Analytics backend
One container running Flask and two Celery periodic tasks for downloading github history for specified repositories and for running analytics, using pandas. Includes test coverage and Travis test definitions.

### Redis
Task broker support database

### PostgreSQL
Storage of git history and results of analysis

### Frontend
ReactJS application with d3js interactive graphics, running behind nginx in the same container

### nginx
Nginx as a gateway to the whole cluster


## Development
The whole stack may be run locally using `docker-compose-dev`

## Production
The whole stack may be deployed on the single instance using `docker-compose-prod` or on multiple instances using docker swarm. The deploy-swarm.sh script is to automate deployment to DigitalOcean cluster.