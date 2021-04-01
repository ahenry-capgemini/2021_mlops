# MLOps connecting the dots

Le TP sera décomposer en 3 parties : 
- DataOps avec la mise en place d'une ETL
- MLOps avec la mise en place d'un pipeline d'entrainement et d'un service d'inference
- Monitoring avec la mise en place de brique pour compléter le monitoring de l'application

## Pré-requis
- Docker installé et les notions de base (build, run et volume)
- Quelques notions de docker-compose : [lien documentation](https://docs.docker.com/compose/gettingstarted/)
- Jupyter notebook installé

Quelques commandes docker utiles :
- docker container stop $(docker container ls –aq)
- docker container rm $(docker container ls –aq)
- docker volume prune –f
- docker-compose -f docker-compose-etl.yml --env-file ./.env up --build --no-deps
- docker-compose up --force-recreate --no-deps _service-name_

## DataOps

## MLOps

## Monitoring
