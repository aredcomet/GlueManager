from django.contrib import admin

from apps.glue.models import GlueJob, GlueJobRun


@admin.register(GlueJob)
class GlueJobAdmin(admin.ModelAdmin):
    pass


@admin.register(GlueJobRun)
class GlueJobRunAdmin(admin.ModelAdmin):
    pass
