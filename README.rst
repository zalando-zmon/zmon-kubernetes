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

Note
====

PostgreSQL and Cassandra do not use persistent volumes!

Deployment
==========

Dependencies
------------

.. codeblock:: bash

  kubectl create -f dependencies/cassandra/deployment.yaml
  kubectl create -f dependencies/cassandra/service.yaml

  kubectl create -f dependencies/kairosdb/deployment.yaml
  kubectl create -f dependencies/kairosdb/service.yaml

  kubectl create -f dependencies/redis/deployment.yaml
  kubectl create -f dependencies/redis/service.yaml

  kubectl create -f dependencies/postgresql/deployment.yaml
  kubectl create -f dependencies/postgresql/service.yaml


Now we need to create the database content:

.. codeblock:: bash
