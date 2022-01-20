# Copyright 2021 The Custom Pod Autoscaler Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys

    # JSON piped in this script example:
    # "runType": "scaler",
    #  "kubernetesMetrics": [
    #     {
    #         "current_replicas": 1,
    #         "spec": {
    #             "type": "Object",
    #             "object": {
    #                 "describedObject": {
    #                     "kind": "Service",
    #                     "name": "edge-server-cv",
    #                     "apiVersion": "/v1"
    #                 },
    #                 "metric": {
    #                     "name": "edge_server_request_rate_for_30"
    #                 },
    #                 "target": {
    #                     "type": "Value"
    #                 }
    #             }
    #         },
    #         "object": {
    #             "current": {
    #                 "value": 206
    #             },
    #             "ready_pod_count": 1,
    #             "timestamp": "2022-01-19T19:03:57Z"
    #         }
    #     },
    #     {
    #         "current_replicas": 1,
    #         "spec": {
    #             "type": "Object",
    #             "object": {
    #                 "describedObject": {
    #                     "kind": "Service",
    #                     "name": "edge-server-cv",
    #                     "apiVersion": "/v1"
    #                 },
    #                 "metric": {
    #                     "name": "edge_server_art_for_30"
    #                 },
    #                 "target": {
    #                     "type": "Value"
    #                 }
    #             }
    #         },
    #         "object": {
    #             "current": {
    #                 "value": 512
    #             },
    #             "ready_pod_count": 1,
    #             "timestamp": "2022-01-19T19:03:57Z"
    #         }
    #     }
    # ]

def main():
    # Parse JSON into a dict
    spec = json.loads(sys.stdin.read())
    # Debugging on a container level
    with open('metrics_input_data.json', 'a', encoding='utf-8') as f:
        json.dump(spec, f, ensure_ascii=False, indent=4)
    metric(spec)

def metric(spec):
    # Get the first Kubernetes metrics value
    flask_metrics_a = spec["kubernetesMetrics"][0]
    # Pull out the current replicas
    current_replicas = flask_metrics_a["current_replicas"]
    # Get the first object metric info
    object_a = flask_metrics_a["object"]
    # Get the current tag
    object_info_a = object_a["current"]
    # Get the value of the first metric
    rr_for30 = object_info_a["value"]
    # Get the second Kubernetes metrics value
    flask_metrics_b = spec["kubernetesMetrics"][1]
    # Get the second object metric info
    object_b = flask_metrics_b["object"]
    # Get the current tag
    object_info_b = object_b["current"]
    # Get the value of the second metric
    art_for30 = object_info_b["value"]


    # # Get the third Kubernetes metrics value #############
    # flask_metrics_c = spec["kubernetesMetrics"][2]
    # # Get the third object metric info
    # object_c = flask_metrics_c["object"]
    # # Get the current tag
    # current_c = object_c["current"]
    # # Get the value of the third metric
    # cpu_for60 = current_c["value"]
    # # Get the fourth Kubernetes metrics value
    # flask_metrics_d = spec["kubernetesMetrics"][3]
    # # Get the fourth object metric info
    # object_d = flask_metrics_d["object"]
    # # Get the current tag
    # current_d = object_d["current"]
    # # Get the value of the fourth metric
    # memory = current_d["value"]

    
    # Generate some JSON to pass to the evaluator
    sys.stdout.write(json.dumps(
        {
            "current_replicas": current_replicas,
            "rr_for30": rr_for30,
            "art_for30": art_for30,
            #"cpu_for60": cpu_for60,
            #"memory": memory

        }
    ))

if __name__ == "__main__":
    main()