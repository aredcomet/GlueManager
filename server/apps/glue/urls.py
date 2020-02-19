from rest_framework.routers import DefaultRouter

from .views import (
    GlueJobRunViewSet,
)

router = DefaultRouter()
router.register(r'glue-job-run', GlueJobRunViewSet, basename='glue_job_run')


urlpatterns = router.urls
