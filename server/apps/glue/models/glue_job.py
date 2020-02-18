import uuid

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class GlueJob(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=254,
        null=False,
        blank=False,
    )

    created_on = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )

    last_modified_on = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
    )

    execution_property = JSONField(
        default=dict,
    )

    command = JSONField(
        default=dict,
    )

    default_arguments = JSONField(
        default=dict,
    )

    max_retries = models.IntegerField(
        blank=False,
        null=False
    )

    allocated_capacity = models.IntegerField(
        blank=False,
        null=False
    )

    timeout = models.IntegerField(
        blank=False,
        null=False
    )

    max_capacity = models.IntegerField(
        blank=False,
        null=False
    )

    glue_version = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.name
