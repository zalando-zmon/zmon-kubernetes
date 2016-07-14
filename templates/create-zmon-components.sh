kubectl create -f deployments/zmon-eventlog-service.yaml
kubectl create -f services/zmon-eventlog-service-service.yaml

kubectl create -f deployments/zmon-controller.yaml
kubectl create -f services/zmon-controller-service.yaml

kubectl create -f deployments/zmon-scheduler.yaml
kubectl create -f services/zmon-scheduler-service.yaml

kubectl create -f deployments/zmon-worker.yaml
