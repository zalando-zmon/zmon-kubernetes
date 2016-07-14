ZMON on Kubernetes
==================

For demo purposes provide k8s templates.

Config used is in:

.. code-block:: bash

  config.yaml

Prepare K8S definitions:

.. code-block:: bash

  ./zmon-k8s.py

Next step is to run the printed commands :)

Minikube
========

Check that you give your VM enough resources:

.. code-block:: bash

  minikube start --memory=4000 --cpus=3


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

.. code-block:: bash

  wget https://github.com/zalando-zmon/zmon-controller/archive/master.zip -O zmon-controller.zip
  wget https://github.com/zalando-zmon/zmon-eventlog-service/archive/master.zip -O zmon-eventlog-service.zip

  mkdir -p zmon-controller-source
  mkdir -p zmon-eventlog-service-source

  unzip zmon-controller.zip -d zmon-controller-source
  unzip zmon-eventlog-service.zip -d zmon-eventlog-service-source

ZMON Database setup
===================

.. code-block:: bash

    export POSTGRES_NODE_IP=$(minikube ip)
    export POSTGRES_NODE_PORT=31088
    export PGPASSWORD={{admin_password}}

    psql -h $POSTGRES_NODE_IP -p $POSTGRES_NODE_PORT -U postgres -c "CREATE DATABASE local_zmon_db;" postgres
    psql -h $POSTGRES_NODE_IP -p $POSTGRES_NODE_PORT -U postgres -c 'CREATE EXTENSION IF NOT EXISTS hstore;' local_zmon_db
    psql -h $POSTGRES_NODE_IP -p $POSTGRES_NODE_PORT -U postgres -c "CREATE ROLE zmon WITH LOGIN PASSWORD '{{postgresql_password}}';" postgres
    psql -h $POSTGRES_NODE_IP -p $POSTGRES_NODE_PORT -U postgres -c "ALTER ROLE zmon WITH PASSWORD '{{postgresql_password}}';" postgres

    find "zmon-controller-source/zmon-controller-master/database/zmon" -name '*.sql' \
                                       | sort \
                                       | xargs cat \
                                       | psql -h $POSTGRES_NODE_IP -p $POSTGRES_NODE_PORT -U postgres -d local_zmon_db

    psql -h $POSTGRES_NODE_IP -p $POSTGRES_NODE_PORT -U postgres -f zmon-eventlog-service-source/zmon-eventlog-service-master/database/eventlog/00_create_schema.sql local_zmon_db


ZMON components
===============

.. code-block:: bash

  kubectl create -f deployments/zmon-eventlog-service.yaml
  kubectl create -f services/zmon-eventlog-service-service.yaml

  kubectl create -f deployments/zmon-controller.yaml
  kubectl create -f services/zmon-controller-service.yaml

  kubectl create -f deployments/zmon-scheduler.yaml
  kubectl create -f services/zmon-scheduler-service.yaml

  kubectl create -f deployments/zmon-worker.yaml
