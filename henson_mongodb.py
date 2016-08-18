"""MongoDB plugin for Henson."""

import os
import pkg_resources
import ssl

from henson import Extension
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorReplicaSetClient,
)
from pymongo import uri_parser

__all__ = ('MongoDB',)

try:
    _dist = pkg_resources.get_distribution(__name__)
    if not __file__.startswith(os.path.join(_dist.location, __name__)):
        # Manually raise the exception if there is a distribution but
        # it's installed from elsewhere.
        raise pkg_resources.DistributionNotFound
except pkg_resources.DistributionNotFound:
    __version__ = 'development'
else:
    __version__ = _dist.version


class MongoDB(Extension):
    """An interface to interact with MongoDB."""

    REQUIRED_SETTINGS = ('MONGODB_URI',)

    DEFAULT_SETTINGS = {
        'MONGODB_DOCUMENT_CLASS': dict,
        'MONGODB_TIME_ZONE_AWARE': False,
    }

    client = None

    def init_app(self, app):
        """Initialize an application instance.

        Args:
            app (henson.base.Application): The application instance to
                initialize.
        """
        super().init_app(app)

        # Keyword arguments that will be passed to the MongoDB client.
        kwargs = {}

        info = uri_parser.parse_uri(app.settings['MONGODB_URI'])
        if not info['database']:
            raise ValueError('A database name must be specified.')
        app.settings['MONGODB_DATABASE'] = info['database']
        app.settings['MONGODB_USERNAME'] = info['username']
        app.settings['MONGODB_PASSWORD'] = info['password']

        app.settings['MONGODB_USE_SSL'] = info['options'].get('ssl', False)

        app.settings['MONGODB_AUTH_MECHANISM'] = info['options'].get(
            'authmechanism', 'DEFAULT')

        # X.509
        app.settings['MONGODB_SSL_CERTFILE'] = info['options'].get(
            'ssl_certfile')
        app.settings['MONGODB_SSL_CA_CERTS'] = info['options'].get(
            'ssl_ca_certs')

        app.settings['MONGODB_REPLICA_SET'] = info['options'].get(
            'replicaset')
        app.settings['MONGODB_MAX_POOL_SIZE'] = info['options'].get(
            'max_pool_size')
        app.settings['MONGODB_CONNECT'] = info['options'].get(
            'auto_start_request', False)

        # Replica sets require both a different client class and a
        # different keyword argument name.
        if app.settings['MONGODB_REPLICA_SET']:
            kwargs['replicaSet'] = app.settings['MONGODB_REPLICA_SET']
            _class = AsyncIOMotorReplicaSetClient
        else:
            _class = AsyncIOMotorClient

        host = app.settings['MONGODB_URI']

        kwargs['ssl'] = app.settings['MONGODB_USE_SSL']

        kwargs['document_class'] = app.settings['MONGODB_DOCUMENT_CLASS']
        kwargs['max_pool_size'] = app.settings['MONGODB_MAX_POOL_SIZE']
        kwargs['tz_aware'] = app.settings['MONGODB_TIME_ZONE_AWARE']
        kwargs['_connect'] = app.settings['MONGODB_CONNECT']

        self._auth = {
            'name': app.settings['MONGODB_USERNAME'],
        }
        if self._auth['name']:
            self._auth['mechanism'] = app.settings['MONGODB_AUTH_MECHANISM']
            if app.settings['MONGODB_AUTH_MECHANISM'] == 'MONGODB-X509':
                kwargs['ssl_cert_reqs'] = ssl.CERT_REQUIRED
                kwargs['ssl_certfile'] = app.settings['MONGODB_SSL_CERTFILE']
                kwargs['ssl_ca_certs'] = app.settings['MONGODB_SSL_CA_CERTS']

                if not (kwargs['ssl_certfile'] and kwargs['ssl_ca_certs']):
                    raise ValueError(
                        'To use X.509, both the certificate file and the '
                        'certificate authority file must be specified.'
                    )
            else:
                # Otherwise use username and password authentication.
                self._auth['password'] = app.settings['MONGODB_PASSWORD']

        if any(self._auth.values()) and not all(self._auth.values()):
            # Make sure that if any authentication settings are
            # provided, all authentication settings are provided. This
            # should only apply to username and password authentication.
            # NOTE: The pymongo URI parser will raise
            # pymongo.errors.InvalidURI if the username is empty.
            raise ValueError(
                'Username and password must be specified together or '
                'not at all.'
            )

        self.client = _class(host, **kwargs)

        # If a database name was provided, store the name so that the
        # db property can be used.
        self._db = app.settings['MONGODB_DATABASE']

    @property
    def db(self):
        """Shortcut to the database object."""
        if isinstance(self._db, str):
            # Lazily load the database instance.
            self._db = self.client[self._db]

        if self._auth:
            # If authentication information has been provided, try to
            # use it.
            self._db.authenticate(**self._auth)

        return self._db
