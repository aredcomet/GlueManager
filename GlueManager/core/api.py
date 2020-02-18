from rest_framework import routers, serializers, viewsets
from .models import GlueConfig, GlueJob, GlueArguments


class GlueJobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlueJob
        fields = ()


class GlueJobViewSet(viewsets.ModelViewSet):
    queryset = GlueJob.objects.all()
    serializer_class = GlueJobSerializer


class GlueArgumentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlueArguments
        fields = ()


class GlueArgumentsViewSet(viewsets.ModelViewSet):
    queryset = GlueArguments.objects.all()
    serializer_class = GlueArgumentsSerializer


