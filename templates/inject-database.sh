export MINIKUBE_IP=$(minikube ip)

cd zmon-controller-source/zmon-controller-master/database/zmon
psql -h $MINIKUBE_IP -p 31088 -c "CREATE DATABASE local_zmon_db;" postgres
psql -h $MINIKUBE_IP -p 31088 -c 'CREATE EXTENSION IF NOT EXISTS hstore;' local_zmon_db
psql -h $MINIKUBE_IP -p 31088 -c "CREATE ROLE zmon WITH LOGIN PASSWORD '{{postgresql_password}}';" postgres
find -name '*.sql' | sort | xargs cat | psql -h $MINIKUBE_IP -p 31088 -U postgres

psql -h $MINIKUBE_IP -p 31088 -f zmon-eventlog-service-source/zmon-eventlog-service-master/database/eventlog/00_create_schema.sql local_zmon_db
