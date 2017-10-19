from collections import namedtuple
from tarifas.models import Plan, SMSPlan, DataPlan


class PackageSet(object):
    '''
    View utility class that get`s Plans based on `min_minutes` param,
    instantiate a Package class from each of them. And calculates the
    best affordable Package.
    '''

    def __init__(self, min_minutes=0, min_mb=0, min_sms=0):
        self.min_minutes, self.min_mb, self.min_sms = (
            min_minutes, min_mb, min_sms
        )
        self.base_query = self.get_base_query()
        self.package_set = self.get_package_set()

    def get_package_set(self):
        return (
            Package(plan, self.min_mb, self.min_sms)
            for plan in self.base_query
        )

    def get_base_query(self):
        return Plan.objects.filter(
            minutes_franchise__gte=self.min_minutes
        ).order_by('value')

    def get_cheapest_packages(self):
        return sorted(
            self.package_set,
            key=lambda package: package.total_value
        )


class Package(object):
    '''
    Utility class for a Package.
    Package is a a Plan with or without aditional plans like SMSPlan and/or
    DataPlan, based on the input parameters as min_mb and min_sms.
    '''

    def get_data_plans(self):
        mb_left = (
            self.min_mb - self.plan.data_mb
            if self.min_mb > self.plan.data_mb
            else 0
        )
        DataPlanPack = namedtuple('DataPlanPack', ['plan', 'quantity', 'value'])
        data_plans = []

        # first query if there's a slight bigger plan and rerturn it if yes
        cheapest = DataPlan.objects.filter(
            data_mb__gte=mb_left
        ).order_by('value').first()
        if cheapest:
            data_plans = [DataPlanPack(cheapest, 1, cheapest.value)]
        # if not, mount a set of DataPlanPack to fullfill the desired MB
        else:
            possible_data_plans = list(DataPlan.objects.filter(
                data_mb__lt=mb_left
            ).order_by('-data_mb'))
            while mb_left > 0:
                try:
                    plan_to_add = possible_data_plans.pop(0)
                except IndexError:
                    break
                quantity = mb_left // plan_to_add.data_mb
                data_plans.append(
                    DataPlanPack(
                        plan_to_add, quantity, plan_to_add.value * quantity
                    )
                )
                mb_left = (mb_left % plan_to_add.data_mb)
        return data_plans

    def get_sms_plan(self):
        sms_left = (
            self.min_sms - self.plan.sms_pack_size
            if self.min_sms > self.plan.sms_pack_size
            else 0
        )
        if sms_left > 0:
            cheapest = SMSPlan.objects.filter(
                sms_pack_size__gte=sms_left,
                unlimited=False
            ).order_by('value').first()
            if cheapest:
                return cheapest
            else:
                unlimited = SMSPlan.objects.filter(unlimited=True).first()
                if unlimited:
                    return unlimited

    @property
    def total_value(self):
        value_data_plans = sum(
            (plan_pack.quantity * plan_pack.plan.value)
            for plan_pack in self.data_plans
        )
        value_sms_plan = self.sms_plan.value if self.sms_plan else 0
        return self.plan.value + value_data_plans + value_sms_plan

    @property
    def total_data(self):
        mb_data_plans = sum(
            (plan_pack.plan.data_mb * plan_pack.quantity)
            for plan_pack in self.data_plans
        )
        total = self.plan.data_mb + mb_data_plans
        if total >= 1024:
            return '{0:.3g}GB'.format(total / 1024)
        else:
            return '{}MB'.format(total)

    @property
    def total_sms(self):
        if self.sms_plan and self.sms_plan.unlimited:
            return str(self.sms_plan)
        elif self.sms_plan:
            return '{} SMS'.format(
                self.plan.sms_pack_size + self.sms_plan.sms_pack_size
            )
        else:
            return '{} SMS'.format(self.plan.sms_pack_size)

    def __init__(self, plan, min_mb, min_sms):
        self.plan, self.min_mb, self.min_sms = plan, min_mb, min_sms
        self.data_plans = self.get_data_plans()
        self.sms_plan = self.get_sms_plan()
