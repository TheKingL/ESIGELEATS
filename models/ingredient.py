"""Modèle de données pour un ingrédient et un ingrédient de recette."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Ingredient:
    """Représente un ingrédient utilisé dans les recettes."""

    id: int | None
    name: str

    @classmethod
    def from_row(cls, row: dict) -> Ingredient:
        """Convertit une ligne de la base de données en une instance de Ingredient."""
        return cls(
            id=row["id"],
            name=row["name"],
        )

    def __repr__(self) -> str:
        return f"<Ingredient id={self.id} name={self.name!r}>"


@dataclass
class RecipeIngredient:
    """Représente un ingrédient spécifique dans une recette."""

    id: int | None
    recipe_id: int
    ingredient_id: int
    quantity: str | None = None
    ingredient_name: str | None = None

    @classmethod
    def from_row(cls, row: dict) -> RecipeIngredient:
        """Convertit une ligne de la base de données en une instance de RecipeIngredient."""
        return cls(
            id=row["id"],
            recipe_id=row["recipe_id"],
            ingredient_id=row["ingredient_id"],
            quantity=row.get("quantity"),
            ingredient_name=row.get("ingredient_name"),
        )

    def __repr__(self) -> str:
        return (
            f"<RecipeIngredient id={self.id} recipe_id={self.recipe_id} "
            f"ingredient_id={self.ingredient_id} quantity={self.quantity!r}>"
        )
