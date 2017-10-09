from django.views.generic import TemplateView
from tarifas.models import Plan


class Home(TemplateView):

    template_name = 'tarifas/home.html'

    @staticmethod
    def _parse_int(string, default=None):
        try:
            return int(string)
        except:
            return default

    def get_params(self, **kwargs):
        '''
        Return parsed GET params
        '''
        return {
            'min_minutes': self._parse_int(
                self.request.GET.get('min_minutes', None)
            ),
            'min_mb': self._parse_int(
                self.request.GET.get('min_mb', None)
            ),
            'min_sms': self._parse_int(
                self.request.GET.get('min_sms', None)
            ),
        }

    def get_cheapest_plan(self, min_minutes, min_mb, min_sms):
        '''
        Get the cheapest `Plan` combined with `SMSPlan`s and/or
        `DataPlan`s.

        He's what it should happen:

        1. Filters Plan to minutes_franchise >= min_minutes
        2. Order by value
        3. Set the first one as possible solotion
        4. Annotate how many MB needs to fulfill each plan
        5. Annotate how many SMS needs to fulfill each plan

        6.

        7. Check if there's Ilimited SMS Plan
            7.1. If yes, check if min_sms > (agg_sms + max sms_plan)
                7.1.1. If yes, set SMSPlan as Ilimitado
            7.1.2. If not, set min sms_plan based on (agg_sms + sms_plan)


        '''
        # if not min_minutes:
            # filtered_plans = Plan.objects.order_by('value')
        # else:
            # filtered_plans = Plan.objects.order_by('value').filter(
                # minutes_franchise__gte=min_minutes
            # )
        print(min_minutes, min_mb, min_sms)
        return {
            'cheapest_plan': Plan.objects.filter(
                    minutes_franchise__gte=min_minutes if min_minutes else 0,
                    data_mb__gte=min_mb if min_mb else 0,
                    sms_pack_size__gte=min_sms if min_sms else 0
                ).order_by('value').first(),
            # 'base_plan': Plan.objects.all().first(),
            # 'sms_plans': [],
            # 'data_plans': [],
        }

    def get_context_data(self, **kwargs):
        '''
        Return template context
        '''
        context = super().get_context_data(**kwargs)
        params = self.get_params(**kwargs)
        context['params'] = params
        context['data'] = self.get_cheapest_plan(**params)
        return context

