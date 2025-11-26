"""Tests des routes du panneau d'administration."""

from unittest.mock import MagicMock


def test_admin_access_control(client, logged_client):
    """Vérifie que l'accès est refusé aux anonymes et aux utilisateurs non-admins."""
    response = client.get("/admin/")
    assert response.status_code != 200

    response = logged_client.get("/admin/")
    assert response.status_code == 302


def test_admin_users_list(admin_client, app):
    """Test de la liste des utilisateurs."""
    app.user_controller = MagicMock()

    # Simulation d'une liste d'utilisateurs
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "utilisateur_test"
    mock_user.display_name = "Test Man"
    mock_user.email = "test@example.com"
    mock_user.is_admin = False

    app.user_controller.list_all.return_value = [mock_user]

    response = admin_client.get("/admin/users-list")

    assert response.status_code == 200
    assert b"utilisateur_test" in response.data


def test_admin_recipes_list(admin_client, app):
    """Test du listing complet des recettes pour admin."""
    app.recipe_controller = MagicMock()

    mock_rows = [
        {
            "id": 1,
            "title": "Recette Admin Test",
            "description": "Description test",
            "status": "APPROVED",
            "image_path": "img.jpg",
            "servings": 4,
            "prep_time_minutes": 30,
            "created_at": "2024-01-01",
            "author_display_name": "Chef",
            "author_username": "chef",
            "average_rating": 4.5,
            "rating_count": 10,
            "favorites_count": 5,
        }
    ]

    app.recipe_controller.db.execute.return_value = mock_rows

    response = admin_client.get("/admin/recipes")

    assert response.status_code == 200
    assert b"Recette Admin Test" in response.data


def test_admin_recipes_validation_page(admin_client):
    """Test de l'accès à la page de validation (structure seulement)."""
    response = admin_client.get("/admin/recipes-list/validation")
    assert response.status_code == 200


def test_admin_insights_page(admin_client):
    """Test de l'accès à la page des statistiques."""
    response = admin_client.get("/admin/insights")
    assert response.status_code == 200
