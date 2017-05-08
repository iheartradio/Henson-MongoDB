"""Test the configuration settings."""

import pytest

from henson_mongodb import MongoDB


def test_database(test_app):
    """Test that the db attribute is enabled."""
    test_app.settings['MONGODB_URI'] = 'mongodb://testing:pw@localhost/testing'
    mongo = MongoDB(test_app)

    assert mongo.db


def test_no_database_valueerror(test_app):
    """Test that ValueError is raised if no database is specified."""
    test_app.settings['MONGODB_URI'] = 'mongodb://localhost'

    with pytest.raises(ValueError):
        MongoDB(test_app)


def test_password_no_username_valueerror(test_app):
    """Test that only password and not username raises ValueError."""
    test_app.settings['MONGODB_URI'] = 'mongodb://testing@localhost/testing'

    with pytest.raises(ValueError):
        MongoDB(test_app)


def test_replica_set(test_app):
    """Test that replica sets get set correctly."""
    test_app.settings['MONGODB_URI'] = (
        'mongodb://testing:testing@localhost/testing?replicaSet=testing-rs'
    )
    mongo = MongoDB(test_app)

    mongo.client.delegate['_topology_settings._replica_set_name'] == 'testing-rs'
