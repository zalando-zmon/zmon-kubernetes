export MINIKUBE_IP=$(minikube ip)

cd ~/git/zmon-controller/zmon-controller-master/database/zmon
psql -h $MINIKUBE_IP -p 31088 -c "CREATE DATABASE local_zmon_db;" postgres
psql -h $MINIKUBE_IP -p 31088 -c 'CREATE EXTENSION IF NOT EXISTS hstore;'
psql -h $MINIKUBE_IP -p 31088 -c "CREATE ROLE zmon WITH LOGIN PASSWORD '{{postgresql_password}}';" postgres
find -name '*.sql' | sort | xargs cat | psql
