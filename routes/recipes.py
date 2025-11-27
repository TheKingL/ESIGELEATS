"""Routes pour la gestion des recettes : création, édition, suppression, affichage."""

import os
from uuid import uuid4

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
from werkzeug.utils import secure_filename

from models.recipe import Recipe
from utils.decorators import login_required
from utils.helpers import allowed_image

bp = Blueprint("recipes", __name__, url_prefix="/recipes")


def _parse_recipe_form(req):
    """
    Lit et valide le formulaire de recette (pour create + edit).
    Retourne un dict avec :
      - form, errors
      - servings, prep_time_minutes
      - ingredient_pairs, ingredient_values
      - step_contents, step_values
    """
    errors: dict = {}

    title = req.form.get("title", "").strip()
    description = req.form.get("description", "").strip()
    servings_raw = req.form.get("servings", "").strip()
    prep_time_raw = req.form.get("prep_time_minutes", "").strip()

    form = {
        "title": title,
        "description": description,
        "servings": servings_raw,
        "prep_time_minutes": prep_time_raw,
    }

    servings = None
    prep_time_minutes = None

    if not title:
        errors["title"] = "Le titre de la recette est requis."

    if servings_raw:
        try:
            servings = int(servings_raw)
            if servings <= 0:
                raise ValueError
        except ValueError:
            errors["servings"] = "Le nombre de portions doit être un entier positif."

    if prep_time_raw:
        try:
            prep_time_minutes = int(prep_time_raw)
            if prep_time_minutes < 0:
                raise ValueError
        except ValueError:
            errors["prep_time_minutes"] = "Le temps de préparation doit être un entier en minutes."

    names = req.form.getlist("ingredient_name[]")
    quantities = req.form.getlist("ingredient_quantity[]")
    ingredient_pairs = []
    for name, qty in zip(names, quantities, strict=True):
        n = (name or "").strip()
        q = (qty or "").strip()
        if n:
            ingredient_pairs.append((n, q or None))

    if not ingredient_pairs:
        errors["ingredients"] = "Ajoutez au moins un ingrédient."

    ingredient_values = [
        type("Obj", (), {"name": n, "quantity": q or ""}) for n, q in ingredient_pairs
    ] or [type("Obj", (), {"name": "", "quantity": ""})]

    steps_raw = req.form.getlist("step_content[]")
    step_contents = [(s or "").strip() for s in steps_raw if (s or "").strip()]

    if not step_contents:
        errors["steps"] = "Ajoutez au moins une étape de préparation."

    step_values = [
        type("Obj", (), {"content": s}) for s in (step_contents if step_contents else steps_raw)
    ] or [type("Obj", (), {"content": ""})]

    return {
        "form": form,
        "errors": errors,
        "servings": servings,
        "prep_time_minutes": prep_time_minutes,
        "ingredient_pairs": ingredient_pairs,
        "ingredient_values": ingredient_values,
        "step_contents": step_contents,
        "step_values": step_values,
    }


@bp.route("create", methods=["GET", "POST"])
@login_required
def create_recipe(current_user):
    """Page de création de recette."""
    ingredients_options = current_app.ingredient_controller.list_all()

    if request.method == "POST":
        parsed = _parse_recipe_form(request)

        form = parsed["form"]
        errors = dict(parsed["errors"])
        servings = parsed["servings"]
        prep_time_minutes = parsed["prep_time_minutes"]
        ingredient_pairs = parsed["ingredient_pairs"]
        ingredient_values = parsed["ingredient_values"]
        step_contents = parsed["step_contents"]
        step_values = parsed["step_values"]

        image_file = request.files.get("image")
        image_extension = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            if not allowed_image(filename):
                errors["image"] = (
                    "Format d'image non supporté (PNG, JPG, JPEG, GIF, WEBP uniquement)."
                )
            else:
                image_extension = filename.rsplit(".", 1)[1].lower()

        if errors:
            return render_template(
                "recipe/recipe_form.html",
                mode="create",
                form=form,
                errors=errors,
                current_user=current_user,
                ingredients_options=ingredients_options,
                ingredient_values=ingredient_values,
                step_values=step_values,
                recipe=None,
            )

        image_path = None
        if image_file and image_extension:
            unique_name = f"{uuid4().hex}.{image_extension}"
            full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
            image_file.save(full_path)
            image_path = f"uploads/recipes/{unique_name}"

        recipe = Recipe(
            id=None,
            author_id=current_user["id"],
            title=form["title"],
            description=form["description"] or None,
            image_path=image_path,
            servings=servings,
            prep_time_minutes=prep_time_minutes,
            status=Recipe.STATUS_PENDING,
        )

        current_app.recipe_controller.create_recipe(recipe)
        current_app.ingredient_controller.replace_ingredients_for_recipe(
            recipe.id, ingredient_pairs
        )
        current_app.recipe_controller.replace_steps_for_recipe(recipe.id, step_contents)

        flash(
            "Votre recette a été créée et est en attente de validation par un administrateur.",
            "success",
        )
        return redirect(url_for("main.home"))

    # GET
    ingredient_values = [type("Obj", (), {"name": "", "quantity": ""})]
    step_values = [type("Obj", (), {"content": ""})]

    return render_template(
        "recipe/recipe_form.html",
        mode="create",
        form=None,
        errors={},
        current_user=current_user,
        ingredients_options=ingredients_options,
        ingredient_values=ingredient_values,
        step_values=step_values,
        recipe=None,
    )


@bp.route(
    "/<int:recipe_id>/delete",
    methods=["POST"],
    endpoint="delete_recipe",
)
@login_required
def delete_recipe(current_user, recipe_id):
    """Supprime une recette."""
    recipe_controller = current_app.recipe_controller

    recipe = recipe_controller.get_by_id(recipe_id)
    if not recipe:
        return render_template("errors/404.html"), 404

    is_author = current_user["id"] == recipe.author_id
    is_admin = current_user.get("is_admin")
    if not (is_author or is_admin):
        flash("Vous n'êtes pas autorisé à supprimer cette recette.", "error")
        return redirect(url_for("recipes.show_recipe", recipe_id=recipe_id))

    if getattr(recipe, "image_path", None):
        try:
            full_path = os.path.join(current_app.root_path, "static", recipe.image_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except FileNotFoundError:
            pass

    recipe_controller.delete_recipe(recipe_id)
    flash("La recette a été supprimée avec succès.", "success")
    return redirect(url_for("main.home"))


@bp.route(
    "/<int:recipe_id>/edit",
    methods=["GET", "POST"],
    endpoint="edit_recipe",
)
@login_required
def edit_recipe(current_user, recipe_id):
    """Page d'édition de recette."""
    recipe_controller = current_app.recipe_controller
    ingredient_controller = current_app.ingredient_controller

    recipe = recipe_controller.get_by_id(recipe_id)
    if not recipe:
        return render_template("errors/404.html"), 404

    is_author = current_user["id"] == recipe.author_id
    is_admin = current_user.get("is_admin")
    if not (is_author or is_admin):
        flash("Vous n'êtes pas autorisé à modifier cette recette.", "error")
        return redirect(url_for("recipes.show_recipe", recipe_id=recipe_id))

    ingredients_options = ingredient_controller.list_all()
    existing_ingredients = ingredient_controller.get_ingredients_for_recipe(recipe_id)
    existing_steps = recipe_controller.get_steps_for_recipe(recipe_id)

    errors: dict = {}

    if request.method == "POST":
        parsed = _parse_recipe_form(request)

        form = parsed["form"]
        errors = dict(parsed["errors"])
        servings = parsed["servings"]
        prep_time_minutes = parsed["prep_time_minutes"]
        ingredient_pairs = parsed["ingredient_pairs"]
        ingredient_values = parsed["ingredient_values"]
        step_contents = parsed["step_contents"]
        step_values = parsed["step_values"]

        image_file = request.files.get("image")
        new_image_path = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            if not allowed_image(filename):
                errors["image"] = (
                    "Le format d'image n'est pas supporté (png, jpg, jpeg, gif, webp)."
                )
            else:
                ext = filename.rsplit(".", 1)[1].lower()
                unique_name = f"{uuid4().hex}.{ext}"
                upload_folder = current_app.config["UPLOAD_FOLDER"]
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join(upload_folder, unique_name)
                image_file.save(image_path)
                new_image_path = f"uploads/recipes/{unique_name}"

        if errors:
            return render_template(
                "recipe/recipe_form.html",
                mode="edit",
                form=form,
                errors=errors,
                current_user=current_user,
                ingredients_options=ingredients_options,
                ingredient_values=ingredient_values,
                step_values=step_values,
                recipe=recipe,
            )

        recipe.title = form["title"]
        recipe.description = form["description"] or None
        recipe.servings = servings
        recipe.prep_time_minutes = prep_time_minutes

        if new_image_path:
            recipe.image_path = new_image_path

        recipe.status = Recipe.STATUS_PENDING

        recipe_controller.update_recipe(recipe)
        ingredient_controller.replace_ingredients_for_recipe(recipe.id, ingredient_pairs)
        recipe_controller.replace_steps_for_recipe(recipe.id, step_contents)

        flash(
            "Votre recette a été mise à jour et est à nouveau en attente de validation.",
            "success",
        )
        return redirect(url_for("recipes.show_recipe", recipe_id=recipe.id))

    # GET
    form = {
        "title": recipe.title,
        "description": recipe.description or "",
        "servings": recipe.servings if recipe.servings is not None else "",
        "prep_time_minutes": recipe.prep_time_minutes
        if recipe.prep_time_minutes is not None
        else "",
    }

    ingredient_values = [
        type(
            "Obj",
            (),
            {"name": ing.ingredient_name, "quantity": ing.quantity or ""},
        )
        for ing in existing_ingredients
    ] or [type("Obj", (), {"name": "", "quantity": ""})]

    step_values = [type("Obj", (), {"content": step.content}) for step in existing_steps] or [
        type("Obj", (), {"content": ""})
    ]

    return render_template(
        "recipe/recipe_form.html",
        mode="edit",
        form=form,
        errors=errors,
        current_user=current_user,
        ingredients_options=ingredients_options,
        ingredient_values=ingredient_values,
        step_values=step_values,
        recipe=recipe,
    )


@bp.route("/<int:recipe_id>", methods=["GET"], endpoint="show_recipe")
def show_recipe(recipe_id):
    """Affiche une recette."""
    recipe_controller = current_app.recipe_controller
    ingredient_controller = current_app.ingredient_controller
    user_controller = current_app.user_controller
    db = recipe_controller.db

    recipe = recipe_controller.get_by_id(recipe_id)
    if not recipe:
        return render_template("errors/404.html"), 404

    author = user_controller.get_by_id(recipe.author_id)
    current_user = session.get("user")
    if author and not author.is_profile_public:
        is_owner = current_user and current_user["id"] == author.id
        is_admin = current_user and current_user.get("is_admin")

        if not (is_owner or is_admin):
            return render_template("errors/403_recipe_private.html", viewed_user=author), 403

    ingredients = ingredient_controller.get_ingredients_for_recipe(recipe_id)
    steps = recipe_controller.get_steps_for_recipe(recipe_id)
    average_rating = recipe_controller.get_average_rating(recipe_id)

    rows = db.execute(
        "SELECT COUNT(*) AS c FROM ratings WHERE recipe_id = ?",
        recipe_id,
    )
    rating_count = rows[0]["c"] if rows else 0

    current_user = session.get("user")
    is_favorite = False
    user_rating = None

    if current_user:
        rows = db.execute(
            "SELECT 1 AS found FROM favorites WHERE user_id = ? AND recipe_id = ?",
            current_user["id"],
            recipe_id,
        )
        is_favorite = bool(rows)

        rows = db.execute(
            "SELECT rating FROM ratings WHERE user_id = ? AND recipe_id = ?",
            current_user["id"],
            recipe_id,
        )
        if rows:
            user_rating = rows[0]["rating"]

    return render_template(
        "recipe/view_recipe.html",
        recipe=recipe,
        author=author,
        ingredients=ingredients,
        steps=steps,
        average_rating=average_rating,
        rating_count=rating_count,
        is_favorite=is_favorite,
        user_rating=user_rating,
        current_user=current_user,
    )


@bp.route("/", methods=["GET"], endpoint="list_recipes")
def list_recipes():
    """Liste toutes les recettes publiées."""
    current_user = session.get("user")
    return render_template("recipe/list_recipes.html", current_user=current_user)


@bp.route("/ingredients/add", methods=["GET", "POST"], endpoint="add_ingredient")
@login_required
def add_ingredient(current_user):
    """Page d'ajout d'un nouvel ingrédient (admin uniquement)."""
    if not current_user.get("is_admin"):
        flash("Vous n'êtes pas autorisé à ajouter un ingrédient.", "error")
        return redirect(url_for("recipes.list_recipes"))

    ingredient_controller = current_app.ingredient_controller
    errors = {}
    form = {"name": ""}

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        form["name"] = name

        if not name:
            errors["name"] = "Le nom de l'ingrédient est requis."
        elif ingredient_controller.search_by_name(name):
            errors["name"] = "Cet ingrédient existe déjà."

        if not errors:
            ingredient_controller.create_ingredient(name)
            flash("Ingrédient ajouté avec succès !", "success")
            return redirect(url_for("recipes.list_recipes"))

    return render_template(
        "recipe/add_ingredient.html",
        current_user=current_user,
        errors=errors,
        form=form,
    )
