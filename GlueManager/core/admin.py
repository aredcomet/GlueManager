from django.contrib import admin
from .models import GlueConfig, GlueJob, GlueArguments


# @admin.register(GlueConfig)
class AdminGlueConfig(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return True


class AdminGlueJob(admin.ModelAdmin):
    pass

class AdminGlueArguments(admin.ModelAdmin):
    pass


admin.site.register(GlueConfig, AdminGlueConfig)
admin.site.register(GlueJob, AdminGlueJob)
admin.site.register(GlueArguments, AdminGlueArguments)