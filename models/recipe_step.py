"""Modèle de données pour une étape de recette."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RecipeStep:
    """Représente une étape dans une recette."""

    id: int | None
    recipe_id: int
    step_number: int
    content: str
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_row(cls, row: dict) -> RecipeStep:
        """Convertit une ligne de la base de données en une instance de RecipeStep."""
        return cls(
            id=row["id"],
            recipe_id=row["recipe_id"],
            step_number=row["step_number"],
            content=row["content"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<RecipeStep id={self.id} recipe_id={self.recipe_id} step={self.step_number}>"
