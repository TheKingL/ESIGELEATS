"""Tests des routes de gestion des recettes (CRUD, Uploads, Ingrédients)."""

import io
from unittest.mock import MagicMock, patch


def test_create_recipe_page_access(logged_client, app):
    """Vérifie que la page de création s'affiche bien."""
    app.ingredient_controller = MagicMock()
    app.ingredient_controller.list_all.return_value = []

    response = logged_client.get("/recipes/create")

    assert response.status_code == 200
    assert b"Titre de la recette" in response.data


def test_create_recipe_submit_success_with_image(logged_client, app):
    """Test création valide avec upload d'image."""
    app.recipe_controller = MagicMock()
    app.ingredient_controller = MagicMock()
    app.user_controller = MagicMock()

    mock_user = MagicMock()
    mock_user.id = 1
    app.user_controller.get_by_id.return_value = mock_user

    data = {
        "title": "Recette Image",
        "servings": "4",
        "prep_time_minutes": "30",
        "ingredient_name[]": ["Riz"],
        "ingredient_quantity[]": ["100g"],
        "step_content[]": ["Cuire"],
        "image": (io.BytesIO(b"fake_image_content"), "photo.jpg"),
    }

    with (
        patch("routes.recipes.uuid4") as mock_uuid,
        patch("werkzeug.datastructures.FileStorage.save"),
    ):
        mock_uuid.return_value.hex = "fake_uuid"

        response = logged_client.post(
            "/recipes/create", data=data, content_type="multipart/form-data"
        )

    assert response.status_code == 302
    assert response.location == "/"

    assert app.recipe_controller.create_recipe.called
    created_recipe = app.recipe_controller.create_recipe.call_args[0][0]
    assert "uploads/recipes/fake_uuid.jpg" in created_recipe.image_path


def test_create_recipe_validation_errors(logged_client, app):
    """Vérifie le rejet des données invalides (titre vide, chiffres négatifs)."""
    app.recipe_controller = MagicMock()
    app.ingredient_controller = MagicMock()

    data = {
        "title": "",
        "servings": "-5",
        "prep_time_minutes": "dix",
    }

    response = logged_client.post("/recipes/create", data=data)

    assert response.status_code == 200
    assert b"Le titre de la recette est requis" in response.data
    assert b"entier positif" in response.data
    assert b"entier en minutes" in response.data
    assert b"Ajoutez au moins un ingr" in response.data


def test_create_recipe_invalid_image(logged_client, app):
    """Vérifie le rejet d'un format d'image non supporté."""
    app.ingredient_controller = MagicMock()
    app.user_controller = MagicMock()

    data = {
        "title": "Bonne recette",
        "servings": "2",
        "ingredient_name[]": ["Sel"],
        "ingredient_quantity[]": ["1"],
        "step_content[]": ["Manger"],
        # Fichier invalide (.exe)
        "image": (io.BytesIO(b"exe"), "virus.exe"),
    }

    response = logged_client.post("/recipes/create", data=data, content_type="multipart/form-data")

    assert response.status_code == 200


def test_edit_recipe_page_access(logged_client, app):
    """Accès à la page d'édition pour le propriétaire."""
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    mock_recipe.author_id = 1
    mock_recipe.title = "Ancien Titre"

    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = mock_recipe

    app.ingredient_controller = MagicMock()
    app.ingredient_controller.list_all.return_value = []
    app.ingredient_controller.get_ingredients_for_recipe.return_value = []

    app.recipe_controller.get_steps_for_recipe.return_value = []

    response = logged_client.get("/recipes/1/edit")

    assert response.status_code == 200
    assert b"Ancien Titre" in response.data


def test_edit_recipe_submit_success(logged_client, app):
    """Soumission valide du formulaire d'édition."""
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    mock_recipe.author_id = 1

    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = mock_recipe
    app.ingredient_controller = MagicMock()
    app.user_controller = MagicMock()

    data = {
        "title": "Nouveau Titre",
        "servings": "5",
        "prep_time_minutes": "45",
        "ingredient_name[]": ["Pomme"],
        "ingredient_quantity[]": ["2"],
        "step_content[]": ["Manger"],
    }

    response = logged_client.post("/recipes/1/edit", data=data)

    assert response.status_code == 302
    assert "/recipes/1" in response.location

    assert mock_recipe.title == "Nouveau Titre"
    assert mock_recipe.status == "PENDING"
    assert app.recipe_controller.update_recipe.called


def test_edit_recipe_forbidden(logged_client, app):
    """On ne peut pas éditer la recette du voisin."""
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    mock_recipe.author_id = 999

    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = mock_recipe

    response = logged_client.get("/recipes/1/edit")

    assert response.status_code == 302
    assert "/recipes/1" in response.location


def test_edit_recipe_not_found(logged_client, app):
    """Edition d'une recette qui n'existe pas."""
    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = None

    response = logged_client.get("/recipes/999/edit")
    assert response.status_code == 404


def test_delete_recipe_success_with_image(logged_client, app):
    """Suppression recette + suppression fichier image."""
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    mock_recipe.author_id = 1
    mock_recipe.image_path = "uploads/recipes/toto.jpg"

    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = mock_recipe
    app.user_controller = MagicMock()
    app.user_controller.get_by_id.return_value = MagicMock(id=1)

    with (
        patch("routes.recipes.os.path.exists", return_value=True),
        patch("routes.recipes.os.remove") as mock_remove,
    ):
        response = logged_client.post("/recipes/1/delete")

        assert response.status_code == 302
        assert response.location == "/"

        app.recipe_controller.delete_recipe.assert_called_with(1)
        assert mock_remove.called


def test_delete_recipe_forbidden(logged_client, app):
    """Interdit de supprimer la recette d'un autre."""
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    mock_recipe.author_id = 999

    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = mock_recipe

    response = logged_client.post("/recipes/1/delete")

    assert response.status_code == 302
    assert "/recipes/1" in response.location
    assert not app.recipe_controller.delete_recipe.called


def test_add_ingredient_admin_success(admin_client, app):
    """Admin ajoute un ingrédient."""
    app.ingredient_controller = MagicMock()
    app.ingredient_controller.search_by_name.return_value = None

    response = admin_client.post("/recipes/ingredients/add", data={"name": "Safran"})

    assert response.status_code == 302
    assert app.ingredient_controller.create_ingredient.called


def test_add_ingredient_duplicate(admin_client, app):
    """Erreur si ingrédient déjà existant."""
    app.ingredient_controller = MagicMock()
    app.ingredient_controller.search_by_name.return_value = True

    response = admin_client.post("/recipes/ingredients/add", data={"name": "Sel"})

    assert response.status_code == 200


def test_add_ingredient_forbidden(logged_client):
    """Utilisateur lambda ne peut pas ajouter d'ingrédient."""
    response = logged_client.get("/recipes/ingredients/add")
    assert response.status_code == 302
    assert "/recipes" in response.location
