"""Modèle de données pour une recette."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Recipe:
    """Représente une recette soumise par un utilisateur."""

    id: int | None
    author_id: int
    title: str
    description: str | None = None
    image_path: str | None = None
    servings: int | None = None
    prep_time_minutes: int | None = None
    status: str = "PENDING"
    validated_by: int | None = None
    validated_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    STATUS_PENDING = "PENDING"
    STATUS_CHANGES_REQUIRED = "CHANGES_REQUIRED"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    def is_approved(self) -> bool:
        """Indique si la recette a été approuvée."""
        return self.status == self.STATUS_APPROVED

    def is_pending(self) -> bool:
        """Indique si la recette est en attente de validation."""
        return self.status == self.STATUS_PENDING

    def is_rejected(self) -> bool:
        """Indique si la recette a été rejetée."""
        return self.status == self.STATUS_REJECTED

    @classmethod
    def from_row(cls, row: dict) -> Recipe:
        """Convertit une ligne de la base de données en une instance de Recipe."""
        return cls(
            id=row["id"],
            author_id=row["author_id"],
            title=row["title"],
            description=row.get("description"),
            image_path=row.get("image_path"),
            servings=row.get("servings"),
            prep_time_minutes=row.get("prep_time_minutes"),
            status=row.get("status", "PENDING"),
            validated_by=row.get("validated_by"),
            validated_at=row.get("validated_at"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<Recipe id={self.id} title={self.title!r} status={self.status}>"
