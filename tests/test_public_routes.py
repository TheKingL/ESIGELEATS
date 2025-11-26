"""Tests des routes publiques (Accueil, Affichage Recettes)."""

from unittest.mock import MagicMock


def test_home_page(client):
    """Test de la page d'accueil."""
    resp = client.get("/")
    assert resp.status_code == 200


def test_list_recipes(client, app):
    """Test de la liste des recettes."""
    response = client.get("/recipes/")
    assert response.status_code == 200


def test_view_recipe_success(client, app):
    """Test de l'affichage d'une recette qui existe."""
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    mock_recipe.title = "Pates Carbonara Test"
    mock_recipe.author_id = 99

    mock_recipe.servings = 2
    mock_recipe.prep_time_minutes = 15
    mock_recipe.description = "Une description de test"
    mock_recipe.image_path = None
    mock_recipe.status = "APPROVED"
    mock_recipe.created_at = "2024-01-01"

    mock_author = MagicMock()
    mock_author.username = "Chef_Gazo"
    mock_author.display_name = "Le Vrai Chef"

    app.recipe_controller = MagicMock()
    app.user_controller = MagicMock()
    app.ingredient_controller = MagicMock()

    app.recipe_controller.get_by_id.return_value = mock_recipe
    app.recipe_controller.get_steps_for_recipe.return_value = [
        {"step_number": 1, "content": "Cuire les pates"},
        {"step_number": 2, "content": "Manger"},
    ]
    app.recipe_controller.get_average_rating.return_value = 4.5

    app.recipe_controller.db.execute.side_effect = [[{"c": 10}], [], []]

    app.user_controller.get_by_id.return_value = mock_author
    app.ingredient_controller.get_ingredients_for_recipe.return_value = []

    response = client.get("/recipes/1")

    assert response.status_code == 200
    assert b"Pates Carbonara Test" in response.data


def test_view_recipe_404(client, app):
    """Test de l'affichage d'une recette qui n'existe pas."""
    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = None

    response = client.get("/recipes/9999")
    assert response.status_code == 404
