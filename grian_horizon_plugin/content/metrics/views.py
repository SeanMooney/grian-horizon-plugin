import json

from django.views import generic

from grian_horizon_plugin.api import metrics

class IndexView(generic.TemplateView):
    template_name = 'metrics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metrics'] = json.dumps(metrics.placeholder_dataset())
        return context