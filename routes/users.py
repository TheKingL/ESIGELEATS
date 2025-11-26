"""Route pour la gestion des utilisateurs"""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.user import User
from utils.decorators import login_required
from utils.helpers import is_strong_password, is_user_admin, is_user_himself

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("<int:user_id>", endpoint="user_profile")
@login_required
def user_profile(current_user, user_id):
    """Afficher le profil d'un utilisateur."""
    row = current_app.user_controller.db.execute("SELECT * FROM users WHERE id = ?", user_id)

    if not row:
        return render_template("errors/404.html"), 404

    row = row[0]

    viewed_user = User(username=row["username"], password_hash=row["password_hash"])
    viewed_user.id = row["id"]
    viewed_user.display_name = row["display_name"]
    viewed_user.bio = row["bio"]
    viewed_user.is_admin = bool(row["is_admin"])
    viewed_user.is_profile_public = bool(row["is_profile_public"])
    viewed_user.last_login = row["last_login"]
    viewed_user.created_at = row["created_at"]
    viewed_user.updated_at = row["updated_at"]

    if not is_user_admin(current_user) and (
        not viewed_user.is_profile_public and current_user["id"] != viewed_user.id
    ):
        return render_template("errors/403_profile_private.html", viewed_user=viewed_user), 403

    return render_template("user/profile.html", viewed_user=viewed_user, current_user=current_user)


@bp.route("<int:user_id>/edit", methods=["GET", "POST"], endpoint="edit_user_profile")
@login_required
def edit_user_profile(current_user, user_id):
    """Modifier le profil d'un utilisateur"""
    if current_user["id"] != user_id:
        flash("Vous n'êtes pas autorisé à modifier ce profil.", "error")
        return redirect(url_for("users.user_profile", user_id=user_id))

    user = current_app.user_controller.get_by_id(user_id)
    if not user:
        return render_template("errors/404.html"), 404

    errors = {}
    form = {
        "username": user.username,
        "display_name": user.display_name,
        "bio": user.bio,
        "is_profile_public": user.is_profile_public,
    }

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        display_name = request.form.get("display_name", "").strip()
        bio = request.form.get("bio", "").strip()
        is_profile_public = "is_profile_public" in request.form

        form["username"] = username
        form["display_name"] = display_name
        form["bio"] = bio
        form["is_profile_public"] = is_profile_public

        if not username:
            errors["username"] = "Le nom d'utilisateur est requis."
        elif (
            username != user.username
            and current_app.user_controller.get_by_username(username) is not None
        ):
            errors["username"] = "Ce nom d'utilisateur est déjà utilisé."

        if not display_name:
            errors["display_name"] = "Le nom de profil est requis."

        if errors:
            return render_template("user/edit_profile.html", errors=errors, form=form, user=user)

        user.username = username
        user.display_name = display_name
        user.bio = bio
        user.is_profile_public = is_profile_public
        current_app.user_controller.update_user(user)

        session["user"] = user.to_session()
        flash("Votre profil a été mis à jour avec succès.", "success")
        return redirect(url_for("users.user_profile", user_id=user.id))

    return render_template("user/edit_profile.html", errors=errors, form=form, user=user)


@bp.route(
    "<int:user_id>/password",
    methods=["GET", "POST"],
    endpoint="edit_user_password",
)
@login_required
def edit_user_password(current_user, user_id):
    """Modifier le mot de passe d'un utilisateur"""
    if current_user["id"] != user_id:
        flash("Vous n'êtes pas autorisé à modifier ce mot de passe.", "error")
        return redirect(url_for("users.user_profile", user_id=user_id))

    user = current_app.user_controller.get_by_id(user_id)
    if not user:
        return render_template("errors/404.html"), 404

    errors = {}
    form = {}

    if request.method == "POST":
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        if not password:
            errors["password"] = "Le mot de passe est requis."
        elif not is_strong_password(password):
            errors["password"] = (
                "Le mot de passe doit contenir au moins 8 caractères, une majuscule, "
                "une minuscule, un chiffre et un caractère spécial."
            )

        if not password_confirm:
            errors["password_confirm"] = "Merci de confirmer votre mot de passe."
        elif password != password_confirm:
            errors["password_confirm"] = "Les mots de passe ne correspondent pas."

        if errors:
            return render_template("user/edit_password.html", errors=errors, form=form, user=user)

        user.hash_and_set_password(password)
        current_app.user_controller.update_user_password(user)

        flash("Votre mot de passe a été mis à jour avec succès.", "success")
        return redirect(url_for("users.user_profile", user_id=user.id))

    return render_template("user/edit_password.html", errors=errors, form=form, user=user)


@bp.route("/<int:user_id>/delete", methods=["POST"], endpoint="delete_user")
@login_required
def delete_user(current_user, user_id):
    """Supprimer un utilisateur."""

    user_controller = current_app.user_controller

    user = user_controller.get_by_id(user_id)
    if not user:
        return render_template("errors/404.html"), 404

    is_admin = is_user_admin(current_user)
    is_self = is_user_himself(current_user, user_id)

    if not (is_admin or is_self):
        flash("Vous n'êtes pas autorisé à supprimer ce compte.", "error")
        return redirect(url_for("users.user_profile", user_id=user_id))

    user_controller.delete_user(user_id)

    if is_self:
        session.pop("user", None)
        flash("Votre compte a bien été supprimé. Au revoir !", "success")
        return redirect(url_for("main.home"))

    flash("Le compte a bien été supprimé.", "success")
    return redirect(url_for("main.home"))


@bp.route("/<int:user_id>/recipes", endpoint="user_recipes")
@login_required
def user_recipes(current_user, user_id):
    """Afficher les recettes d'un utilisateur."""
    user_controller = current_app.user_controller
    user = user_controller.get_by_id(user_id)

    if not user:
        return render_template("errors/404.html"), 404

    if (not user.is_profile_public) and (
        current_user["id"] != user_id and not current_user.get("is_admin")
    ):
        return render_template("errors/403_profile_private.html", viewed_user=user), 403

    return render_template("user/user_recipes.html", viewed_user=user, current_user=current_user)


@bp.route("/<int:user_id>/favorites", methods=["GET"], endpoint="favorite_recipes")
@login_required
def user_favorite_recipes(current_user, user_id):
    """Afficher les recettes favorites d'un utilisateur."""
    user_controller = current_app.user_controller
    recipe_controller = current_app.recipe_controller

    viewed_user = user_controller.get_by_id(user_id)
    if not viewed_user:
        return render_template("errors/404.html"), 404

    is_owner = current_user["id"] == viewed_user.id
    is_admin = current_user.get("is_admin", False)

    if not viewed_user.is_profile_public and not (is_owner or is_admin):
        return render_template("errors/403_profile_private.html"), 403

    favorites = recipe_controller.get_favorite_recipes_for_user(user_id)

    return render_template(
        "user/user_favorite_recipes.html",
        viewed_user=viewed_user,
        current_user=current_user,
        favorites=favorites,
    )


@bp.route("/<int:user_id>/rated", methods=["GET"], endpoint="rated_recipes_page")
@login_required
def user_rated_recipes(current_user, user_id):
    """Afficher les recettes notées par un utilisateur."""
    user_controller = current_app.user_controller

    viewed_user = user_controller.get_by_id(user_id)
    if not viewed_user:
        return render_template("errors/404.html"), 404

    is_owner = current_user["id"] == viewed_user.id
    is_admin = current_user.get("is_admin", False)

    if not viewed_user.is_profile_public and not (is_owner or is_admin):
        return render_template("errors/403_profile_private.html", viewed_user=viewed_user), 403

    return render_template(
        "user/user_rated_recipes.html",
        viewed_user=viewed_user,
        current_user=current_user,
    )
