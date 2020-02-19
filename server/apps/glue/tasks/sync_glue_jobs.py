import boto3

from django.conf import settings
from django.db.models import Sum

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from apps.account.models import Account

from apps.glue.models import (
    GlueJob,
    GlueJobRun,
    RunStateEnum

)


WORKING_GLUE_STATES = [
    RunStateEnum.STARTING.value,
    RunStateEnum.RUNNING.value,
    RunStateEnum.STOPPING.value,
]


@db_task()
def sync_glue_jobs():
    accounts = Account.objects.all()
    for account in accounts:
        client = boto3.client("glue", account.aws_region)

        response = client.get_jobs()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            print(f"Failed getting jobs for {account.name}")
            continue

        glue_jobs = response['Jobs']

        for job in glue_jobs:
            glue_job, created = GlueJob.objects.update_or_create(
                name=job.get('Name'),
                defaults={
                    "account": account,
                    "role": job.get('Role'),
                    "created_on": job.get('CreatedOn'),
                    "last_modified_on": job.get('LastModifiedOn'),
                    "execution_property": job.get('ExecutionProperty'),
                    "command": job.get('Command'),
                    "default_arguments": job.get('DefaultArguments'),
                    "max_retries": job.get('MaxRetries'),
                    "allocated_capacity": job.get('AllocatedCapacity'),
                    "timeout": job.get('Timeout'),
                    "max_capacity": job.get('MaxCapacity'),
                    "glue_version": job.get('GlueVersion'),
                }
            )


@db_task()
def sync_glue_job_runs():
    accounts = Account.objects.all()

    for account in accounts:
        client = boto3.client("glue", account.aws_region)

        glue_jobs = account.gluejob_set.all()

        for glue_job in glue_jobs:
            data = list()
            get_job_runs(client, glue_job.name, data, next_token='')

            for each_run in data:
                job_run, created = GlueJobRun.objects.update_or_create(
                    run_id=each_run.get('Id'),
                    defaults={
                        "job": glue_job,
                        "attempt": each_run.get('Attempt'),
                        "started_on": each_run.get('StartedOn'),
                        "last_modified_on": each_run.get('LastModifiedOn'),
                        "completed_on": each_run.get('CompletedOn'),
                        "state": each_run.get('JobRunState'),
                        "arguments": each_run.get('Arguments'),
                        "error_message": each_run.get('ErrorMessage', ''),
                        "predecessor_runs": each_run.get('PredecessorRuns'),
                        "allocated_capacity": each_run.get('AllocatedCapacity'),
                        "execution_time": each_run.get('ExecutionTime'),
                        "timeout": each_run.get('Timeout'),
                        "max_capacity": each_run.get('MaxCapacity'),
                        "worker_type": each_run.get('WorkerType'),
                        "number_of_workers": each_run.get('NumberOfWorkers'),
                        "log_group_name": each_run.get('LogGroupName'),
                    }
                )


@db_task()
def process_queued_runs():
    accounts = Account.objects.all()

    for account in accounts:
        config = account.config
        max_dpu = config.get('max_dpu')
        max_concurrent_job_runs = config.get('max_concurrent_job_runs')

        runs = GlueJobRun.objects.filter(state__in=WORKING_GLUE_STATES, job__account=account)

        current_running_jobs = runs.count()

        if current_running_jobs >= max_concurrent_job_runs:
            print(f"Reached Max Concurrent Jobs of {max_concurrent_job_runs}")
            continue

        current_dpu_utilization = runs.aggregate(dpu_sum=Sum('max_capacity')).get('dpu_sum')

        current_dpu_utilization = current_dpu_utilization if current_dpu_utilization is not None else 0

        if current_dpu_utilization >= max_dpu:
            print(f"Reached Max DPU  {max_dpu}")
            continue

        available_dpu = max_dpu - current_dpu_utilization
        available_run_slots = max_concurrent_job_runs - current_running_jobs

        # Can still allocate jobs and still have some DPU's left to use, get jobs in queue that can be accomodated
        queued_runs = GlueJobRun.objects.filter(state=RunStateEnum.QUEUED.value, max_capacity__lte=available_dpu).select_related('job').order_by('received_on')[:available_run_slots]

        glue_client = boto3.client("glue", account.aws_region)
        for run in queued_runs:
            if available_dpu < run.max_capacity:
                break
            response = glue_client.start_job_run(
                JobName=run.job.name,
                Arguments=run.arguments,
                Timeout=run.timeout,
                MaxCapacity=run.max_capacity,
            )

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                print(f"Couldn't create job for {run.id}")
                continue

            run.run_id = response['JobRunId']
            run.state = RunStateEnum.STARTING.value
            run.save()
            available_dpu = available_dpu - run.max_capacity


def get_job_runs(client, job_name, data, next_token=None):
    if next_token is None:
        return

    response = client.get_job_runs(JobName=job_name, MaxResults=200, NextToken=next_token)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        return

    data.extend(response['JobRuns'])

    get_job_runs(client, job_name, data, next_token=response.get('NextToken', None))


@db_periodic_task(crontab(minute='*/1'))
def master_job():
    sync_glue_jobs_task = sync_glue_jobs.s()

    pipeline = (sync_glue_jobs_task.then(sync_glue_job_runs).then(process_queued_runs))

    settings.HUEY.enqueue(pipeline)
