from django.contrib import admin
from tarifas.models import Plan, SMSPlan, DataPlan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_pack', 'sms_pack', 'value')


class SMSPlanAdmin(admin.ModelAdmin):
    list_display = ('sms_pack', 'value')


class DataPlanAdmin(admin.ModelAdmin):
    list_display = ('data_pack', 'value')


admin.site.register(Plan, PlanAdmin)
admin.site.register(SMSPlan, SMSPlanAdmin)
admin.site.register(DataPlan, DataPlanAdmin)
