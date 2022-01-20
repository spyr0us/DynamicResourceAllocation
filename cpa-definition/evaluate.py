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
import math

# JSON piped into this script example:
# {
#   "resource": "php-apache",
#   "runType": "api",
#   "metrics": [
#     {
#       "resource": "php-apache",
#       "value": "{\"current_replicas\": 3, \"rr_for30\": 20 \"art_for30\": 60}"
#     }
#   ]
# }

target_average_response_time = 320

def main():
    # Parse JSON into a dict
    spec = json.loads(sys.stdin.read())
    evaluate(spec)

def evaluate(spec):
    # Only expect 1 metric provided
    if len(spec["metrics"]) != 1:
        sys.stderr.write("Expected 1 metric")
        exit(1)

    # Get the metric value, there should only be 1
    metric_value = json.loads(spec["metrics"][0]["value"])

    # Get the current replicas from the metric
    current_replicas = metric_value["current_replicas"]
    # Get the average_response_time_for30 value from the metric
    art_for30 = metric_value["art_for30"]
    # Get the request_rate_for30 value from the metric
    #rr_for30 = metric_value["rr_for30"]

    # Calculate target replicas
    target_replicas = math.ceil(current_replicas * ( art_for30 / target_average_response_time))

    # Build JSON dict with targetReplicas
    evaluation = {}
    evaluation["targetReplicas"] = target_replicas

    # Output JSON to stdout
    sys.stdout.write(json.dumps(evaluation))

if __name__ == "__main__":
    main()