from django.contrib import admin
from tarifas.models import Plan, SMSPlan, DataPlan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'data_display', 'sms_pack', 'value')


class SMSPlanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value')


class DataPlanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value')


admin.site.register(Plan, PlanAdmin)
admin.site.register(SMSPlan, SMSPlanAdmin)
admin.site.register(DataPlan, DataPlanAdmin)
