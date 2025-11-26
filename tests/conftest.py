"""Test de la configuration pour les tests Flask."""

import pytest

from app import app as flask_app


@pytest.fixture
def app():
    """Fixture pour l'application Flask en mode test."""
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="cle_secrete_pour_les_tests_bang_bang",
        SESSION_COOKIE_DOMAIN=None,
    )
    yield flask_app


@pytest.fixture
def client(app):
    """Fixture pour le client de test Flask."""
    return app.test_client()


@pytest.fixture
def logged_client(app, client):
    """Fixture pour un client de test connecté."""
    with client.session_transaction() as sess:
        sess["user"] = {
            "id": 1,
            "username": "testuser",
            "is_admin": False,
        }
    return client


@pytest.fixture
def admin_client(app, client):
    """Fixture pour un client de test connecté en tant qu'administrateur."""
    with client.session_transaction() as sess:
        sess["user"] = {
            "id": 999,
            "username": "admin",
            "is_admin": True,
        }
    return client
