"""Routes pour le panel administrateur."""

from flask import Blueprint, current_app, render_template

from utils.decorators import admin_required, login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"], endpoint="dashboard")
@login_required
@admin_required
def dashboard(current_user):
    """Page principale du panel administrateur (réservée aux admins)."""
    return render_template("admin/dashboard.html", current_user=current_user)


@bp.route("/users-list", methods=["GET"], endpoint="list_users")
@login_required
@admin_required
def list_users(current_user):
    """Liste tous les utilisateurs (réservé aux admins)."""
    user_controller = current_app.user_controller
    users = user_controller.list_all()
    return render_template("admin/users.html", current_user=current_user, users=users)


@bp.route("/recipes", methods=["GET"], endpoint="recipes")
@login_required
@admin_required
def list_recipes(current_user):
    """Listing de toutes les recettes (tous statuts confondus) pour les admins."""

    recipe_controller = current_app.recipe_controller
    db = recipe_controller.db

    rows = db.execute(
        """
        SELECT
            r.*,
            u.display_name AS author_display_name,
            u.username     AS author_username,
            AVG(rt.rating)            AS average_rating,
            COUNT(rt.rating)          AS rating_count,
            COUNT(DISTINCT f.user_id) AS favorites_count
        FROM recipes r
        LEFT JOIN users u   ON u.id = r.author_id
        LEFT JOIN ratings rt ON rt.recipe_id = r.id
        LEFT JOIN favorites f ON f.recipe_id = r.id
        GROUP BY r.id
        ORDER BY r.status, r.title COLLATE NOCASE;
        """
    )

    recipes = []
    for row in rows:
        obj = type("RecipeRow", (), {})()
        obj.id = row["id"]
        obj.title = row["title"]
        obj.description = row.get("description")
        obj.status = row["status"]
        obj.image_path = row.get("image_path")
        obj.servings = row.get("servings")
        obj.prep_time_minutes = row.get("prep_time_minutes")
        obj.created_at = row.get("created_at")
        obj.author_display_name = row.get("author_display_name")
        obj.author_username = row.get("author_username")
        obj.average_rating = (
            float(row["average_rating"]) if row["average_rating"] is not None else None
        )
        obj.rating_count = row["rating_count"]
        obj.favorites_count = row["favorites_count"]
        recipes.append(obj)

    return render_template(
        "admin/recipes.html",
        current_user=current_user,
        recipes=recipes,
    )


@bp.route("/recipes-list/validation", methods=["GET"], endpoint="recipes_validation")
@login_required
@admin_required
def recipes_validation(current_user):
    """Page de validation des recettes (affiche uniquement les PENDING, gérées en JS via API)."""
    return render_template(
        "admin/recipes_validation.html",
        current_user=current_user,
    )


@bp.route("/insights", methods=["GET"], endpoint="insights")
@login_required
@admin_required
def insights(current_user):
    """Dashboard statistiques / insights admin."""
    return render_template("admin/insights.html", current_user=current_user)
