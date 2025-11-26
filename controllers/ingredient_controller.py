"""
Contrôleur pour gérer les ingrédients dans l'application de recettes.

Ce module fournit des fonctionnalités pour créer, lire, mettre à jour et supprimer
des ingrédients, ainsi que pour gérer les ingrédients associés aux recettes.
"""

from __future__ import annotations

from collections.abc import Iterable

from models.ingredient import Ingredient, RecipeIngredient
from sql import SQL


def _row_to_ingredient(row: dict) -> Ingredient:
    """Convertit une ligne de la base de données en une instance d'Ingredient."""
    return Ingredient.from_row(row)


def _row_to_recipe_ingredient(row: dict) -> RecipeIngredient:
    """Convertit une ligne de la base de données en une instance de RecipeIngredient."""
    return RecipeIngredient.from_row(row)


class IngredientController:
    """Contrôleur pour gérer les opérations liées aux ingrédients."""

    def __init__(self, db: SQL) -> None:
        self.db = db

    def get_by_id(self, ingredient_id: int) -> Ingredient | None:
        """Récupère un ingrédient par son ID."""
        rows = self.db.execute("SELECT * FROM ingredients WHERE id = ?", ingredient_id)
        if not rows:
            return None
        return _row_to_ingredient(rows[0])

    def get_by_name(self, name: str) -> Ingredient | None:
        """Récupère un ingrédient par son nom."""
        rows = self.db.execute(
            "SELECT * FROM ingredients WHERE name = ?",
            name.strip(),
        )
        if not rows:
            return None
        return _row_to_ingredient(rows[0])

    def create_ingredient(self, name: str) -> Ingredient:
        """Crée un nouvel ingrédient avec le nom donné."""
        normalized = name.strip()
        self.db.execute(
            "INSERT INTO ingredients (name) VALUES (?)",
            normalized,
        )
        rows = self.db.execute("SELECT last_insert_rowid() AS id")
        ingredient_id = rows[0]["id"]
        return Ingredient(id=ingredient_id, name=normalized)

    def ensure_ingredient(self, name: str) -> Ingredient:
        """S'assure qu'un ingrédient avec le nom donné existe, le crée sinon."""
        normalized = name.strip()
        if not normalized:
            raise ValueError("Ingredient name cannot be empty")
        existing = self.get_by_name(normalized)
        if existing:
            return existing
        return self.create_ingredient(normalized)

    def search_by_name(self, term: str, *, limit: int = 10) -> list[Ingredient]:
        """Recherche des ingrédients par nom avec une correspondance partielle."""
        like = f"%{term.strip()}%"
        rows = self.db.execute(
            "SELECT * FROM ingredients WHERE name LIKE ? ORDER BY name LIMIT ?",
            like,
            limit,
        )
        return [_row_to_ingredient(row) for row in rows]

    def list_all(self) -> list[Ingredient]:
        """Liste tous les ingrédients triés par nom."""
        rows = self.db.execute("SELECT * FROM ingredients ORDER BY name")
        return [_row_to_ingredient(row) for row in rows]

    def get_ingredients_for_recipe(self, recipe_id: int) -> list[RecipeIngredient]:
        """Récupère tous les ingrédients associés à une recette donnée."""
        rows = self.db.execute(
            """
            SELECT ri.id, ri.recipe_id, ri.ingredient_id, ri.quantity, i.name AS ingredient_name FROM recipe_ingredients AS ri
            JOIN ingredients AS i ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
            ORDER BY ri.id
            """,
            recipe_id,
        )
        return [_row_to_recipe_ingredient(row) for row in rows]

    def replace_ingredients_for_recipe(
        self,
        recipe_id: int,
        ingredients: Iterable[tuple[str, str | None]],
    ) -> None:
        """Remplace les ingrédients associés à une recette donnée."""
        self.db.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", recipe_id)

        for name, quantity in ingredients:
            normalized_name = (name or "").strip()
            if not normalized_name:
                continue

            ingredient = self.ensure_ingredient(normalized_name)
            self.db.execute(
                """
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity)
                VALUES (?, ?, ?)
                """,
                recipe_id,
                ingredient.id,
                quantity.strip() if quantity else None,
            )

    def find_recipe_ids_by_ingredient_name(self, term: str) -> list[int]:
        """Trouve les IDs de recettes contenant des ingrédients correspondant au terme donné."""
        like = f"%{term.strip()}%"
        rows = self.db.execute(
            """
            SELECT DISTINCT ri.recipe_id FROM recipe_ingredients AS ri
            JOIN ingredients AS i ON i.id = ri.ingredient_id
            WHERE i.name LIKE ?
            """,
            like,
        )
        return [row["recipe_id"] for row in rows]
