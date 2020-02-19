from rest_framework import serializers

from apps.glue.models import GlueJobRun


class GlueJobRunSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlueJobRun
        fields = '__all__'
