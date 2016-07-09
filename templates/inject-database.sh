wget https://github.com/zalando-zmon/zmon-controller/archive/master.zip -O zmon-controller.zip
wget https://github.com/zalando-zmon/zmon-eventlog-service/archive/master.zip -O zmon-eventlog-service.zip

mkdir -p zmon-controller-source
mkdir -p zmon-eventlog-service-source

unzip zmon-controller.zip -d zmon-controller-source
unzip zmon-eventlog-service.zip -d zmon-eventlog-service-source

export MINIKUBE_IP=$(minikube ip)
export PGPASSWORD={{admin_password}}

psql -h $MINIKUBE_IP -p 31088 -U postgres -c "CREATE DATABASE local_zmon_db;" postgres
psql -h $MINIKUBE_IP -p 31088 -U postgres -c 'CREATE EXTENSION IF NOT EXISTS hstore;' local_zmon_db
psql -h $MINIKUBE_IP -p 31088 -U postgres -c "CREATE ROLE zmon WITH LOGIN PASSWORD '{{postgresql_password}}';" postgres
psql -h $MINIKUBE_IP -p 31088 -U postgres -c "ALTER ROLE zmon WITH PASSWORD '{{postgresql_password}}';" postgres

find "zmon-controller-source/zmon-controller-master/database/zmon" -name '*.sql' \
                                   | sort \
                                   | xargs cat \
                                   | psql -h $MINIKUBE_IP -p 31088 -U postgres -d local_zmon_db

psql -h $MINIKUBE_IP -p 31088 -U postgres -f zmon-eventlog-service-source/zmon-eventlog-service-master/database/eventlog/00_create_schema.sql local_zmon_db
