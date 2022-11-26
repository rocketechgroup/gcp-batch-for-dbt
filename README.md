# GCP Batch for DBT

## Create service account

```
export PROJECT_ID=rocketech-de-pgcp-sandbox
export SA_NAME=dbt-batch-demo
```

```
gcloud iam service-accounts create ${SA_NAME} \
    --description="DBT Batch Demo SA" \
    --display-name="${SA_NAME}"
```

The following roles are required to use this `custom service account` to create and run batch jobs
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/batch.jobsEditor"
    
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/batch.serviceAgent"
```

## Limitations & Gotchas

- The Batch job submission is very limited, only a [few regions](https://cloud.google.com/batch/docs/locations) are
  supported
- If you specify certain things wrong, such as the wrong machine type, it is very difficult to figure out what is wrong
  because nothing is in the logs
- When using custom service account, if lack of permission, instead of the job failing on 403, it hangs until timeout (
  about 30 minutes) with no logs. 