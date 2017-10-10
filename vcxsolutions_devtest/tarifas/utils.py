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
        data_plans = []
        while self.mb_left > 0:
            cheapest = DataPlan.objects.filter(
                data_mb__gte=self.mb_left
            ).order_by('value').first()
            if cheapest:
                self.mb_left = 0
                data_plans.append(cheapest)
                break
            else:
                biggest = DataPlan.objects.filter(
                    data_mb__lt=self.mb_left
                ).order_by('-data_mb').first()
                if biggest:
                    self.mb_left -= biggest.data_mb
                    data_plans.append(biggest)
                else:
                    break
        return data_plans

    def get_sms_plan(self):
        if self.sms_left > 0:
            cheapest = SMSPlan.objects.filter(
                sms_pack_size__gte=self.sms_left,
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
        value_data_plans = sum(plan.value for plan in self.data_plans)
        value_sms_plan = self.sms_plan.value if self.sms_plan else 0
        return self.plan.value + value_data_plans + value_sms_plan

    @property
    def total_data(self):
        mb_data_plans = sum(plan.data_mb for plan in self.data_plans)
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
        if min_mb > plan.data_mb:
            self.mb_left = min_mb - plan.data_mb
            self.data_plans = self.get_data_plans()
        else:
            self.data_plans = []

        if min_sms > plan.sms_pack_size:
            self.sms_left = min_sms - plan.sms_pack_size
            self.sms_plan = self.get_sms_plan()
        else:
            self.sms_plan = None
        self.sms_left = min_sms - plan.sms_pack_size
