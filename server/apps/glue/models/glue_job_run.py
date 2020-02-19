import uuid

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField, ArrayField

from .enum import RunStateEnum, WorkerTypeEnum


class GlueJobRun(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    run_id = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
    )

    job = models.ForeignKey(
        'GlueJob',
        on_delete=models.CASCADE,
    )

    attempt = models.IntegerField(
        blank=True,
        null=True,
    )

    received_on = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )

    started_on = models.DateTimeField(
        blank=True,
        null=True,
    )

    last_modified_on = models.DateTimeField(
        blank=True,
        null=True,
    )

    completed_on = models.DateTimeField(
        null=True,
        blank=True,
    )

    state = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=RunStateEnum.choices()
    )

    arguments = JSONField(
        default=dict,
        blank=True,
        null=True,
    )

    error_message = models.TextField(
        blank=True,
        null=True,
    )

    predecessor_runs = ArrayField(
        base_field=models.CharField(
            max_length=1000,
            blank=True,
        ),
        blank=True,
        null=True,
    )

    allocated_capacity = models.IntegerField(
        blank=True,
        null=True,
    )

    execution_time = models.IntegerField(
        blank=True,
        null=True,
    )

    timeout = models.IntegerField(
        blank=True,
        null=True,
    )

    max_capacity = models.IntegerField(
        blank=True,
        null=True,
    )

    worker_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=WorkerTypeEnum.choices()
    )

    number_of_workers = models.IntegerField(
        blank=True,
        null=True,
    )

    log_group_name = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "Job - " + self.job.name + ", Run ID: " + self.run_id if self.run_id else "NA"
