from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from apps.glue.models import GlueJobRun, GlueJob, RunStateEnum
from apps.glue.serializers import GlueJobRunSerializer


class GlueJobRunViewSet(viewsets.ModelViewSet):
    queryset = GlueJobRun.objects.all()

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        glue_job_run = self.get_object()
        serializer = self.get_serializer(glue_job_run)
        return Response(serializer.data)

    def create(self, request):
        data = request.data

        try:
            job = GlueJob.objects.get(name=data.get('job_name'))
        except GlueJob.DoesNotExist:
            return Response(data={'errors': 'Invalid Job Name'}, status=status.HTTP_400_BAD_REQUEST)

        data.update({
            "state": RunStateEnum.QUEUED.value,
            "job": job.id,
        })
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            instance
            return Response(data={'id': str(instance.id)}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        return GlueJobRunSerializer(*args, **kwargs)
