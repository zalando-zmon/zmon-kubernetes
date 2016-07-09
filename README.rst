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


ZMON Database setup
===================

Now we need to create the database content, clone/download zmon controller for this.

.. code-block:: bash

export MINIKUBE_IP=$(minikube ip)

cd ~/git/zmon-controller/zmon-controller-master/database/zmon
psql -h $MINIKUBE_IP -p 31088 -c "CREATE DATABASE local_zmon_db;" postgres
psql -h $MINIKUBE_IP -p 31088 -c 'CREATE EXTENSION IF NOT EXISTS hstore;'
psql -h $MINIKUBE_IP -p 31088 -c "CREATE ROLE zmon WITH LOGIN PASSWORD '--secret--';" postgres
find -name '*.sql' | sort | xargs cat | psql -h $MINIKUBE_IP -p 31088


ZMON components
===============

.. code-block:: bash

  kubectl create -f deployments/zmon-eventlog-service.yaml
  kubectl create -f services/zmon-eventlog-service.yaml

  kubectl create -f deployments/zmon-controller.yaml
  kubectl create -f services/zmon-controller-service.yaml

  kubectl create -f deployments/zmon-scheduler.yaml

  kubectl create -f deployments/zmon-worker.yaml
