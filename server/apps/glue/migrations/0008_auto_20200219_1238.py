# Generated by Django 3.0.3 on 2020-02-19 07:08

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue', '0007_auto_20200219_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gluejobrun',
            name='allocated_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gluejobrun',
            name='arguments',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='gluejobrun',
            name='last_modified_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gluejobrun',
            name='predecessor_runs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=1000), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='gluejobrun',
            name='started_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]