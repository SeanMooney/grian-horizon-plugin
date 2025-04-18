import json
import logging
import random


from django import http
from django.views import generic

from openstack_dashboard.api.rest import urls

LOG = logging.getLogger(__name__)


@urls.register
class Metrics(generic.View):
    """Api to dispatch metrics requests"""

    url_regex = r"^metrics/placeholder_dataset/$"

    def get(self, request):
        return http.HttpResponse(json.dumps(placeholder_dataset()))


@urls.register
class HypervisorMetricsSummary(generic.TemplateView):
    """Api to dispatch metrics requests"""

    template_name = "metrics/partials/hypervisor-summary.html"
    url_regex = r"^metrics/hypervisor_summary$"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_names = ("cpu_util", "ram_util", "disk_util")
        random_data = [
            random.randint(0, 100)  # nosec B311
            for _ in range(len(data_names))
        ]
        data_map = {
            key: json.dumps(
                add_use_free_bg_colors(
                    data_points_to_chart_js_data(
                        {"Used": val, "Free": 100 - val}
                    )
                )
            )
            for key, val in zip(data_names, random_data)
        }
        context.update(data_map)
        return context


def data_points_to_chart_js_data(data: dict) -> list[dict]:
    """Takes a dict of key value data and convert it to chartjs format

    {
      "labels": ["Used", "Free"],
      "datasets": [
        {
          "data": [58, 42],
        }
      ]
    }
    """
    return {"labels": [*data.keys()], "datasets": [{"data": [*data.values()]}]}


def add_use_free_bg_colors(data: dict) -> dict:
    for dataset in data.get("datasets"):
        dataset.update({"backgroundColor": ["#428bca", "#da1a31"]})
    return data


def placeholder_dataset() -> dict:
    """Return a static data set

    :return: dict
    """
    labels = ["Used", "free", "Yellow", "Green", "Purple", "Orange"]
    data = {
        "labels": labels,
        "datasets": [
            {
                "label": "#1",
                "data": [
                    random.randint(0, 100)  # nosec B311
                    for _ in range(len(labels))
                ],
                "borderWidth": 1,
                "tension": 0.25,
                "pointStyle": "circle",
                "pointRadius": 5,
                "pointHoverRadius": 15,
                "fill": True,
            },
            {
                "label": "#2",
                "data": [
                    random.randint(0, 100)  # nosec B311
                    for _ in range(len(labels))
                ],
                "borderWidth": 1,
                "tension": 0.25,
                "pointStyle": "circle",
                "pointRadius": 5,
                "pointHoverRadius": 15,
                "fill": True,
            },
        ],
    }

    return data


@urls.register
class TimeChartView(generic.TemplateView):
    template_name = "metrics/partials/time-chart.html"
    url_regex = r"^metrics/time-chart/$"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chart_type"] = "line"
        context["metrics"] = json.dumps(placeholder_dataset())
        return context
