# GCP Batch for DBT
An example to run DBT jobs using the GCP Batch services. 

The purpose of this repo is to try out if Batch can be a drop-in replacement of the [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html) which requires k8 to run batch workload on Airflow.

The main reason for considering a drop-in replacement is that the effort to test K8 operator locally e2e is very high because it is not a GCP service, and from experience there isn't an easy solution to get around this.

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