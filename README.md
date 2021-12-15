# DynamicResourceAllocation
Dynamic Resource Allocation in Kubernetes

1) Αρχίζουμε το minikube με την εξής εντολή 

$ minikube delete && minikube start --kubernetes-version=v1.22.3 --memory=6g --bootstrapper=kubeadm --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook --extra-config=scheduler.bind-address=0.0.0.0 --extra-config=controller-manager.bind-address=0.0.0.0

2) Στο github της εφαρμογής αναγνώρισης εικόνας (https://github.com/tararouras/alphabot-ppl/tree/dockerize-edge-server),  αφού έχουμε κάνει gitclone το επιθυμητό branch του repository , αλλάζουμε στο αρχείο edge_server_requirements.txt το opencv-python σε opencv-python==4.2.0.32. Ακόμα μετανομάζουμε προσωρινά το αρχείο Dockerfile.edge_server σε σκέτο Dockerfile.

3) Πριν κάνουμε Build την εικόνα μας , χρησιμοποιούμε την εντολή eval $(minikube docker-env) και έπειτα πραγματοποιούμε κανονικά την εντολή " docker build -t imagerec . " . Διαγράφουμε έπειτα από το αρχείο edge-server-deployment-small.yaml όλο το κομμάτι του Node affinity Και αλλάζουμε το όνομα της εικόνας σε imagerec:latest . Τέλος κάνουμε apply το deployment Και το αντίστοιχο service.

4) Ακολουθώ τις οδηγίες που βρίσκονται εδώ https://github.com/prometheus-operator/kube-prometheus/tree/release-0.9 ( προσοχή έχει ορθογραφικό λάθος γράφει 0.7 αντί για 0.9 σε κάποιες εντολές + go install δε λειτουργεί συνήθως θα θελήσεις άλλο τρόπο ) . Παράλληλα στο αρχείο example.jsonnet θα κάνουμε uncomment τα node και τα custom metrics , ενώ στα custom-metrics.lisbonnet έχουμε προσθέσει και έναν έξτρα κανόνα για flask http metrics. Μετά χρησιμοποιώντας το build.sh example.jsonnet δημιουργούνται τα απαραίτητα manifests που κάνουμε apply . Τέλος κάνω deploy και το εξής yaml file edge-server-prom-rules.yaml που περιέχει διάφορους κανόνες για την εφαρμογή μας. 

5) Για να δημιουργήσω φόρτο στην εργασία τρέχω απλά "python3 startap.py" , προσέχοντας να υπάρχει ο φάκελος με τις εικόνες στο directory που δουλεύω Ακόμα αν σε δεύτερο terminal εκτελώ kubectl logs edge-server-cv θα βλέπω και τις απαντήσεις του server. 

6) Κάνω import στη grafana το json αρχείου που έχω επισυννάψει για να εμφανιστούν τα 5 dashboards με τα διάφορα metrics ( με αλλαγή του κανόνα number of pods σε "expr": "count(count by (pod) (flask_http_request_total{pod=~\"edge-server-.*\"}))" ). 

7) Από το https://github.com/jthomperoo/custom-pod-autoscaler-operator/blob/master/INSTALL.md εγκαθιστώ τον CustomPodAutoscaler-Operator με helm -> Cluster Scoped Install ( Έχει σημασία με αυτόν τον τρόπο γιατί αλλιώς δεν έχει κάποια απαραίτητα προνόμια ).

8) Στο φάκελο cpa-defintion κάνω " docker build -t cpa_python ." και έπειτα στο Project directory τώρα, κάνω kubectl apply -f τα αρχεία "cpa-role.yaml" και "edge-server-cpa-small.yaml" ( Το πρώτο αρχείο δημιουργεί ένα role για να έχει ο cpa, access σε custom και external metrics ). 

9) Για να αρχίσει ο cpa να βρίσκει το metric , μπορεί να χρειαστεί στην αρχή να τρέξουμε για λίγο διάστημα την εντολή " python3 startap.py" και για να σιγουρευτούμε πως ο cpa μας δουλεύει , μπορούμε να κάνουμε είτε "kubectl logs python-custom-autoscaler" ή να δούμε αν υπάρχει κάποιο πρόβλημα με το API κάνοντας " kubectl get --raw="/apis/custom.metrics.k8s.io/v1beta1/namespaces/default/services/edge-server-cv/edge_server_request_rate_for_30" .



