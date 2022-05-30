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
import pickle 
import sklearn
from sklearn.preprocessing import StandardScaler
import numpy as np 
import os 


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
    edge_metrics_a = spec["kubernetesMetrics"][0]
    current_replicas = edge_metrics_a["current_replicas"]
    # Get the first object metric info
    object_a = edge_metrics_a["object"]
    # Get the current tag
    object_info_a = object_a["current"]
    # Get the value of the first metric IN SECONDS
    art_for_10 = object_info_a["value"] / 1000
    # Get the second Kubernetes metrics value
    edge_metrics_b = spec["kubernetesMetrics"][1]
    # # Get the second object metric info
    object_b = edge_metrics_b["object"]
    # # Get the current tag
    object_info_b = object_b["current"]
    # # Get the value of the second metric
    cpu_cores = object_info_b["value"] / 1000
    # # Get the third Kubernetes metrics value #############
    edge_metrics_c = spec["kubernetesMetrics"][2]
    # # Get the third object metric info
    object_c = edge_metrics_c["object"]
    # # Get the current tag
    current_c = object_c["current"]
    # # Get the value of the third metric
    cpu_per_limit = current_c["value"] / 1000
    # # Get the fourth Kubernetes metrics value
    edge_metrics_d = spec["kubernetesMetrics"][3]
    # # Get the fourth object metric info
    object_d = edge_metrics_d["object"]
    # # Get the current tag
    current_d = object_d["current"]
    # # Get the value of the fourth metric
    cpu_throttling = current_d["value"] / 1000
    # # Get the fifth Kubernetes metrics value
    edge_metrics_e = spec["kubernetesMetrics"][4]
    # # Get the fifth object metric info
    object_e = edge_metrics_e["object"]
    # # Get the current tag
    current_e = object_e["current"]
    # # Get the value of the fifth metric
    memory_in_MB = current_e["value"] / 1048576000
    # # Get the sixth Kubernetes metrics value
    edge_metrics_f = spec["kubernetesMetrics"][5]
    # # Get the sixth object metric info
    object_f = edge_metrics_f["object"]
    # # Get the current tag
    current_f = object_f["current"]
    # # Get the value of the sixth metric
    memory_per_limit = current_f["value"] / 1000
    # # Get the seventh Kubernetes metrics value
    edge_metrics_g = spec["kubernetesMetrics"][6]
    # # Get the seventh object metric info
    object_g = edge_metrics_g["object"]
    # # Get the current tag
    current_g = object_g["current"]
    # # Get the value of the seventh metric
    replicas_count = current_g["value"] / 1000
    # # Get the eight Kubernetes metrics value
    edge_metrics_h = spec["kubernetesMetrics"][7]
    # # Get the eigth object metric info
    object_h = edge_metrics_h["object"]
    # # Get the current tag
    current_h = object_h["current"]
    # # Get the value of the eigth metric
    rr_for_2 = current_h["value"] / 1000
    # # Get the ninth Kubernetes metrics value
    edge_metrics_i = spec["kubernetesMetrics"][8]
    # # Get the ninth object metric info
    object_i = edge_metrics_i["object"]
    # # Get the current tag
    current_i = object_i["current"]
    # # Get the value of the ninth metric
    rr_for_30 = current_i["value"] / 1000
    # # Get the tenth Kubernetes metrics value
    edge_metrics_j = spec["kubernetesMetrics"][9]
    # # Get the tenth object metric info
    object_j = edge_metrics_j["object"]
    # # Get the current tag
    current_j = object_j["current"]
    # # Get the value of the tenth metric
    total_requests_interval_30 = current_j["value"] / 1000
    
    ## Machine Learning Implementation 
    loaded_rfc, loaded_pca = pickle.load(open(r'RandomForest_and_PCA.sav', 'rb'))
    loaded_reg, loaded_svm , loaded_knn , loaded_nb = pickle.load(open(r'Regression_SVM_KNN_NB.sav', 'rb'))
    X = [[art_for_10*1000, cpu_throttling, cpu_per_limit, rr_for_30, memory_in_MB, cpu_cores, total_requests_interval_30, rr_for_2, current_replicas, memory_per_limit]]
    
    yreg = loaded_reg.predict(X)
    ysvm = loaded_svm.predict(X)
    yknn = loaded_knn.predict(X)
    ynb  = loaded_nb.predict(X)
    X1 = loaded_pca.transform(X)
    yrfc = loaded_rfc.predict(X1)
    
    
    # Generate some JSON to pass to the evaluator
    sys.stdout.write(json.dumps(
        {
            "art_for_10": art_for_10,
            "cpu_throttling": cpu_throttling,
            "cpu_per_limit": cpu_per_limit,
            "rr_for_30": rr_for_30,
            "memory_in_MB": memory_in_MB,
            "cpu_cores": cpu_cores,
            "total_requests_interval_30": total_requests_interval_30,
            "rr_for_2": rr_for_2,
            "current_replicas": current_replicas,
            #"replicas_count": replicas_count,
            "memory_per_limit": memory_per_limit,
            "RFC_scaling_decision": int(yrfc[0]),   
            "Regression_scaling_decision": int(yreg[0]),
            "SVM_scaling_decision": int(ysvm[0]),
            "KNN_scaling_decision": int(yknn[0]),
            "NB_scaling_decision": int(ynb[0])  
            }
    ))

if __name__ == "__main__":
    main()