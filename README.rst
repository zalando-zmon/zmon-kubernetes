ZMON on Kubernetes
==================

For demo purposes provide k8s templates.

Config used is in:

.. code-block:: bash

  config.yaml

Then run:

.. code-block:: bash

  ./zmon-k8s.py

This generates all required deployment files.

Remember the generated password and tokens.

Note
====

PostgreSQL and Cassandra do not use persistent volumes!

Deployment
==========

Create Namespace
----------------

.. code-block:: bash

  kubectl create namespace zmon

Dependencies
------------

.. code-block:: bash

  kubectl create -f dependencies/cassandra/deployment.yaml
  kubectl create -f dependencies/cassandra/service.yaml

  kubectl create -f dependencies/kairosdb/deployment.yaml
  kubectl create -f dependencies/kairosdb/service.yaml

  kubectl create -f dependencies/redis/deployment.yaml
  kubectl create -f dependencies/redis/service.yaml

  kubectl create -f dependencies/postgresql/deployment.yaml
  kubectl create -f dependencies/postgresql/service.yaml

ZMON source download
====================

wget https://github.com/zalando-zmon/zmon-controller/archive/master.zip -O zmon-controller.zip
wget https://github.com/zalando-zmon/zmon-eventlog-service/archive/master.zip -O zmon-eventlog-service.zip

mkdir -p zmon-controller-source
mkdir -p zmon-eventlog-service-source

unzip zmon-controller.zip -d zmon-controller-source
unzip zmon-eventlog-service.zip -d zmon-eventlog-service-source

ZMON Database setup
===================

.. code-block:: bash

  export MINIKUBE_IP=$(minikube ip)

  cd zmon-controller-source/zmon-controller-master/database/zmon
  psql -h $MINIKUBE_IP -p 31088 -c "CREATE DATABASE local_zmon_db;" postgres
  psql -h $MINIKUBE_IP -p 31088 -c 'CREATE EXTENSION IF NOT EXISTS hstore;' local_zmon_db
  psql -h $MINIKUBE_IP -p 31088 -c "CREATE ROLE zmon WITH LOGIN PASSWORD '{{postgresql_password}}';" postgres
  find -name '*.sql' | sort | xargs cat | psql -h $MINIKUBE_IP -p 31088 -U postgres

  psql -h $MINIKUBE_IP -p 31088 -f zmon-eventlog-service-source/zmon-eventlog-service-master/database/eventlog/00_create_schema.sql local_zmon_db


ZMON components
===============

.. code-block:: bash

  kubectl create -f deployments/zmon-eventlog-service.yaml
  kubectl create -f services/zmon-eventlog-service.yaml

  kubectl create -f deployments/zmon-controller.yaml
  kubectl create -f services/zmon-controller-service.yaml

  kubectl create -f deployments/zmon-scheduler.yaml

  kubectl create -f deployments/zmon-worker.yaml
