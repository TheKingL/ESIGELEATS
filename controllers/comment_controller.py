"""
Contrôleur des commentaires pour les recettes.

Ce module fournit des fonctionnalités pour récupérer et créer des commentaires
pour les recettes dans la base de données.
"""

from models.comment import Comment
from sql import SQL


def _row_to_comment(row: dict) -> Comment:
    return Comment.from_row(row)


class CommentController:
    """Contrôleur pour gérer les commentaires des recettes."""

    def __init__(self, db: SQL) -> None:
        self.db = db

    def get_comments(self, recipe_id: int) -> list[Comment]:
        """Récupère tous les commentaires pour une recette donnée."""
        query = """
            SELECT c.*, u.username, u.display_name, u.is_admin, u.is_profile_public FROM comments c
            JOIN users u ON u.id = c.user_id
            WHERE c.recipe_id = ?
            ORDER BY c.created_at ASC
        """
        rows = self.db.execute(query, recipe_id)
        return [_row_to_comment(r) for r in rows]

    def create_comment(self, recipe_id: int, user_id: int, content: str) -> Comment:
        """Crée un nouveau commentaire pour une recette."""
        self.db.execute(
            "INSERT INTO comments (recipe_id, user_id, content) VALUES (?, ?, ?)",
            recipe_id,
            user_id,
            content,
        )

        row = self.db.execute(
            """
            SELECT c.*, u.username, u.display_name, u.is_admin, u.is_profile_public FROM comments c
            JOIN users u ON u.id = c.user_id
            WHERE c.id = last_insert_rowid()
            """
        )[0]

        return _row_to_comment(row)
