Full-stack website to track the development of open-sources cryptocurrencies, built with microservices. The primary goal is to experiment with various architectures, orchestration tools and different cloud environments.

## Stack

### Analytics backend
One container running Flask and two Celery periodic tasks for downloading github history for specified repositories and for running analytics, using pandas. Includes test coverage and Travis test definitions.

### Redis
Database to support the Celery task broker. Does not require persistent storage.

### PostgreSQL
Storage of git history and results of analysis. Requires a persistent volume container. Kubernetes implementation supports a mini cluster to ensure high availability.

### Frontend
ReactJS application with d3js interactive graphics, running behind nginx in the same container.

### nginx
Nginx as a gateway to the whole cluster, as APIs are exposed by analytics backend.


## Development

### Docker
Run locally using `docker-compose-dev.yaml` configuration

### Kubernetes
Run locally on minikube using `k8-dev.yaml` configuration or using `helm` and helm chart in `helm-chart` folder

## Production
The whole stack may be deployed on the single instance using `docker-compose-prod` or on multiple instances using docker swarm. The `deploy-swarm.sh` script is to automate deployment to DigitalOcean cluster.