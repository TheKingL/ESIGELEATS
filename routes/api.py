"""Route API pour les opérations liées aux recettes, aux utilisateurs et aux commentaires."""

from flask import Blueprint, current_app, jsonify, request, session

from models.recipe import Recipe
from utils.decorators import api_admin_required, api_login_required

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/recipes/<int:recipe_id>/rate", methods=["POST"], endpoint="rate_recipe")
@api_login_required
def rate_recipe(current_user, recipe_id):
    """Permet à un utilisateur de noter une recette."""
    recipe_controller = current_app.recipe_controller
    db = recipe_controller.db

    recipe = recipe_controller.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "not_found"}), 404

    data = request.get_json(silent=True) or {}
    rating = data.get("rating")

    if not isinstance(rating, int) or not 1 <= rating <= 5:
        return jsonify({"error": "invalid_rating"}), 400

    rows = db.execute(
        "SELECT rating FROM ratings WHERE user_id = ? AND recipe_id = ?",
        current_user["id"],
        recipe_id,
    )

    if rows:
        existing = rows[0]["rating"]
        if existing == rating:
            db.execute(
                "DELETE FROM ratings WHERE user_id = ? AND recipe_id = ?",
                current_user["id"],
                recipe_id,
            )
            average_rating = recipe_controller.get_average_rating(recipe_id)
            return jsonify({"status": "removed", "average_rating": average_rating})

        db.execute(
            """
            UPDATE ratings
            SET rating = ?, created_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND recipe_id = ?
            """,
            rating,
            current_user["id"],
            recipe_id,
        )
        status = "updated"
    else:
        db.execute(
            "INSERT INTO ratings (user_id, recipe_id, rating) VALUES (?, ?, ?)",
            current_user["id"],
            recipe_id,
            rating,
        )
        status = "added"

    average_rating = recipe_controller.get_average_rating(recipe_id)
    return jsonify({"status": status, "average_rating": average_rating})


@bp.route(
    "/recipes/<int:recipe_id>/favorite",
    methods=["POST"],
    endpoint="toggle_favorite",
)
@api_login_required
def toggle_favorite(current_user, recipe_id):
    """Ajoute ou supprime une recette des favoris de l'utilisateur."""
    recipe_controller = current_app.recipe_controller
    db = recipe_controller.db

    recipe = recipe_controller.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "not_found"}), 404

    rows = db.execute(
        "SELECT 1 AS found FROM favorites WHERE user_id = ? AND recipe_id = ?",
        current_user["id"],
        recipe_id,
    )
    if rows:
        db.execute(
            "DELETE FROM favorites WHERE user_id = ? AND recipe_id = ?",
            current_user["id"],
            recipe_id,
        )
        return jsonify({"status": "removed"})

    db.execute(
        "INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)",
        current_user["id"],
        recipe_id,
    )
    return jsonify({"status": "added"})


@bp.route("/users/<int:user_id>/recipes", methods=["GET"], endpoint="get_user_recipes")
def get_user_recipes(user_id):
    """Retourne la liste des recettes d'un utilisateur donné."""
    recipe_controller = current_app.recipe_controller
    user_controller = current_app.user_controller
    db = recipe_controller.db

    current_user = session.get("user")

    user = user_controller.get_by_id(user_id)
    if not user:
        return jsonify({"error": "not_found"}), 404

    if (not user.is_profile_public) and (
        not current_user or (current_user["id"] != user_id and not current_user.get("is_admin"))
    ):
        return jsonify({"error": "forbidden"}), 403

    query = """
        SELECT
            r.id,
            r.title,
            r.description,
            r.image_path,
            r.created_at,
            r.status,
            r.prep_time_minutes,
            r.servings,

            -- auteur
            u.username       AS author_username,
            u.display_name   AS author_display_name,

            -- ratings globaux
            COALESCE(AVG(rt.rating), 0) AS average_rating,
            COUNT(rt.rating)            AS rating_count
    """

    params = []

    if current_user:
        query += """
            , ur.rating AS user_rating
            , CASE WHEN f.user_id IS NULL THEN 0 ELSE 1 END AS is_favorite
        """
    else:
        query += """
            , NULL AS user_rating
            , 0    AS is_favorite
        """

    query += """
        FROM recipes r
        JOIN users u
          ON r.author_id = u.id
        LEFT JOIN ratings rt
          ON rt.recipe_id = r.id
    """

    if current_user:
        query += """
        LEFT JOIN ratings ur
          ON ur.recipe_id = r.id
         AND ur.user_id   = ?
        LEFT JOIN favorites f
          ON f.recipe_id  = r.id
         AND f.user_id    = ?
        """
        params.extend([current_user["id"], current_user["id"]])

    query += """
        WHERE r.author_id = ?
        GROUP BY r.id
        ORDER BY r.created_at DESC
    """
    params.append(user_id)

    rows = db.execute(query, *params)

    recipes = []
    for row in rows:
        recipes.append(
            {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "image_path": row["image_path"],
                "created_at": row["created_at"],
                "prep_time_minutes": row["prep_time_minutes"],
                "servings": row["servings"],
                "status": row["status"],
                "author": {
                    "username": row["author_username"],
                    "display_name": row["author_display_name"],
                },
                "average_rating": float(row["average_rating"])
                if row["average_rating"] is not None
                else 0.0,
                "rating_count": row["rating_count"],
                "user_rating": row["user_rating"],
                "is_favorite": bool(row["is_favorite"]),
            }
        )

    return jsonify({"recipes": recipes})


@bp.route(
    "/users/<int:user_id>/rated_recipes",
    methods=["GET"],
    endpoint="rated_recipes",
)
def rated_recipes(user_id):
    """Retourne la liste des recettes notées par un utilisateur donné."""
    user_controller = current_app.user_controller
    recipe_controller = current_app.recipe_controller

    current_user = session.get("user")

    viewed = user_controller.get_by_id(user_id)
    if not viewed:
        return jsonify({"error": "not_found"}), 404

    is_owner = current_user and current_user["id"] == user_id
    is_admin = current_user and current_user.get("is_admin", False)

    if not viewed.is_profile_public and not (is_owner or is_admin):
        return jsonify({"error": "private_profile"}), 403

    rated = recipe_controller.get_rated_recipes_for_user(user_id)

    payload = []
    for r in rated:
        payload.append(
            {
                "id": r.id,
                "title": r.title,
                "user_rating": r.user_rating,
                "average_rating": r.average_rating,
                "rating_date": r.rating_date,
                "image_path": r.image_path,
            }
        )

    return jsonify({"recipes": payload})


@bp.route("/recipes", methods=["GET"], endpoint="get_recipes")
def get_recipes():
    """
    Retourne la liste des recettes approuvées (APPROVED),
    triées par date de création décroissante.
    """
    db = current_app.recipe_controller.db

    query = """
        SELECT r.*,
               u.username AS author_username,
               u.display_name AS author_display_name,
               AVG(rt.rating) AS average_rating,
               COUNT(rt.rating) AS rating_count,
               (SELECT COUNT(*) FROM favorites f WHERE f.recipe_id = r.id) AS favorites_count
        FROM recipes r
        JOIN users u ON u.id = r.author_id
        LEFT JOIN ratings rt ON rt.recipe_id = r.id
        WHERE r.status = 'APPROVED'
        GROUP BY r.id
        ORDER BY r.created_at DESC
    """

    rows = db.execute(query)

    results = []
    for row in rows:
        results.append(
            {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "image_path": row["image_path"],
                "author": row["author_display_name"] or row["author_username"],
                "average_rating": float(row["average_rating"]) if row["average_rating"] else None,
                "rating_count": row["rating_count"],
                "favorites_count": row["favorites_count"],
                "created_at": row["created_at"],
                "servings": row["servings"],
                "prep_time_minutes": row["prep_time_minutes"],
            }
        )

    return jsonify(results)


@bp.route("/admin/recipes/pending", methods=["GET"], endpoint="admin_pending_recipes")
@api_login_required
@api_admin_required
def admin_pending_recipes(current_user):
    """Retourne la liste des recettes en attente de validation (PENDING), triées par titre."""
    recipe_controller = current_app.recipe_controller
    db = recipe_controller.db

    rows = db.execute(
        """
        SELECT r.id, r.title, r.description, r.created_at, u.username AS author_username, u.display_name AS author_display_name FROM recipes r
        JOIN users u ON u.id = r.author_id
        WHERE r.status = ?
        ORDER BY r.title COLLATE NOCASE
        """,
        Recipe.STATUS_PENDING,
    )

    data = []
    for row in rows:
        data.append(
            {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"] or "",
                "created_at": row["created_at"],
                "author_username": row["author_username"],
                "author_display_name": row["author_display_name"],
            }
        )

    return jsonify(data)


@bp.route(
    "/admin/recipes/<int:recipe_id>/status",
    methods=["POST"],
    endpoint="admin_update_recipe_status",
)
@api_login_required
@api_admin_required
def admin_update_recipe_status(current_user, recipe_id: int):
    """Met à jour le statut d'une recette (APPROVED, CHANGES_REQUIRED, REJECTED)."""
    recipe_controller = current_app.recipe_controller
    recipe = recipe_controller.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "not_found"}), 404

    payload = request.get_json(silent=True) or {}
    status = payload.get("status")

    allowed_statuses = {
        Recipe.STATUS_APPROVED,
        Recipe.STATUS_CHANGES_REQUIRED,
        Recipe.STATUS_REJECTED,
    }
    if status not in allowed_statuses:
        return jsonify({"error": "invalid_status"}), 400

    recipe_controller.update_status(
        recipe_id,
        status,
        validated_by=current_user["id"],
    )

    if status == Recipe.STATUS_APPROVED:
        msg = "Recette validée avec succès."
        category = "success"
    elif status == Recipe.STATUS_CHANGES_REQUIRED:
        msg = "Recette marquée comme 'à modifier'"
        category = "warning"
    else:
        msg = "Recette refusée."
        category = "danger"

    return jsonify(
        {
            "status": "success",
            "recipe_id": recipe_id,
            "new_status": status,
            "flash_message": msg,
            "flash_category": category,
        }
    )


def _serialize_comment(comment):
    """Sérialise un objet Comment en dictionnaire pour JSON."""
    return {
        "id": comment.id,
        "recipe_id": comment.recipe_id,
        "content": comment.content,
        "created_at": comment.created_at,
        "user": {
            "id": comment.user_id,
            "username": comment.username,
            "display_name": comment.display_name,
            "is_admin": comment.is_admin,
            "is_profile_public": comment.is_profile_public,
        },
    }


@bp.route("/recipes/<int:recipe_id>/comments", methods=["GET"])
def get_recipe_comments(recipe_id):
    """Retourne la liste des commentaires pour une recette donnée."""
    comment_controller = current_app.comment_controller

    comments = comment_controller.get_comments(recipe_id)
    return jsonify([_serialize_comment(c) for c in comments])


@bp.route("/recipes/<int:recipe_id>/comments", methods=["POST"])
@api_login_required
def add_recipe_comment(current_user, recipe_id):
    """Ajoute un commentaire à une recette donnée."""
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()

    if not content:
        return jsonify({"error": "Le commentaire ne peut pas être vide."}), 400

    recipe_controller = current_app.recipe_controller
    recipe = recipe_controller.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "Recette introuvable."}), 404

    comment_controller = current_app.comment_controller
    comment = comment_controller.create_comment(recipe_id, current_user["id"], content)

    return jsonify(_serialize_comment(comment)), 201


@bp.route("/notifications/counters", methods=["GET"], endpoint="notification_counters")
@api_login_required
def notification_counters(current_user):
    """
    Renvoie les compteurs de notifications pour la navbar.
    - changes_required : nb de recettes de l'utilisateur avec statut CHANGES_REQUIRED
    - pending_recipes  : nb de recettes en attente (PENDING) si admin, sinon 0
    """
    recipe_controller = current_app.recipe_controller
    db = recipe_controller.db
    user_id = current_user["id"]

    row = db.execute(
        "SELECT COUNT(*) AS c FROM recipes WHERE author_id = ? AND status = ?",
        user_id,
        Recipe.STATUS_CHANGES_REQUIRED,
    )[0]
    changes_required = int(row["c"])

    pending_recipes = 0
    if current_user.get("is_admin"):
        row2 = db.execute(
            "SELECT COUNT(*) AS c FROM recipes WHERE status = ?",
            Recipe.STATUS_PENDING,
        )[0]
        pending_recipes = int(row2["c"])

    return jsonify(
        {
            "changes_required": changes_required,
            "pending_recipes": pending_recipes,
        }
    )


@bp.route("/admin/stats/overview", methods=["GET"], endpoint="admin_stats_overview")
@api_login_required
@api_admin_required
def admin_stats_overview(current_user):
    """
    Retourne un gros objet 'stats' pour le dashboard admin.
    ATTENTION : accès réservé aux admins.
    """
    db = current_app.recipe_controller.db

    stats = {
        "kpis": {
            "total_users": 0,
            "total_recipes": 0,
            "pending_recipes": 0,
            "changes_required_recipes": 0,
            "rejected_recipes": 0,
            "total_favorites": 0,
            "total_ratings": 0,
            "total_comments": 0,
        },
        "status_counts": {
            "PENDING": 0,
            "CHANGES_REQUIRED": 0,
            "APPROVED": 0,
            "REJECTED": 0,
        },
        "recipes_by_day": {
            "labels": [],
            "created": [],
            "approved": [],
        },
        "rating_distribution": {
            "ratings": [1, 2, 3, 4, 5],
            "counts": [0, 0, 0, 0, 0],
        },
        "top_authors": [],
        "top_recipes_engagement": [],
    }

    # KPIs basiques
    row = db.execute("SELECT COUNT(*) AS c FROM users")[0]
    stats["kpis"]["total_users"] = row["c"]
    row = db.execute("SELECT COUNT(*) AS c FROM recipes")[0]
    stats["kpis"]["total_recipes"] = row["c"]
    row = db.execute(
        "SELECT COUNT(*) AS c FROM recipes WHERE status = ?",
        Recipe.STATUS_PENDING,
    )[0]
    stats["kpis"]["pending_recipes"] = row["c"]
    row = db.execute(
        "SELECT COUNT(*) AS c FROM recipes WHERE status = ?",
        Recipe.STATUS_CHANGES_REQUIRED,
    )[0]
    stats["kpis"]["changes_required_recipes"] = row["c"]
    row = db.execute(
        "SELECT COUNT(*) AS c FROM recipes WHERE status = ?",
        Recipe.STATUS_REJECTED,
    )[0]
    stats["kpis"]["rejected_recipes"] = row["c"]
    row = db.execute("SELECT COUNT(*) AS c FROM favorites")[0]
    stats["kpis"]["total_favorites"] = row["c"]
    row = db.execute("SELECT COUNT(*) AS c FROM ratings")[0]
    stats["kpis"]["total_ratings"] = row["c"]
    row = db.execute("SELECT COUNT(*) AS c FROM comments")[0]
    stats["kpis"]["total_comments"] = row["c"]

    # Répartition des statuts
    rows = db.execute("""
        SELECT status, COUNT(*) AS c FROM recipes
        GROUP BY status;
    """)
    for row in rows:
        stats["status_counts"][row["status"]] = row["c"]

    # Recettes dans le temps
    created = db.execute("""
        SELECT DATE(created_at) AS d, COUNT(*) AS c FROM recipes 
        GROUP BY DATE(created_at)
        ORDER BY d;
    """)

    approved = db.execute("""
        SELECT DATE(validated_at) AS d, COUNT(*) AS c FROM recipes
        WHERE status = 'APPROVED' AND validated_at IS NOT NULL
        GROUP BY DATE(validated_at)
        ORDER BY d;
    """)

    date_to_created_count = {row["d"]: row["c"] for row in created}
    date_to_approved_count = {row["d"]: row["c"] for row in approved}
    all_dates = sorted(set(date_to_created_count.keys()) | set(date_to_approved_count.keys()))
    for d in all_dates:
        stats["recipes_by_day"]["labels"].append(d)
        stats["recipes_by_day"]["created"].append(date_to_created_count.get(d, 0))
        stats["recipes_by_day"]["approved"].append(date_to_approved_count.get(d, 0))

    # Distribution des notes
    rating_counts = db.execute("""
        SELECT rating, COUNT(*) AS c FROM ratings
        GROUP BY rating;
    """)

    for row in rating_counts:
        rating = row["rating"]
        count = row["c"]
        if 1 <= rating <= 5:
            stats["rating_distribution"]["counts"][rating - 1] = count

    # Top auteurs
    top_authors = db.execute("""
        SELECT u.id, u.username, u.display_name, COUNT(r.id) AS recipe_count
        FROM users u
        LEFT JOIN recipes r ON r.author_id = u.id
        GROUP BY u.id
        ORDER BY recipe_count DESC
        LIMIT 5;
    """)

    for row in top_authors:
        stats["top_authors"].append(
            {
                "label": row["display_name"] or row["username"],
                "recipe_count": row["recipe_count"],
            }
        )

    # Top recettes (le + de buzz)
    top_recipes = db.execute("""
        SELECT
            r.id,
            r.title,
            (SELECT COUNT(*) FROM favorites f WHERE f.recipe_id = r.id) AS fav_count,
            (SELECT COUNT(*) FROM comments c WHERE c.recipe_id = r.id) AS comment_count
        FROM recipes r
        ORDER BY fav_count DESC, comment_count DESC
        LIMIT 5;
    """)

    for row in top_recipes:
        stats["top_recipes_engagement"].append(
            {
                "title": row["title"],
                "favorites": row["fav_count"],
                "comments": row["comment_count"],
            }
        )

    return jsonify(stats)
