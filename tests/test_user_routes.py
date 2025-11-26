"""Tests des routes de gestion des utilisateurs (profil, édition, suppression)."""

from unittest.mock import MagicMock


def test_user_profile_public_success(logged_client, app):
    """Vérifie qu'un utilisateur peut voir un profil public."""
    app.user_controller = MagicMock()

    mock_row = {
        "id": 2,
        "username": "public_user",
        "password_hash": "hash",
        "display_name": "Public Man",
        "bio": "Coucou",
        "is_admin": 0,
        "is_profile_public": 1,
        "last_login": "2024-01-01",
        "created_at": "2024-01-01",
        "updated_at": None,
    }
    app.user_controller.db.execute.return_value = [mock_row]

    response = logged_client.get("/users/2")

    assert response.status_code == 200
    assert b"Public Man" in response.data


def test_user_profile_private_forbidden(logged_client, app):
    """Vérifie qu'un utilisateur standard ne peut pas voir un profil privé tiers."""
    app.user_controller = MagicMock()

    mock_row = {
        "id": 2,
        "username": "private_user",
        "password_hash": "hash",
        "display_name": "Private Man",
        "bio": "Secret",
        "is_admin": 0,
        "is_profile_public": 0,
        "last_login": None,
        "created_at": None,
        "updated_at": None,
    }
    app.user_controller.db.execute.return_value = [mock_row]

    response = logged_client.get("/users/2")

    assert response.status_code == 403


def test_user_profile_private_access_admin(admin_client, app):
    """Vérifie qu'un admin peut voir n'importe quel profil privé."""
    app.user_controller = MagicMock()

    mock_row = {
        "id": 2,
        "username": "private_user",
        "password_hash": "hash",
        "display_name": "Private Man",
        "bio": "Secret",
        "is_admin": 0,
        "is_profile_public": 0,
        "last_login": None,
        "created_at": None,
        "updated_at": None,
    }
    app.user_controller.db.execute.return_value = [mock_row]

    response = admin_client.get("/users/2")

    assert response.status_code == 200
    assert b"Private Man" in response.data


def test_edit_profile_access_denied(logged_client):
    """Vérifie qu'on ne peut pas accéder à la page d'édition d'un autre utilisateur."""
    response = logged_client.get("/users/2/edit")

    assert response.status_code == 302
    assert "/users/2" in response.location


def test_edit_profile_submit_success(logged_client, app):
    """Test de la mise à jour de son propre profil."""
    app.user_controller = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "mon_user"
    mock_user.to_session.return_value = {"id": 1, "username": "nouveau_nom"}

    app.user_controller.get_by_id.return_value = mock_user
    app.user_controller.get_by_username.return_value = None

    data = {
        "username": "nouveau_nom",
        "display_name": "Nouveau Nom",
        "bio": "Nouvelle bio",
        "is_profile_public": "on",
    }

    response = logged_client.post("/users/1/edit", data=data)

    assert response.status_code == 302
    assert "/users/1" in response.location
    assert app.user_controller.update_user.called


def test_delete_user_self_success(logged_client, app):
    """Un utilisateur peut supprimer son propre compte."""
    app.user_controller = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    app.user_controller.get_by_id.return_value = mock_user

    response = logged_client.post("/users/1/delete")

    assert response.status_code == 302
    assert response.location == "/"
    app.user_controller.delete_user.assert_called_with(1)


def test_delete_user_malicious_attempt(logged_client, app):
    """Un utilisateur ne PEUT PAS supprimer le compte d'un autre (Hacker check)."""
    app.user_controller = MagicMock()

    mock_victim = MagicMock()
    mock_victim.id = 2
    app.user_controller.get_by_id.return_value = mock_victim

    response = logged_client.post("/users/2/delete")

    assert response.status_code == 302
    assert "/users/2" in response.location

    app.user_controller.delete_user.assert_not_called()


def test_delete_user_as_admin(admin_client, app):
    """Un administrateur peut supprimer n'importe quel compte."""
    app.user_controller = MagicMock()

    mock_victim = MagicMock()
    mock_victim.id = 2
    app.user_controller.get_by_id.return_value = mock_victim

    response = admin_client.post("/users/2/delete")

    assert response.status_code == 302
    app.user_controller.delete_user.assert_called_with(2)


def test_user_not_found(logged_client, app):
    """Vérifie la gestion 404 si l'utilisateur n'existe pas."""
    app.user_controller = MagicMock()

    app.user_controller.db.execute.return_value = []
    app.user_controller.get_by_id.return_value = None

    assert logged_client.get("/users/999").status_code == 404
    assert logged_client.post("/users/999/delete").status_code == 404


def test_edit_password_success(logged_client, app):
    """Test changement de mot de passe réussi."""
    app.user_controller = MagicMock()
    mock_user = MagicMock()
    mock_user.id = 1
    app.user_controller.get_by_id.return_value = mock_user

    data = {"password": "NewPassword123!", "password_confirm": "NewPassword123!"}

    response = logged_client.post("/users/1/password", data=data)

    assert response.status_code == 302
    assert "/users/1" in response.location
    assert mock_user.hash_and_set_password.called
    assert app.user_controller.update_user_password.called


def test_edit_password_mismatch(logged_client, app):
    """Test erreur si les mots de passe ne correspondent pas."""
    app.user_controller = MagicMock()
    mock_user = MagicMock()
    mock_user.id = 1
    app.user_controller.get_by_id.return_value = mock_user

    data = {"password": "NewPassword123!", "password_confirm": "PasLeMeme!"}

    response = logged_client.post("/users/1/password", data=data)

    assert response.status_code == 200
    assert b"ne correspondent pas" in response.data


def test_edit_password_weak(logged_client, app):
    """Test erreur mot de passe trop faible."""
    app.user_controller = MagicMock()
    app.user_controller.get_by_id.return_value = MagicMock()

    data = {"password": "faible", "password_confirm": "faible"}

    response = logged_client.post("/users/1/password", data=data)

    assert response.status_code == 200
    assert b"doit contenir au moins" in response.data


def test_edit_profile_username_taken(logged_client, app):
    """Test erreur si on prend un pseudo déjà pris."""
    app.user_controller = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "moi"
    app.user_controller.get_by_id.return_value = mock_user

    app.user_controller.get_by_username.return_value = MagicMock()

    response = logged_client.post(
        "/users/1/edit", data={"username": "pris", "display_name": "Test", "bio": "Bio"}
    )

    assert response.status_code == 200
    assert b"d\xc3\xa9j\xc3\xa0 utilis\xc3\xa9" in response.data


def test_user_sub_pages(logged_client, app):
    """Test simple d'accès aux pages recettes, favoris, notées."""
    app.user_controller = MagicMock()
    app.recipe_controller = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.is_profile_public = True
    app.user_controller.get_by_id.return_value = mock_user

    app.recipe_controller.get_favorite_recipes_for_user.return_value = []

    # Test Recettes
    assert logged_client.get("/users/1/recipes").status_code == 200

    # Test Favoris
    assert logged_client.get("/users/1/favorites").status_code == 200

    # Test Notes
    assert logged_client.get("/users/1/rated").status_code == 200
