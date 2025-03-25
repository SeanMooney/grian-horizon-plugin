import logging
import itertools
import json
import random
import typing as ty


from django.conf import settings
from django import http
from django.views import generic

from openstack_dashboard.api.rest import utils
from openstack_dashboard.api.rest import urls

LOG = logging.getLogger(__name__)


@urls.register
class Metrics(generic.View):
    """Api to dispatch metrics requests"""
    url_regex = r'^metrics/placeholder_dataset/$'
    
    def get(self, request):
        return http.HttpResponse(json.dumps(placeholder_dataset()))
    
  
def hi() -> str:
    LOG.debug("hi")
    return "hi"

def placeholder_dataset() -> dict:
    """
    Return a static data set
    """
    labels = ["Used", "free", "Yellow", "Green", "Purple", "Orange"]
    data = {
        "labels": labels,
        "datasets": [{
            "label": "#1",
            "data": [random.randint(0, 100) for _ in range(len(labels))],
            "borderWidth": 1,
            "tension": 0.25,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointHoverRadius": 15,
            "fill": True
        },{
            "label": "#2",
            "data": [random.randint(0, 100) for _ in range(len(labels))],
            "borderWidth": 1,
            "tension": 0.25,
            "pointStyle": 'circle',
            "pointRadius": 5,
            "pointHoverRadius": 15,
            "fill": True
        }
        ]
    }
    
    return data

@urls.register
class TimeChartView(generic.TemplateView):
    template_name = 'metrics/partials/time-chart.html'
    url_regex = r'^metrics/time-chart/$'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chart_type'] = 'line'
        context['metrics'] = json.dumps(placeholder_dataset())
        return context