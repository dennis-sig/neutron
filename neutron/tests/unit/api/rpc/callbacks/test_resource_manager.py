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


from neutron.api.rpc.callbacks import registry as rpc_registry
from neutron.api.rpc.callbacks import resources


from neutron.tests import base


class ResourcesCallbackRequestTestCase(base.BaseTestCase):

    def setUp(self):
        super(ResourcesCallbackRequestTestCase, self).setUp()
        self.resource_id = '46ebaec0-0570-43ac-82f6-60d2b03168c4'
        self.qos_rule_id = '5f126d84-551a-4dcf-bb01-0e9c0df0c793'

    def test_resource_callback_request(self):

        #TODO(QoS) convert it to the version object format
        def _get_qos_policy_cb(resource, policy_id, **kwargs):
            qos_policy = {
                "tenant_id": "8d4c70a21fed4aeba121a1a429ba0d04",
                "id": "46ebaec0-0570-43ac-82f6-60d2b03168c4",
                "name": "10Mbit",
                "description": "This policy limits the ports to 10Mbit max.",
                "shared": False,
                "rules": [{
                    "id": "5f126d84-551a-4dcf-bb01-0e9c0df0c793",
                    "max_kbps": "10000",
                    "max_burst_kbps": "0",
                    "type": "bnadwidth_limit"
                }]
            }
            return qos_policy

        #TODO(QoS) convert it to the version object format
        def _get_qos_bandwidth_limit_rule_cb(resource, rule_id, **kwargs):
            bandwidth_limit = {
                "id": "5f126d84-551a-4dcf-bb01-0e9c0df0c793",
                "qos_policy_id": "46ebaec0-0570-43ac-82f6-60d2b03168c4",
                "max_kbps": "10000",
                "max_burst_kbps": "0",
            }
            return bandwidth_limit

        rpc_registry.register_provider(
                        _get_qos_bandwidth_limit_rule_cb,
                        resources.QOS_RULE)

        rpc_registry.register_provider(
            _get_qos_policy_cb,
            resources.QOS_POLICY)

        self.ctx = None
        kwargs = {'context': self.ctx}

        qos_policy = rpc_registry.get_info(
            resources.QOS_POLICY,
            self.resource_id,
            **kwargs)
        self.assertEqual(self.resource_id, qos_policy['id'])

        qos_rule = rpc_registry.get_info(
            resources.QOS_RULE,
            self.qos_rule_id,
            **kwargs)
        self.assertEqual(self.qos_rule_id, qos_rule['id'])
