"""Fonctions d'aide génériques dans l'application"""

import re

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def is_strong_password(password: str) -> bool:
    """Vérifie si le mot de passe est fort."""
    if len(password) < 8:
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True


def allowed_image(filename: str) -> bool:
    """Vérifie si l'extension du fichier est autorisée pour les images."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS


def is_user_admin(user: dict) -> bool:
    """Vérifie si l'utilisateur donné est un administrateur."""
    return user is not None and user.get("is_admin") is True


def is_user_himself(user: dict, user_id: int) -> bool:
    """Vérifie si l'utilisateur donné correspond à l'ID spécifié."""
    return user is not None and user["id"] == user_id
