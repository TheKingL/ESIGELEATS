"""Fichier principal de l'application Flask."""

import os
import sqlite3

from flask import Flask
from flask_session import Session

from controllers.comment_controller import CommentController
from controllers.ingredient_controller import IngredientController
from controllers.recipe_controller import RecipeController
from controllers.user_controller import UserController
from routes.admin import bp as admin_bp
from routes.api import bp as api_bp
from routes.auth import bp as auth_bp
from routes.main import bp as main_bp
from routes.recipes import bp as recipes_bp
from routes.users import bp as users_bp
from sql import SQL
from utils.errors import bp as errors_bp

app = Flask(__name__)

app.secret_key = "supersecretkey"

# Configure image uploads
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads", "recipes")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DB_FILE = "database.db"

def init_db_if_needed():
    """Crée et remplit la base de données si elle n'existe pas."""
    if not os.path.exists(DB_FILE):
        print(f"Base de données '{DB_FILE}' introuvable. Initialisation en cours...")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        try:
            print("> Exécution de setupdb.sql...")
            with open("sql/setupdb.sql", "r", encoding="utf-8") as f:
                cursor.executescript(f.read())

            print("> Exécution de fill_recipes.sql...")
            with open("sql/fill_recipes.sql", "r", encoding="utf-8") as f:
                cursor.executescript(f.read())

            conn.commit()
            print("Base de données créée et remplie avec succès !")

        except Exception as e:
            print(f"Erreur lors de l'initialisation de la BDD : {e}")
            conn.close()
            os.remove(DB_FILE)
            exit(1)
        finally:
            conn.close()
    else:
        print(f"Base de données '{DB_FILE}' détectée. Démarrage...")


init_db_if_needed()
db = SQL(f"sqlite:///{DB_FILE}")

app.user_controller = UserController(db)
app.recipe_controller = RecipeController(db)
app.ingredient_controller = IngredientController(db)
app.comment_controller = CommentController(db)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(errors_bp)
app.register_blueprint(recipes_bp)
app.register_blueprint(users_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5050, host="0.0.0.0")
