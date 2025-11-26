"""
Contrôleur pour la gestion des opérations liées aux utilisateurs dans la base de données.

Ce module fournit des fonctionnalités pour créer, lire, mettre à jour et supprimer
des utilisateurs, ainsi que pour récupérer des listes d'utilisateurs.
"""

from models.user import User
from sql import SQL


def _row_to_user(row: dict) -> User:
    """Convertit une ligne de la base de données en une instance de User."""
    return User.from_row(row)


class UserController:
    """Contrôleur pour la gestion des utilisateurs."""

    def __init__(self, db: SQL) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        """Récupère un utilisateur par son ID."""
        rows = self.db.execute("SELECT * FROM users WHERE id = ?", user_id)
        if not rows:
            return None

        row = rows[0]
        return _row_to_user(row)

    def get_by_username(self, username: str) -> User | None:
        """Récupère un utilisateur par son nom d'utilisateur."""
        rows = self.db.execute(
            "SELECT * FROM users WHERE username = ?",
            username,
        )
        if not rows:
            return None

        row = rows[0]
        return _row_to_user(row)

    def create_user(self, user: User) -> int:
        """Crée un nouvel utilisateur dans la base de données."""
        self.db.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                display_name,
                bio,
                is_admin,
                is_profile_public,
                last_login,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
            user.username,
            user.password_hash,
            user.display_name,
            user.bio,
            int(user.is_admin),
            int(user.is_profile_public),
            user.last_login,
        )

        rows = self.db.execute("SELECT last_insert_rowid() AS id")
        new_id = rows[0]["id"]
        user.id = new_id
        return new_id

    def update_user(self, user: User) -> None:
        """Met à jour un utilisateur existant dans la base de données."""
        self.db.execute(
            """
            UPDATE users SET
                username = ?,
                display_name = ?,
                bio = ?,
                is_profile_public = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            user.username,
            user.display_name,
            user.bio,
            int(user.is_profile_public),
            user.id,
        )

    def update_user_password(self, user: User) -> None:
        """Met à jour le mot de passe d'un utilisateur existant dans la base de données."""
        self.db.execute(
            """
            UPDATE users SET
                password_hash = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            user.password_hash,
            user.id,
        )

    def delete_user(self, user_id: int):
        """Supprime un utilisateur de la base de données par son ID."""
        self.db.execute("DELETE FROM users WHERE id = ?", user_id)

    def list_all(self) -> list[User]:
        """Récupère une liste de tous les utilisateurs, triés par nom d'affichage ou nom d'utilisateur."""
        rows = self.db.execute(
            """
            SELECT *
            FROM users
            ORDER BY
              CASE
                WHEN display_name IS NULL OR TRIM(display_name) = '' THEN 1
                ELSE 0
              END,
              LOWER(COALESCE(display_name, username))
            """
        )
        return [_row_to_user(row) for row in rows]
