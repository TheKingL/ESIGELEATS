"""Petit script pour ajouter un utilisateur administrateur à la base de données."""

from werkzeug.security import generate_password_hash

from models.user import User
from sql import SQL

db = SQL("sqlite:///database.db")

admin_user = User("admin", generate_password_hash("adminpassword"))
admin_id = db.execute(
    "INSERT INTO users (username, password_hash, display_name, is_admin, is_profile_public) VALUES (?, ?, ?, ?, ?)",
    admin_user.login,
    admin_user.password_hash,
    "Administrateur",
    1,
    0,
)
print(f"Created admin user with ID {admin_id}: {admin_user}")
