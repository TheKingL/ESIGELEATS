PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS favorites;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipe_steps;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    username          TEXT     NOT NULL UNIQUE,
    password_hash     TEXT     NOT NULL,
    display_name      TEXT,
    bio               TEXT,
    is_admin          INTEGER  NOT NULL DEFAULT 0, -- 0 = non admin
    is_profile_public INTEGER  NOT NULL DEFAULT 1, -- 1 = public ; 0 = privé
    last_login        DATETIME,
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME
);

CREATE TABLE recipes
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id         INTEGER  NOT NULL,
    title             TEXT     NOT NULL,
    description       TEXT,
    image_path        TEXT,
    servings          INTEGER NOT NULL,
    prep_time_minutes INTEGER NOT NULL,
    status            TEXT     NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'CHANGES_REQUIRED', 'APPROVED', 'REJECTED')),
    validated_by      INTEGER,
    validated_at      DATETIME,
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME,
    FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (validated_by) REFERENCES users (id) ON DELETE SET NULL
);

CREATE TABLE recipe_steps
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER  NOT NULL,
    step_number INTEGER  NOT NULL,
    content     TEXT     NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
    UNIQUE (recipe_id, step_number)
);

CREATE TABLE ingredients
(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE recipe_ingredients
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id     INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity      TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);

CREATE TABLE favorites
(
    user_id    INTEGER  NOT NULL,
    recipe_id  INTEGER  NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
);

CREATE TABLE comments
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id  INTEGER  NOT NULL,
    user_id    INTEGER  NOT NULL,
    content    TEXT     NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE ratings
(
    user_id    INTEGER  NOT NULL,
    recipe_id  INTEGER  NOT NULL,
    rating     INTEGER  NOT NULL CHECK (rating BETWEEN 1 AND 5),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
);

CREATE INDEX idx_recipes_title ON recipes (title);
CREATE INDEX idx_recipe_steps_recipe_id_step ON recipe_steps (recipe_id, step_number);
CREATE INDEX idx_ingredients_name ON ingredients (name);
CREATE INDEX idx_recipe_ingredients_ingredient_id ON recipe_ingredients (ingredient_id);
CREATE INDEX idx_ratings_recipe_id ON ratings (recipe_id);
CREATE INDEX idx_comments_recipe_id_created_at ON comments(recipe_id, created_at);
CREATE INDEX idx_favorites_user_id ON favorites (user_id);
