#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import horizon

# This panel will be loaded from horizon, because specified in enabled file.
# To register REST api, import below here.
# from cafe_ui.api import rest_api  # noqa: F401


class Metrics(horizon.Panel):
    name = "Metrics"
    slug = "metrics"
