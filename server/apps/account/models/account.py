from django.db import models
from django.contrib.postgres.fields import JSONField


def account_config_default():
    return {
        "max_dpu": 300,
        "max_jobs": 1000,
        "max_concurrent_job_runs": 50,
        "max_concurrent_job_runs_per_job": 1000,
        "hot_launches": 10,
        "cool_off_after_hot_launch": 600,
    }


class Account(models.Model):
    name = models.CharField(
        max_length=254,
        null=False,
        blank=False,
    )

    config = JSONField(
        default=account_config_default,
        blank=False,
        null=False,
    )

    aws_region = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
