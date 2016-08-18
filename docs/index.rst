==============
Henson-MongoDB
==============

Henson-MongoDB is a library that helps to easily integrate
`MongoDB <https://docs.mongodb.com>`_ into a
`Henson <https://henson.readthedocs.io>`_ application.

Installation
============

Henson-MongoDB can be installed with::

    $ python -m pip install Henson-MongoDB

.. warning::

    Henson-MongoDB is not yet available on the Python Package Index.

Configuration
=============

The following configuration settings can be added to the application.

+-----------------------------+----------------------------------------------+
| ``MONGODB_URI``             | The                                          |
|                             | `connection string URI`_ used to connect to  |
|                             | the server and provide any configuration not |
|                             | covered by other Henson-MongoDB settings.    |
+-----------------------------+----------------------------------------------+
| ``MONGODB_DOCUMENT_CLASS``  | The default class to use for documents       |
|                             | returned by queries. Default: ``dict``.      |
+-----------------------------+----------------------------------------------+
| ``MONGODB_TIME_ZONE_AWARE`` | Whether or not ``datetime`` instances        |
|                             | returned as values will be time zone aware.  |
|                             | Default: ``False``.                          |
+-----------------------------+----------------------------------------------+

The following values can be specified through the ``MONGODB_URI`` setting.

+------------------------+----------------------------------------------------+
| ``database``           | The name of the database to make available through |
|                        | the :attr:`~henson_mongodb.MongoDB.db` attribute.  |
+------------------------+----------------------------------------------------+
| ``replicaset``         | The name of the replica set to which to connect.   |
+------------------------+----------------------------------------------------+
| ``username``           | The username to use for authentication. If         |
|                        | provided, ``password`` must also be provided.      |
+------------------------+----------------------------------------------------+
| ``password``           | The password to use for authentication. If         |
|                        | provided, ``username`` must also be provided.      |
+------------------------+----------------------------------------------------+
| ``ssl``                | Whether or not to use SSL/TLS.                     |
+------------------------+----------------------------------------------------+
| ``authMechanism``      | The mechanism to use for authentication. The       |
|                        | supported types are ``DEFAULT`` and                |
|                        | ``MONGODB-X509``.                                  |
+------------------------+----------------------------------------------------+
| ``ssl_certfile``       | The path to the certificate file when using X.509. |
+------------------------+----------------------------------------------------+
| ``ssl_ca_certs``       | The path to the certificate authority when using   |
|                        | X.509.                                             |
+------------------------+----------------------------------------------------+
| ``max_pool_size``      | The maximum number of connections to each server   |
|                        | allowed. Requests will block if the number of      |
|                        | connections is exceeded.                           |
+------------------------+----------------------------------------------------+
| ``auto_start_request`` | Whether or not to connect to the server            |
|                        | immediately. If not, connection will be            |
|                        | established on the first operation.                |
|                        | Default: ``False``.                                |
+------------------------+----------------------------------------------------+

.. _connection string URI: https://docs.mongodb.com/manual/reference/connection-string/

Usage
=====

.. code::

    from henson import Application
    from henson_mongodb import MongoDB

    app = Application('application-with-mongodb')
    app.settings['MONGODB_URI'] = 'mongodb://localhost/henson'

    mongo = MongoDB(app)

    async def run(app, message):
        characters = await mongo.db.puppets.find({'show': message['show']})
        return characters

    app.callback = run

Henson-MongoDB is powered by `Motor <https://motor.readthedocs.io>`_. For
further details about how to interact with the database, please refer to the
`Motor tutorial <https://motor.readthedocs.io/en/stable/tutorial-asyncio.html>`_.

API
===

.. autoclass:: henson_mongodb.MongoDB
   :exclude-members: init_app
   :members:

Contents:

.. toctree::
   :maxdepth: 1



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
