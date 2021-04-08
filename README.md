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

Une seule image est utilisée : dossier ETL
Pour builder l'image :
```bash
docker-compose -f docker-compose-etl.yml --env-file ./.env up --build --no-deps
```

Adresse ETL : http://localhost:81/docs
Adresse GreatExpectation : http://localhost:81/great-expectations

Le pipeline s'étend sur 3 niveaux de raffinage de données :
- raw : données brutes récupérées de différentes API
- curated : les données sont préparées par des traitements spécifiques
- refined : les données sont mergées et validées

### Les endpoints
#### GET /retrieve-raw-weather-data
Recupère les données brutes de Météo France
ex : http://localhost:81/retrieve-raw-weather-data?year=2020&start_month=1&end_month=6&dataset_name=2020_01_06

#### GET /retrieve-raw-rte-data
Recupère les données brutes de RTE
ex : http://localhost:81/retrieve-raw-rte-data?year=2020&start_month=1&end_month=6&dataset_name=2020_01_06

#### GET /prepare-raw-weather-data
Prépare les données Météo France
ex : http://localhost:81/prepare-raw-weather-data?dataset_name=2020_01_06

#### GET /prepare-raw-rte-data
Prépare les données RTE
ex : http://localhost:81/prepare-raw-rte-data?dataset_name=2020_01_06

#### GET /merge-curated-data
Merge nos différentes données pré-traitées
ex : http://localhost:81/merge-curated-data?dataset_name=2020_01_06

#### GET /validate-refined-data
Etape de validation des données
ex : http://localhost:81/validate-refined-data?dataset_name=2020_01_06


## MLOps

On rajoute plusieurs images : S3 (MinIO pour simuler un S3), DB (mysql), MLflow, training_api, serving_api, load_testing_service (locust)
Pour builder et lancer les containers :
```bash
docker-compose -f docker-compose-training.yml --env-file ./.env up --build --no-deps
```
en rajoutant la partie prédiction :
```bash
docker-compose -f docker-compose-predict.yml --env-file ./.env up --build --no-deps
```

Les urls
- MinIO : http://0.0.0.0:9000/
- MLflow : http://0.0.0.0:5000
- Training_api : http://0.0.0.0:8000/docs
- Serving_api : http://0.0.0.0:8001/docs
- locust : http://0.0.0.0:8089

## Monitoring

On rajoute 3 images pour pouvoir faire le monitoring : Prometheus, Grafana, data_drift_detector
Pour builder et lancer les containers :
```bash
docker-compose -f docker-compose-monitoring_1.yml --env-file ./.env up --build --no-deps
```
en rajoutant la partie data_drift_detector :
```bash
docker-compose -f docker-compose-monitoring_2.yml --env-file ./.env up --build --no-deps

Les urls
- Prometheus : http://0.0.0.0:9090/
- Grafana : http://0.0.0.0:3000/
- data_drift_detector : http://0.0.0.0:82/
