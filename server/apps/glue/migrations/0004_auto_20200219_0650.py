# Generated by Django 3.0.3 on 2020-02-19 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glue', '0003_gluejob_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='gluejobrun',
            name='number_of_workers',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gluejobrun',
            name='worker_type',
            field=models.CharField(choices=[('Standard', 'Standard'), ('G1.X', 'G1 X'), ('G2.X', 'G2 X')], default='Standard', max_length=255),
            preserve_default=False,
        ),
    ]
