from django.contrib import admin

# Register your models here.
from .models import Denounce


class DenounceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'denounce_status']
    list_editable = ["denounce_status"]


admin.site.register(Denounce, DenounceAdmin)
