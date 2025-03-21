import logging
import json
import typing as ty


from django.conf import settings
from django.views import generic

from openstack_dashboard.api.rest import utils
from openstack_dashboard.api.rest import urls

LOG = logging.getLogger(__name__)


@urls.register
class Metrics(generic.View):
    """Api to dispatch metrics requests"""
    url_regex = r'^metrics/$'
    
    @utils.ajax()
    def get(self, request):
        return placeholder_dataset()
  
def hi() -> str:
    LOG.debug("hi")
    return "hi"

def placeholder_dataset() -> dict:
    """
    Return a static data set
    """
    data = '''
    {
        "labels": ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        "datasets": [{
            "label": "# of Votes",
            "data": [12, 19, 3, 5, 2, 3],
            "borderWidth": 1
        }]
    }
    '''
    json_data = json.loads(data)
    return json_data
