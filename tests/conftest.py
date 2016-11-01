"""Test configuration."""

from henson import Application
import pytest


@pytest.fixture
def test_app(monkeypatch):
    """Return a test application."""
    app = Application('testing')

    monkeypatch.setitem(
        app.settings, 'MONGODB_URI', 'mongodb://localhost/testing')

    return app
