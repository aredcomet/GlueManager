from uuid import uuid4
from django.db import models


class GlueConfig(models.Model):
    profile = models.CharField(max_length=254, default='default')
    max_dpu_standard = models.IntegerField(default=300)
    max_concurrent_jobs = models.IntegerField(default=50, help_text='No of concurrant job runs.')
    cool_off_time = models.IntegerField(default=600, help_text='Wait time to resume launching glue jobs after hitting hot launch limit')
    hot_launch_limit = models.IntegerField(default=10, help_text='Number of glue jobs that can be launched within cool off time.')
    job_status_check_interval = models.IntegerField(default=60, help_text='Seconds')

    def __str__(self):
        return f'{self.profile}'

class GlueJob(models.Model):
    GLUE_WORKER_TYPE = (
        (0, 'Standard'),
        (1, 'G1.X'),
        (2, 'G2.X'))

    GLUE_JOB_STATUS = (
        (0, 'QUE'),
        (1, 'STARTING'),
        (2, 'RUNNING'),
        (3, 'TIMEOUT'),
        (4, 'FAILED'),
        (5, 'STOPPED'),
        (6, 'STOPPING'),
        (7, 'SUCCEEDED'))

    job_uuid = models.UUIDField(default=uuid4(), primary_key=True)
    group_name = models.CharField(max_length=254, default='UNNAMED')
    job_name = models.CharField(max_length=254)
    requested_ts = models.DateTimeField(auto_now_add=True)
    modified_ts = models.DateTimeField(auto_now=True)
    job_run_id = models.CharField(max_length=25, null=True, blank=True)
    worker_type = models.IntegerField(choices=GLUE_WORKER_TYPE, default=0)
    dpu = models.IntegerField(default=2)
    status = models.IntegerField(choices=GLUE_JOB_STATUS)
    trial_no = models.IntegerField(default=1)
    preceding = models.ForeignKey('self', on_delete=models.CASCADE, related_name='preceding_job')
    succeeding = models.ForeignKey('self', on_delete=models.CASCADE, related_name='succeeding_job')
    message = models.TextField(max_length=1024)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.job_name}::{self.job_uuid}'


class GlueArguments(models.Model):
    glue_job = models.ForeignKey('GlueJob', on_delete=models.CASCADE)
    key = models.CharField(max_length=25),
    value = models.CharField(max_length=254)

    def __str__(self):
        return f'{self.key}::{self.value}'
