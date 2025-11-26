"""Modèle de données pour un utilisateur."""

from werkzeug.security import check_password_hash, generate_password_hash


class User:
    """Représente un utilisateur du système."""

    def __init__(
        self,
        username: str,
        password_hash: str,
        *,
        id_user: int | None = None,
        display_name: str | None = None,
        bio: str | None = None,
        is_admin: int | bool = False,
        is_profile_public: int | bool = True,
        last_login=None,
        created_at=None,
        updated_at=None,
    ) -> None:
        self.id = id_user
        self.username = username
        self.login = username
        self.password_hash = password_hash
        self.display_name = display_name
        self.bio = bio
        self.is_admin = bool(is_admin)
        self.is_profile_public = bool(is_profile_public)
        self.last_login = last_login
        self.created_at = created_at
        self.updated_at = updated_at

    def hash_and_set_password(self, password: str) -> None:
        """Hash et stocke le mot de passe fourni."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        return check_password_hash(self.password_hash, password)

    def to_session(self) -> dict:
        """Retourne un dictionnaire avec les informations de l'utilisateur pour la session."""
        return {
            "id": self.id,
            "username": self.username,
            "display_name": self.display_name,
            "is_admin": self.is_admin,
            "is_profile_public": self.is_profile_public,
        }

    @classmethod
    def from_row(cls, row: dict) -> "User":
        """Convertit une ligne de la base de données en une instance de User."""
        return cls(
            username=row["username"],
            password_hash=row["password_hash"],
            id_user=row["id"],
            display_name=row.get("display_name"),
            bio=row.get("bio"),
            is_admin=row.get("is_admin", 0),
            is_profile_public=row.get("is_profile_public", 1),
            last_login=row.get("last_login"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<User username={self.username!r} id={self.id}>"
