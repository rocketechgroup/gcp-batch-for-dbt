# Package the DBT JOB

### Build

First, replace the properties of `project` and `impersonate_service_account` in dbt/profiles.yml with your own one, then
execute

```
export PROJECT_ID=<replace with your gcp project id>
docker build . -f ./Dockerfile -t eu.gcr.io/$PROJECT_ID/dbt-batch-demo:latest
```

### Tag

```
export VERSION=0.0.1
docker tag eu.gcr.io/$PROJECT_ID/dbt-batch-demo \
    eu.gcr.io/$PROJECT_ID/dbt-batch-demo:$VERSION
```

### Push to GCR

```
gcloud auth configure-docker
docker push eu.gcr.io/$PROJECT_ID/dbt-batch-demo:$VERSION
```