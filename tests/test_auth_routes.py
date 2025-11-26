"""Tests complets des routes d'authentification (Pages & Actions)."""

from unittest.mock import MagicMock


def test_login_page(client):
    """Test de l'affichage de la page de connexion."""
    resp = client.get("/login")
    assert resp.status_code == 200


def test_register_page(client):
    """Test de l'affichage de la page d'inscription."""
    resp = client.get("/register")
    assert resp.status_code == 200


def test_login_submit_success(client, app):
    """Test d'une connexion réussie."""
    app.user_controller = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "testuser"
    mock_user.check_password.return_value = True
    mock_user.to_session.return_value = {"id": 1, "username": "testuser"}

    app.user_controller.get_by_username.return_value = mock_user

    response = client.post("/login", data={"username": "testuser", "password": "Password123!"})

    assert response.status_code == 302
    assert response.location == "/"

    with client.session_transaction() as sess:
        assert sess["user"]["username"] == "testuser"


def test_login_submit_fail_wrong_password(client, app):
    """Test d'une connexion avec mauvais mot de passe."""
    app.user_controller = MagicMock()

    mock_user = MagicMock()
    mock_user.check_password.return_value = False

    app.user_controller.get_by_username.return_value = mock_user

    response = client.post(
        "/login", data={"username": "testuser", "password": "WrongPassword"}, follow_redirects=True
    )

    assert response.status_code == 200


def test_login_submit_fail_user_not_found(client, app):
    """Test d'une connexion avec utilisateur inconnu."""
    app.user_controller = MagicMock()
    app.user_controller.get_by_username.return_value = None

    response = client.post(
        "/login", data={"username": "ghost", "password": "pwd"}, follow_redirects=True
    )

    assert response.status_code == 200


def test_register_submit_success(client, app):
    """Test d'une inscription réussie."""
    app.user_controller = MagicMock()
    app.user_controller.get_by_username.return_value = None

    data = {
        "username": "newuser",
        "display_name": "New User",
        "password": "Password123!",
        "password_confirm": "Password123!",
    }

    response = client.post("/register", data=data)

    assert response.status_code == 302
    assert response.location == "/"
    assert app.user_controller.create_user.called


def test_logout(logged_client):
    """Test de la déconnexion."""
    with logged_client.session_transaction() as sess:
        assert "user" in sess

    response = logged_client.get("/logout", follow_redirects=False)

    assert response.status_code == 302
    assert response.location == "/login"

    with logged_client.session_transaction() as sess:
        assert "user" not in sess
