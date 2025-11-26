"""Tests unitaires des fonctions utilitaires."""

from utils.helpers import is_strong_password, is_user_admin, is_user_himself


def test_is_strong_password():
    """Vérifie la validation des mots de passe."""
    # Cas valides
    assert is_strong_password("Password123!") is True
    assert is_strong_password("GazoLeBoss94*") is True

    # Cas invalides
    assert is_strong_password("short") is False  # Trop court
    assert is_strong_password("password123!") is False  # Pas de majuscule
    assert is_strong_password("PASSWORD123!") is False  # Pas de minuscule
    assert is_strong_password("PasswordWithoutNumber!") is False  # Pas de chiffre
    assert is_strong_password("Password123") is False  # Pas de caractère spécial


def test_is_user_admin():
    """Vérifie la détection d'admin."""
    admin_user = {"id": 1, "is_admin": True}
    normal_user = {"id": 2, "is_admin": False}
    none_user = None

    assert is_user_admin(admin_user) is True
    assert is_user_admin(normal_user) is False
    assert is_user_admin(none_user) is False


def test_is_user_himself():
    """Vérifie si l'utilisateur courant est bien la cible."""
    current = {"id": 42}

    assert is_user_himself(current, 42) is True
    assert is_user_himself(current, 99) is False
    assert is_user_himself(None, 42) is False
