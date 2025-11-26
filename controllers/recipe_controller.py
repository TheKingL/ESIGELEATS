"""
Contrôleur pour la gestion des recettes.

Ce module fournit des fonctionnalités pour créer, lire, mettre à jour et supprimer
des recettes, ainsi que pour gérer les étapes des recettes et récupérer des listes
de recettes basées sur divers critères.
"""

from __future__ import annotations

from collections.abc import Iterable

from models.recipe import Recipe
from models.recipe_step import RecipeStep
from sql import SQL


def _row_to_recipe(row: dict) -> Recipe:
    """Convertit une ligne de la base de données en une instance de Recipe."""
    return Recipe.from_row(row)


def _row_to_step(row: dict) -> RecipeStep:
    """Convertit une ligne de la base de données en une instance de RecipeStep."""
    return RecipeStep.from_row(row)


class RecipeController:
    """Contrôleur pour la gestion des recettes."""

    def __init__(self, db: SQL) -> None:
        self.db = db

    def get_by_id(self, recipe_id: int) -> Recipe | None:
        """Récupère une recette par son ID."""
        rows = self.db.execute("SELECT * FROM recipes WHERE id = ?", recipe_id)
        if not rows:
            return None
        return _row_to_recipe(rows[0])

    def list_public(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> list[Recipe]:
        """Liste les recettes publiques avec pagination et recherche optionnelle."""
        params: list = [Recipe.STATUS_APPROVED]
        query = "SELECT * FROM recipes WHERE status = ?"
        if search:
            query += " AND (title LIKE ? OR description LIKE ?)"
            like = f"%{search}%"
            params.extend([like, like])
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        rows = self.db.execute(query, *params)
        return [_row_to_recipe(row) for row in rows]

    def list_by_author(
        self,
        author_id: int,
        *,
        include_all_statuses: bool = True,
        status: str | None = None,
    ) -> list[Recipe]:
        """Liste les recettes d'un auteur avec filtrage par statut optionnel."""
        params: list = [author_id]
        query = "SELECT * FROM recipes WHERE author_id = ?"
        if not include_all_statuses and status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC"
        rows = self.db.execute(query, *params)
        return [_row_to_recipe(row) for row in rows]

    def create_recipe(self, recipe: Recipe) -> int:
        """Crée une nouvelle recette et retourne son ID."""
        self.db.execute(
            """
            INSERT INTO recipes (
                author_id,
                title,
                description,
                image_path,
                servings,
                prep_time_minutes,
                status,
                validated_by,
                validated_at,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            recipe.author_id,
            recipe.title,
            recipe.description,
            recipe.image_path,
            recipe.servings,
            recipe.prep_time_minutes,
            recipe.status,
            recipe.validated_by,
            recipe.validated_at,
        )
        rows = self.db.execute("SELECT last_insert_rowid() AS id")
        new_id = rows[0]["id"]
        recipe.id = new_id
        return new_id

    def update_recipe(self, recipe: Recipe) -> None:
        """Met à jour une recette existante."""
        self.db.execute(
            """
            UPDATE recipes SET
                title = ?,
                description = ?,
                image_path = ?,
                servings = ?,
                prep_time_minutes = ?,
                status = ?,
                validated_by = ?,
                validated_at = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            recipe.title,
            recipe.description,
            recipe.image_path,
            recipe.servings,
            recipe.prep_time_minutes,
            recipe.status,
            recipe.validated_by,
            recipe.validated_at,
            recipe.id,
        )

    def update_status(
        self,
        recipe_id: int,
        status: str,
        *,
        validated_by: int | None = None,
    ) -> None:
        """Met à jour le statut d'une recette."""
        if status in (
            Recipe.STATUS_APPROVED,
            Recipe.STATUS_REJECTED,
            Recipe.STATUS_CHANGES_REQUIRED,
        ):
            self.db.execute(
                """
                UPDATE recipes SET
                    status = ?,
                    validated_by = ?,
                    validated_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                status,
                validated_by,
                recipe_id,
            )
        else:
            self.db.execute(
                """
                UPDATE recipes SET
                    status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                status,
                recipe_id,
            )

    def delete_recipe(self, recipe_id: int) -> None:
        """Supprime une recette par son ID."""
        self.db.execute("DELETE FROM recipes WHERE id = ?", recipe_id)

    def get_average_rating(self, recipe_id: int) -> float | None:
        """Récupère la note moyenne d'une recette."""
        rows = self.db.execute(
            "SELECT AVG(rating) AS avg_rating FROM ratings WHERE recipe_id = ?",
            recipe_id,
        )
        if not rows:
            return None
        avg = rows[0]["avg_rating"]
        return float(avg) if avg is not None else None

    def get_steps_for_recipe(self, recipe_id: int) -> list[RecipeStep]:
        """Récupère les étapes d'une recette par son ID."""
        rows = self.db.execute(
            """
            SELECT * FROM recipe_steps
            WHERE recipe_id = ?
            ORDER BY step_number ASC
            """,
            recipe_id,
        )
        return [_row_to_step(row) for row in rows]

    def replace_steps_for_recipe(
        self,
        recipe_id: int,
        contents: Iterable[str],
    ) -> None:
        """Remplace les étapes d'une recette par un nouvel ensemble d'étapes."""
        self.db.execute("DELETE FROM recipe_steps WHERE recipe_id = ?", recipe_id)

        step_number = 1
        for raw in contents:
            content = (raw or "").strip()
            if not content:
                continue
            self.db.execute(
                """
                INSERT INTO recipe_steps (recipe_id, step_number, content)
                VALUES (?, ?, ?)
                """,
                recipe_id,
                step_number,
                content,
            )
            step_number += 1

    def get_favorite_recipes_for_user(self, user_id: int):
        """Récupère les recettes favorites d'un utilisateur."""
        query = """
            SELECT r.*, 
                   AVG(rt.rating) AS average_rating,
                   COUNT(rt.rating) AS rating_count,
                   fav.created_at AS favorite_date
            FROM favorites fav
            JOIN recipes r ON r.id = fav.recipe_id
            LEFT JOIN ratings rt ON rt.recipe_id = r.id
            WHERE fav.user_id = ?
            GROUP BY r.id
            ORDER BY fav.created_at DESC
        """
        rows = self.db.execute(query, user_id)

        favorites = []
        for row in rows:
            recipe = _row_to_recipe(row)
            recipe.average_rating = float(row["average_rating"]) if row["average_rating"] else None
            recipe.rating_count = row["rating_count"]
            recipe.favorite_date = row["favorite_date"]
            favorites.append(recipe)
        return favorites

    def get_rated_recipes_for_user(self, user_id):
        """Récupère les recettes notées par un utilisateur."""
        query = """
            SELECT 
                r.*,
                ur.rating AS user_rating,
                ur.created_at AS rating_date,
                AVG(rt.rating) AS average_rating
            FROM ratings ur
            JOIN recipes r ON r.id = ur.recipe_id
            LEFT JOIN ratings rt ON rt.recipe_id = r.id
            WHERE ur.user_id = ?
            GROUP BY r.id
            ORDER BY ur.created_at DESC;
        """

        rows = self.db.execute(query, user_id)

        recipes = []
        for row in rows:
            rec = _row_to_recipe(row)
            rec.user_rating = row["user_rating"]
            rec.rating_date = row["rating_date"]
            rec.average_rating = float(row["average_rating"]) if row["average_rating"] else None
            recipes.append(rec)

        return recipes
