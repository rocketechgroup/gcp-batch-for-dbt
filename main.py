import os
import uuid

from google.cloud import batch_v1


def create_container_job(
        project_id: str,
        batch_region: str,
        job_region: str,
        machine_type: str,
        network: str,
        subnet: str,
        service_account_email: str,
        job_name: str,
        container_image: str,
        container_entrypoint: str,
        container_commands: str
) -> batch_v1.Job:
    client = batch_v1.BatchServiceClient()

    # Define what will be done as part of the job.
    runnable = batch_v1.Runnable()
    runnable.container = batch_v1.Runnable.Container()
    runnable.container.image_uri = container_image
    runnable.container.entrypoint = container_entrypoint
    runnable.container.commands = container_commands

    # Jobs can be divided into tasks. In this case, we have only one task.
    task = batch_v1.TaskSpec()
    task.runnables = [runnable]

    # We can specify what resources are requested by each task.
    resources = batch_v1.ComputeResource()
    resources.cpu_milli = 1000  # in milliseconds per cpu-second. This means the task requires 1 cpu core
    resources.memory_mib = 512  # in MiB
    task.compute_resource = resources

    task.max_retry_count = 2
    task.max_run_duration = "3600s"

    # Tasks are grouped inside a job using TaskGroups.
    # Currently, it's possible to have only one task group.
    group = batch_v1.TaskGroup()
    group.task_count = 1
    group.task_spec = task

    # Policies are used to define on what kind of virtual machines the tasks will run on.
    # In this case, we tell the system to use "e2-standard-4" machine type.
    # Read more about machine types here: https://cloud.google.com/compute/docs/machine-types
    policy = batch_v1.AllocationPolicy.InstancePolicy()
    policy.machine_type = machine_type
    instances = batch_v1.AllocationPolicy.InstancePolicyOrTemplate()
    instances.policy = policy

    location_policy = batch_v1.AllocationPolicy.LocationPolicy()
    location_policy.allowed_locations = [f"regions/{job_region}"]

    network_interface = batch_v1.AllocationPolicy.NetworkInterface()
    network_interface.network = network
    network_interface.subnetwork = subnet
    network_interface.no_external_ip_address = True

    network_policy = batch_v1.AllocationPolicy.NetworkPolicy()
    network_policy.network_interfaces = [network_interface]

    service_account = batch_v1.types.ServiceAccount()
    service_account.email = service_account_email

    allocation_policy = batch_v1.AllocationPolicy()
    allocation_policy.instances = [instances]
    allocation_policy.location = location_policy
    allocation_policy.network = network_policy
    allocation_policy.service_account = service_account

    job = batch_v1.Job()
    job.task_groups = [group]
    job.allocation_policy = allocation_policy
    job.labels = {"env": "testing", "type": "container"}
    # We use Cloud Logging as it's an out of the box available option
    job.logs_policy = batch_v1.LogsPolicy()
    job.logs_policy.destination = batch_v1.LogsPolicy.Destination.CLOUD_LOGGING

    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{batch_region}"

    return client.create_job(create_request)


if __name__ == '__main__':
    project_id = os.environ.get('PROJECT_ID')
    job = create_container_job(
        project_id=project_id,
        batch_region='europe-north1',  # this is just the region used to submit the job
        job_region='europe-west2',
        machine_type="e2-standard-2",
        network="global/networks/private",
        subnet="regions/europe-west2/subnetworks/private-1",
        service_account_email=f"dbt-batch-demo@{project_id}.iam.gserviceaccount.com",
        job_name='dbt-batch-demo-' + uuid.uuid4().hex,
        container_image=f"eu.gcr.io/{project_id}/dbt-batch-demo:0.0.1",
        container_entrypoint="/bin/bash",
        container_commands=["-cx", "dbt run --project-dir dbt_batch_demo"]
    )
