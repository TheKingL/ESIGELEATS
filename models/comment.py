"""Modèle de données pour un commentaire sur une recette."""

from dataclasses import dataclass


@dataclass
class Comment:
    """Représente un commentaire fait par un utilisateur sur une recette."""

    id: int
    recipe_id: int
    user_id: int
    content: str
    created_at: str

    # Meta infos de l'utilisateur qui a commenté
    username: str | None = None
    display_name: str | None = None
    is_admin: bool = False
    is_profile_public: bool = True

    @classmethod
    def from_row(cls, row: dict) -> "Comment":
        """Convertit une ligne de la base de données en une instance de Comment."""
        return cls(
            id=row["id"],
            recipe_id=row["recipe_id"],
            user_id=row["user_id"],
            content=row["content"],
            created_at=row["created_at"],
            username=row.get("username"),
            display_name=row.get("display_name"),
            is_admin=bool(row.get("is_admin", False)),
            is_profile_public=bool(row.get("is_profile_public", True)),
        )

    def __repr__(self) -> str:
        return (
            f"<Comment id={self.id} recipe_id={self.recipe_id} user_id={self.user_id} "
            f"content={self.content[:20]!r}...>"
        )
