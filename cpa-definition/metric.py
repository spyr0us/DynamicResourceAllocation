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

# JSON piped into this script example:
# {
#     "resource": "...",
#     "runType": "scaler",
#     "kubernetesMetrics": [
#       {
#         "current_replicas": 1,
#         "spec": {
#           "type": "Object",
#           "metric": {
#             "name": "queue_messages_ready",
#             "selector": "queue=worker_tasks",
#             "target": {
#               "type": "Value"
#             }
#           }
#         },
#         "object": { 
#           "current": {
#             "value": 5 
#           },
#           "ready_pod_count": 1,
#           "timestamp": "2021-04-05T18:10:10Z"
#         }
#       }
#     ]
#   }

def main():
    # Parse JSON into a dict
    spec = json.loads(sys.stdin.read())
    metric(spec)

def metric(spec):
    # Get the Kubernetes metrics value, there is only 1 expected, so it should be the first one
    flask_metrics = spec["kubernetesMetrics"][0]
    # Pull out the current replicas
    current_replicas = flask_metrics["current_replicas"]
    # Get the object metric info
    objecta = flask_metrics["object"]
    # Get the current tag
    current = objecta["current"]
    # Get the value of the metric
    average_value = current["value"]
    
    
    # Generate some JSON to pass to the evaluator
    sys.stdout.write(json.dumps(
        {
            "current_replicas": current_replicas,
            "average_value": average_value
        }
    ))

if __name__ == "__main__":
    main()