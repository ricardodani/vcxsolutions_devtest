from django.views.generic import TemplateView
from tarifas.core import PackageSet


class Home(TemplateView):

    template_name = 'tarifas/home.html'

    def get_params(self):
        def parse_param(attrname, default=0):
            try:
                return int(self.request.GET.get(attrname, default))
            except Exception:
                return default
        return {
            'min_minutes': parse_param('min_minutes'),
            'min_mb': parse_param('min_mb'),
            'min_sms': parse_param('min_sms'),
        }

    def get_data(self, **kwargs):
        pset = PackageSet(**kwargs)
        cheapests = pset.get_cheapest_packages()
        return {
            'cheapest': cheapests[0] if cheapests else None,
            'other_options': cheapests[1:4]
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.get_params()
        context['params'] = params
        context['data'] = self.get_data(**params)
        return context
