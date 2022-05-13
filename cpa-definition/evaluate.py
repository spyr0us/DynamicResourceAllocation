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
#
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

    # Get all the metric values
    art_for_10 = metric_value["art_for_10"]
    cpu_cores = metric_value["cpu_cores"]
    cpu_per_limit = metric_value["cpu_per_limit"]
    cpu_throttling = metric_value["cpu_throttling"]
    memory_in_MB = metric_value["memory_in_MB"]
    memory_per_limit = metric_value["memory_per_limit"]
    replicas_count = metric_value["replicas_count"]
    rr_for_2 = metric_value["rr_for_2"]
    rr_for_30 = metric_value["rr_for_30"]
    total_requests_interval_30 = metric_value["total_requests_interval_30"]

    # Calculate target replicas
    #target_replicas = math.ceil(current_replicas * ( rr_for30 / target_average_response_time))
    target_replicas=1
    # Build JSON dict with targetReplicas
    evaluation = {}
    evaluation["targetReplicas"] = target_replicas

    # Output JSON to stdout
    sys.stdout.write(json.dumps(evaluation))

if __name__ == "__main__":
    main()