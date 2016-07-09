ZMON on Kubernetes
==================

For demo purposes provide k8s templates.

Config used is in:

.. code-block:: bash

  config.yaml

Then run:

.. code-block:: bash

  ./zmon-k8s.py

The generated k8s deployment definitions will be in ``deployments`` folder.

The defined services are in the services folder.


Note
====
Setting up the dependencies can done by example from the dependency folder. Careful, there are no persistent volumes!!
