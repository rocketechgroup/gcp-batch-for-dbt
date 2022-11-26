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
    --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer"
    
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/batch.agentReporter"
    
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"
```

## Submit a job

> set PROJECT_ID as a environment variable first

```
pyhton submit_job.py
```

## Check status of the job

> set PROJECT_ID as a environment variable first

```
pyhton get_job.py
```

## Limitations & Gotchas

- The Batch job submission is very limited, only a [few regions](https://cloud.google.com/batch/docs/locations) are
  supported
- If you specify certain things wrong, such as the wrong machine type, it is very difficult to figure out what is wrong
  because nothing is in the logs
- When using custom service account, if lack of permission, instead of the job failing on 403, it hangs until timeout (
  about 30 minutes) with no logs. Make sure you
  read [prerequisites](https://cloud.google.com/batch/docs/get-started#project-prerequisites) fully, especially when
  it's related to permissions 

## Additional reading
- Many [Batch examples](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/6982717f255e87f3e2f1797ac3469f088b9b8693/batch) from Google 
- Batch docs, start [here](https://cloud.google.com/batch/docs/create-run-job#before-you-begin)