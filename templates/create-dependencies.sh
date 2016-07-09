kubectl create namespace zmon

kubectl create -f dependencies/cassandra/deployment.yaml
kubectl create -f dependencies/cassandra/service.yaml

kubectl create -f dependencies/kairosdb/deployment.yaml
kubectl create -f dependencies/kairosdb/service.yaml

kubectl create -f dependencies/redis/deployment.yaml
kubectl create -f dependencies/redis/service.yaml

kubectl create -f dependencies/postgresql/deployment.yaml
kubectl create -f dependencies/postgresql/service.yaml
