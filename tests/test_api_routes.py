"""Tests des endpoints API (Notation, Favoris, Stats, Admin)."""

from unittest.mock import MagicMock


def test_rate_recipe_add_success(logged_client, app):
    """Vérifie l'ajout d'une nouvelle note."""
    app.recipe_controller = MagicMock()

    # On simule une recette existante
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    app.recipe_controller.get_by_id.return_value = mock_recipe

    # On simule qu'il n'y a pas encore de note (liste vide)
    app.recipe_controller.db.execute.return_value = []

    # On simule la nouvelle moyenne après ajout
    app.recipe_controller.get_average_rating.return_value = 4.5

    response = logged_client.post("/api/recipes/1/rate", json={"rating": 5})

    assert response.status_code == 200
    assert response.json["status"] == "added"
    assert response.json["average_rating"] == 4.5


def test_rate_recipe_toggle_remove(logged_client, app):
    """Si on remet la même note, ça doit la supprimer (toggle)."""
    app.recipe_controller = MagicMock()
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    app.recipe_controller.get_by_id.return_value = mock_recipe

    app.recipe_controller.db.execute.return_value = [{"rating": 5}]

    app.recipe_controller.get_average_rating.return_value = 4.0

    response = logged_client.post("/api/recipes/1/rate", json={"rating": 5})

    assert response.status_code == 200
    assert response.json["status"] == "removed"


def test_rate_recipe_update(logged_client, app):
    """Si on met une note différente, ça doit update."""
    app.recipe_controller = MagicMock()
    mock_recipe = MagicMock()
    mock_recipe.id = 1
    app.recipe_controller.get_by_id.return_value = mock_recipe

    app.recipe_controller.db.execute.return_value = [{"rating": 3}]

    app.recipe_controller.get_average_rating.return_value = 4.8

    response = logged_client.post("/api/recipes/1/rate", json={"rating": 5})

    assert response.status_code == 200
    assert response.json["status"] == "updated"


def test_rate_recipe_invalid_input(logged_client, app):
    """Vérifie qu'on ne peut pas mettre des notes pées (0, 6, string...)."""
    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = MagicMock()

    res = logged_client.post("/api/recipes/1/rate", json={"rating": 6})
    assert res.status_code == 400

    res = logged_client.post("/api/recipes/1/rate", json={"rating": "cinq"})
    assert res.status_code == 400


def test_toggle_favorite(logged_client, app):
    """Test l'ajout et la suppression de favoris."""
    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = MagicMock()

    app.recipe_controller.db.execute.return_value = []
    res = logged_client.post("/api/recipes/1/favorite")
    assert res.json["status"] == "added"

    app.recipe_controller.db.execute.return_value = [{"found": 1}]
    res = logged_client.post("/api/recipes/1/favorite")
    assert res.json["status"] == "removed"


def test_get_user_recipes_private_forbidden(logged_client, app):
    """Un user lambda ne doit pas voir les recettes d'un profil privé."""
    app.user_controller = MagicMock()

    mock_target_user = MagicMock()
    mock_target_user.id = 2
    mock_target_user.is_profile_public = False  # Profil privé
    app.user_controller.get_by_id.return_value = mock_target_user

    response = logged_client.get("/api/users/2/recipes")

    assert response.status_code == 403
    assert response.json["error"] == "forbidden"


def test_get_user_recipes_public_success(client, app):
    """Test de récupération des recettes d'un user public."""
    app.user_controller = MagicMock()
    app.recipe_controller = MagicMock()

    mock_target_user = MagicMock()
    mock_target_user.id = 2
    mock_target_user.is_profile_public = True
    app.user_controller.get_by_id.return_value = mock_target_user

    mock_rows = [
        {
            "id": 10,
            "title": "Pizza",
            "description": "Miam",
            "image_path": "img.jpg",
            "created_at": "2024",
            "prep_time_minutes": 10,
            "servings": 2,
            "status": "APPROVED",
            "author_username": "Mario",
            "author_display_name": "Super Mario",
            "average_rating": 5.0,
            "rating_count": 1,
            "user_rating": None,
            "is_favorite": 0,
        }
    ]
    app.recipe_controller.db.execute.return_value = mock_rows

    response = client.get("/api/users/2/recipes")

    assert response.status_code == 200
    assert len(response.json["recipes"]) == 1
    assert response.json["recipes"][0]["title"] == "Pizza"


def test_admin_update_status_success(admin_client, app):
    """Vérifie qu'un admin peut valider une recette."""
    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = MagicMock()

    data = {"status": "APPROVED"}
    response = admin_client.post("/api/admin/recipes/1/status", json=data)

    assert response.status_code == 200
    assert response.json["new_status"] == "APPROVED"
    assert app.recipe_controller.update_status.called


def test_admin_update_status_invalid(admin_client, app):
    """Vérifie qu'on ne peut pas mettre un statut bidon."""
    app.recipe_controller = MagicMock()
    app.recipe_controller.get_by_id.return_value = MagicMock()

    data = {"status": "NIMPORTEQUOI"}
    response = admin_client.post("/api/admin/recipes/1/status", json=data)

    assert response.status_code == 400


def test_admin_stats_overview(admin_client, app):
    """
    Le test ultime : le dashboard admin.
    Il faut mocker la séquence exacte des appels SQL.
    """
    app.recipe_controller = MagicMock()

    app.recipe_controller.db.execute.side_effect = [
        [{"c": 100}],  # Users
        [{"c": 50}],  # Recipes
        [{"c": 5}],  # Pending
        [{"c": 2}],  # Changes
        [{"c": 1}],  # Rejected
        [{"c": 200}],  # Favs
        [{"c": 300}],  # Ratings
        [{"c": 50}],  # Comments
        [{"status": "APPROVED", "c": 42}, {"status": "PENDING", "c": 5}],  # Status breakdown
        [{"d": "2024-01-01", "c": 2}],  # Created timeline
        [{"d": "2024-01-02", "c": 1}],  # Approved timeline
        [{"rating": 5, "c": 10}],  # Rating dist
        [{"id": 1, "username": "Chef", "display_name": "Chef", "recipe_count": 10}],  # Top authors
        [{"id": 1, "title": "Best", "fav_count": 5, "comment_count": 2}],  # Top recipes
    ]

    response = admin_client.get("/api/admin/stats/overview")

    assert response.status_code == 200
    data = response.json

    assert data["kpis"]["total_users"] == 100
    assert data["kpis"]["rejected_recipes"] == 1
    assert len(data["top_authors"]) == 1
    assert data["top_recipes_engagement"][0]["title"] == "Best"


def test_add_comment_success(logged_client, app):
    """Test l'ajout d'un commentaire."""
    app.recipe_controller = MagicMock()
    app.comment_controller = MagicMock()

    app.recipe_controller.get_by_id.return_value = MagicMock()

    mock_comment = MagicMock()
    mock_comment.id = 1
    mock_comment.content = "Super"
    mock_comment.created_at = "2024-01-01 12:00:00"
    mock_comment.recipe_id = 1

    mock_comment.user_id = 1
    mock_comment.username = "testuser"
    mock_comment.display_name = "Test User"
    mock_comment.is_admin = False
    mock_comment.is_profile_public = True

    app.comment_controller.create_comment.return_value = mock_comment

    res = logged_client.post("/api/recipes/1/comments", json={"content": "Super"})

    assert res.status_code == 201
    assert res.json["content"] == "Super"
    assert res.json["user"]["username"] == "testuser"


def test_add_comment_empty(logged_client):
    """On ne doit pas pouvoir poster un commentaire vide."""
    res = logged_client.post("/api/recipes/1/comments", json={"content": "   "})
    assert res.status_code == 400
