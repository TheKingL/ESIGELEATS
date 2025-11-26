-- ============================================================
-- 1. Les users
-- ============================================================
INSERT INTO users (id, username, password_hash, display_name, bio, is_admin, is_profile_public, created_at) VALUES
(1, 'admin', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Administrateur', 'Je suis le chef ici.', 1, 0, '2024-01-01'),
(2, 'cazauxl', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Loris C.', 'Pâtes lover.', 0, 1, '2024-01-02'),
(3, 'totol', 'scrypt:32768:8:1$pAZUUfJqyS73WKaX$1aea27b35b990e2a3a56bb43cadb267c82d9cd338444548e9e820ffdc311a4dcf0755198b0b94be83b0f8279289fccf5a1f11ee8e0ef7d2e6809bbc4486e5122', 'Toto', 'La beauté du geste.', 0, 1, '2024-01-03'),
(4, 'serazina', 'scrypt:32768:8:1$3YvMDrSEGQTzVUsT$36d269dd6dfc4d8a3edce81b12778c8c155dc769f878d9f3f10c8718e736a0b535ece691794bf284cb0bdc6ac3b467bd6bcee6ff94af34cdf0ab45a5d34e932c', 'Axel S.', 'Omelette master.', 0, 1, '2024-01-04'),
(5, 'chiqueta', 'scrypt:32768:8:1$QJCaIo8PFI9Hg4go$04284f87edabd3dbdd2f1985a0f765540a6dfe916c1d1765c142f3d0d1fce5763cc4b43cd4c814e90b7527956370337e2519838533477a4cdcc05fb38801069a', 'Aurélien', 'Explorateur culinaire.', 0, 0, '2024-01-05'),
(6, 'gordon_du_93', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Gordon R.', 'C''est CRU !!', 0, 1, '2024-01-15'),
(7, 'mamie_gateau', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Mamie Geo', 'Tout au beurre.', 0, 1, '2024-02-20'),
(8, 'fitboy_2000', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Kevin Fit', 'Manger bouger.', 0, 1, '2024-03-10'),
(9, 'vegan_warrior', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Lucie V.', 'Green life.', 0, 1, '2024-04-05'),
(10, 'le_gras_cest_la_vie', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Karadoc', 'Saucisson = Fruit.', 0, 1, '2024-05-12'),
(11, 'spicy_mama', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Maria P.', 'Caliente.', 0, 1, '2024-06-25'),
(12, 'sugar_rush', 'scrypt:32768:8:1$HJc17xMG8OlM0vAZ$ffdc096cdd33442e1b4cb236aa4c910dccea944877eb795b4b51dff5996b0df6b3e09451f6f30fe38ffa7ce6a3dfc39a0a4966cf190450e0d64a59c3c7afb992', 'Willy W.', 'Sucre pur.', 0, 1, '2024-07-30');

INSERT INTO ingredients (id, name) VALUES
(1, 'Carotte'), (2, 'Oignon'), (3, 'Oignon rouge'), (4, 'Échalote'), (5, 'Ail'), (6, 'Poireau'), (7, 'Pomme de terre'), (8, 'Patate douce'), (9, 'Courgette'), (10, 'Aubergine'),
(11, 'Poivron rouge'), (12, 'Poivron vert'), (13, 'Poivron jaune'), (14, 'Tomate'), (15, 'Tomates cerises'), (16, 'Concombre'), (17, 'Champignons de Paris'), (18, 'Épinards'), (19, 'Brocoli'), (20, 'Chou-fleur'),
(21, 'Salade verte'), (22, 'Roquette'), (23, 'Citron'), (24, 'Citron vert'), (25, 'Orange'), (26, 'Pomme'), (27, 'Poire'), (28, 'Banane'), (29, 'Fraise'), (30, 'Framboise'),
(31, 'Poulet'), (32, 'Blanc de poulet'), (33, 'Bœuf haché'), (34, 'Steak de bœuf'), (35, 'Lardons'), (36, 'Jambon'), (37, 'Saucisse'), (38, 'Saumon'), (39, 'Thon en boîte'), (40, 'Crevettes'),
(41, 'Œufs'), (42, 'Lait'), (43, 'Crème fraîche'), (44, 'Crème liquide'), (45, 'Beurre'), (46, 'Yaourt nature'), (47, 'Mozzarella'), (48, 'Parmesan'), (49, 'Gruyère râpé'), (50, 'Fromage de chèvre'),
(51, 'Farine de blé'), (52, 'Sucre en poudre'), (53, 'Sucre roux'), (54, 'Sel'), (55, 'Poivre noir'), (56, 'Huile d''olive'), (57, 'Huile de tournesol'), (58, 'Vinaigre balsamique'), (59, 'Vinaigre de vin rouge'), (60, 'Pâtes'),
(61, 'Riz basmati'), (62, 'Riz rond'), (63, 'Semoule'), (64, 'Boulgour'), (65, 'Quinoa'), (66, 'Pain de mie'), (67, 'Chapelure'), (68, 'Levure chimique'), (69, 'Levure boulangère'), (70, 'Miel'),
(71, 'Moutarde'), (72, 'Concentré de tomate'), (73, 'Coulis de tomate'), (74, 'Lait de coco'), (75, 'Sauce soja'), (76, 'Persil'), (77, 'Coriandre'), (78, 'Basilic'), (79, 'Thym'), (80, 'Romarin'),
(81, 'Origan'), (82, 'Ciboulette'), (83, 'Laurier'), (84, 'Paprika'), (85, 'Paprika fumé'), (86, 'Curry'), (87, 'Curcuma'), (88, 'Cumin'), (89, 'Gingembre frais'), (90, 'Piment rouge'),
(91, 'Piment d''Espelette'), (92, 'Cannelle'), (93, 'Noix de muscade');

-- ============================================================
-- 2. Les big recettes de bg ultime
-- ============================================================
INSERT INTO recipes (id, author_id, title, description, servings, prep_time_minutes, status, validated_by, validated_at, created_at) VALUES
(1, 2, 'Pâtes carbonara', 'Classique.', 2, 15, 'APPROVED', 1, '2025-01-01 12:00:00', '2025-01-01 10:00:00'),
(2, 3, 'Poulet miel citron', 'Sucré salé.', 4, 30, 'APPROVED', 1, '2025-01-02 09:00:00', '2025-01-01 11:30:00'),
(3, 4, 'Riz cantonais', 'Facile.', 3, 20, 'APPROVED', 1, '2025-01-01 16:00:00', '2025-01-01 14:00:00'),
(4, 5, 'Tarte aux pommes', 'Dessert.', 6, 45, 'APPROVED', 1, '2025-01-03 10:00:00', '2025-01-01 15:00:00'),
(5, 2, 'Soupe courgettes', 'Sain.', 4, 25, 'APPROVED', 1, '2025-01-01 18:00:00', '2025-01-01 17:00:00'),
(6, 1, 'Bœuf bourguignon', 'Mijoté.', 6, 180, 'APPROVED', 1, '2025-01-02 14:00:00', '2025-01-02 08:00:00'),
(7, 3, 'Guacamole', 'Apéro.', 2, 10, 'APPROVED', 1, '2025-01-02 10:00:00', '2025-01-02 09:30:00'),
(8, 4, 'Omelette', 'Rapide.', 1, 8, 'APPROVED', 1, '2025-01-03 11:00:00', '2025-01-02 12:00:00'),
(9, 5, 'Curry légumes', 'Végé.', 4, 35, 'APPROVED', 1, '2025-01-02 16:00:00', '2025-01-02 13:00:00'),
(10, 1, 'Brownies', 'Chocolat.', 8, 25, 'APPROVED', 1, '2025-01-04 09:00:00', '2025-01-02 15:00:00'),
(11, 3, 'Saumon moutarde', 'Poisson.', 2, 18, 'APPROVED', 1, '2025-01-03 10:30:00', '2025-01-03 09:00:00'),
(12, 4, 'Salade César', 'Fraicheur.', 2, 15, 'APPROVED', 1, '2025-01-03 12:00:00', '2025-01-03 10:00:00'),
(13, 5, 'Pizza maison', 'Italienne.', 3, 90, 'APPROVED', 1, '2025-01-03 18:00:00', '2025-01-03 11:00:00'),
(14, 1, 'Chili con carne', 'Epicé.', 5, 60, 'APPROVED', 1, '2025-01-05 10:00:00', '2025-01-03 16:00:00'),
(15, 2, 'Smoothie', 'Fruits.', 2, 5, 'APPROVED', 1, '2025-01-03 17:00:00', '2025-01-03 16:30:00'),
(16, 3, 'Gâteau yaourt', 'Enfance.', 6, 30, 'APPROVED', 1, '2025-01-04 14:00:00', '2025-01-04 10:00:00'),
(17, 4, 'Pâtes pesto', 'Etudiant.', 2, 12, 'APPROVED', 1, '2025-01-04 15:00:00', '2025-01-04 12:00:00'),
(18, 5, 'Crevettes ail', 'Tapas.', 3, 15, 'APPROVED', 1, '2025-01-05 12:00:00', '2025-01-05 09:00:00'),
(19, 2, 'Wraps poulet', 'Picnic.', 2, 20, 'APPROVED', 1, '2025-01-06 09:00:00', '2025-01-05 11:00:00'),
(20, 3, 'Purée', 'Maison.', 4, 35, 'APPROVED', 1, '2025-01-05 13:00:00', '2025-01-05 11:30:00'),
(21, 6, 'Lasagnes Bolognaise', 'Couches de bonheur.', 6, 90, 'APPROVED', 1, '2025-01-05 19:00:00', '2025-01-05 14:00:00'),
(22, 7, 'Blanquette de veau', 'A l''ancienne.', 4, 120, 'APPROVED', 1, '2025-01-07 10:00:00', '2025-01-05 16:00:00'),
(23, 8, 'Bowl Saumon Avocat', 'Healthy et frais.', 1, 15, 'APPROVED', 1, '2025-01-06 12:00:00', '2025-01-06 09:00:00'),
(24, 9, 'Dahl de lentilles', 'Indien vegan.', 4, 40, 'APPROVED', 1, '2025-01-06 14:00:00', '2025-01-06 10:00:00'),
(25, 10, 'Tartiflette', 'Beaucoup de fromage.', 6, 60, 'APPROVED', 1, '2025-01-06 18:00:00', '2025-01-06 11:00:00'),
(26, 11, 'Fajitas Poulet', 'Mexicain.', 4, 30, 'APPROVED', 1, '2025-01-07 12:00:00', '2025-01-07 08:00:00'),
(27, 12, 'Muffins Myrtilles', 'Gouter.', 12, 25, 'APPROVED', 1, '2025-01-07 15:00:00', '2025-01-07 09:00:00'),
(28, 6, 'Côte de bœuf', 'Au barbecue.', 2, 20, 'APPROVED', 1, '2025-01-08 09:00:00', '2025-01-07 13:00:00'),
(29, 7, 'Clafoutis Cerises', 'Saison.', 6, 45, 'APPROVED', 1, '2025-01-07 18:00:00', '2025-01-07 14:00:00'),
(30, 8, 'Omelette Blanc d''oeuf', 'Protéines pures.', 1, 5, 'APPROVED', 1, '2025-01-07 16:00:00', '2025-01-07 15:30:00'),
(31, 9, 'Steak de Soja', 'Fait maison.', 2, 20, 'APPROVED', 1, '2025-01-08 12:00:00', '2025-01-08 10:00:00'),
(32, 10, 'Sandwich Rosette', 'Simple et efficace.', 1, 5, 'APPROVED', 1, '2025-01-08 13:00:00', '2025-01-08 12:30:00'),
(33, 11, 'Chili Sin Carne', 'Version sans viande.', 4, 50, 'APPROVED', 1, '2025-01-09 10:00:00', '2025-01-08 14:00:00'),
(34, 12, 'Pancakes Sirop d''érable', 'Petit dej.', 4, 20, 'APPROVED', 1, '2025-01-09 09:30:00', '2025-01-09 08:00:00'),
(35, 6, 'Risotto Champignons', 'Crémeux.', 2, 35, 'APPROVED', 1, '2025-01-09 13:00:00', '2025-01-09 11:00:00'),
(36, 7, 'Pot-au-feu', 'Hiver.', 6, 180, 'APPROVED', 1, '2025-01-10 10:00:00', '2025-01-09 15:00:00'),
(37, 8, 'Poulet Vapeur', 'Sec mais efficace.', 1, 15, 'APPROVED', 1, '2025-01-10 11:00:00', '2025-01-10 09:00:00'),
(38, 9, 'Salade de fruits', 'Vitamines.', 4, 15, 'APPROVED', 1, '2025-01-10 12:00:00', '2025-01-10 10:00:00'),
(39, 10, 'Pâté en croûte', 'Apéro dinatoire.', 8, 90, 'APPROVED', 1, '2025-01-10 18:00:00', '2025-01-10 14:00:00'),
(40, 11, 'Curry Thaï Vert', 'Très pimenté.', 4, 40, 'APPROVED', 1, '2025-01-11 10:00:00', '2025-01-10 16:00:00'),
(42, 6, 'Filet Mignon', 'Moutarde.', 4, 45, 'APPROVED', 1, '2025-01-11 13:00:00', '2025-01-11 11:00:00'),
(43, 7, 'Hachis Parmentier', 'Restes.', 4, 40, 'APPROVED', 1, '2025-01-12 11:00:00', '2025-01-11 16:00:00'),
(44, 8, 'Shake Banane', 'Post-workout.', 1, 5, 'APPROVED', 1, '2025-01-12 10:00:00', '2025-01-12 09:30:00'),
(45, 9, 'Houmous', 'Pois chiches.', 4, 10, 'APPROVED', 1, '2025-01-12 14:00:00', '2025-01-12 11:00:00'),
(46, 10, 'Raclette', 'Fromage fondu.', 4, 20, 'APPROVED', 1, '2025-01-12 13:00:00', '2025-01-12 12:00:00'),
(47, 11, 'Nouilles sautées', 'Wok.', 2, 15, 'APPROVED', 1, '2025-01-12 20:00:00', '2025-01-12 18:00:00'),
(48, 12, 'Cheesecake', 'New York.', 8, 300, 'APPROVED', 1, '2025-01-13 09:00:00', '2025-01-12 19:00:00'),
(49, 2, 'Croque Monsieur', 'Béchamel.', 2, 15, 'APPROVED', 1, '2025-01-13 12:30:00', '2025-01-13 12:00:00'),
(50, 6, 'Burger de la mort', 'Gras.', 1, 30, 'APPROVED', 1, '2025-01-13 14:00:00', '2025-01-13 12:30:00'),
(51, 7, 'Salade Quinoa', 'Triste.', 2, 15, 'APPROVED', 1, '2025-01-13 18:00:00', '2025-01-13 13:00:00'),
(52, 8, 'Shake Masse', 'Poudre.', 1, 2, 'APPROVED', 1, '2025-01-14 09:00:00', '2025-01-14 08:30:00'),
(53, 9, 'Tofu braisé', 'Soya.', 4, 45, 'APPROVED', 1, '2025-01-14 12:00:00', '2025-01-14 10:00:00'),
(54, 10, 'Saucisson brioché', 'Lyon.', 6, 90, 'APPROVED', 1, '2025-01-14 15:00:00', '2025-01-14 11:00:00'),
(55, 6, 'Fish and Chips', 'Friture.', 4, 40, 'APPROVED', 1, '2025-01-14 16:00:00', '2025-01-14 13:00:00'),
(56, 7, 'Tarte Fraises', 'Fruit.', 8, 60, 'APPROVED', 1, '2025-01-14 17:00:00', '2025-01-14 14:00:00'),
(57, 11, 'Curry Vindaloo', 'Feu.', 4, 50, 'APPROVED', 1, '2025-01-15 09:00:00', '2025-01-14 16:00:00'),
(58, 12, 'Cookies XXL', 'Gras.', 12, 25, 'APPROVED', 1, '2025-01-14 18:00:00', '2025-01-14 17:00:00'),
(59, 8, 'Meal Prep', 'Riz Dinde.', 5, 120, 'APPROVED', 1, '2025-01-15 08:00:00', '2025-01-15 07:00:00'),
(60, 9, 'Soupe Potiron', 'Hiver.', 4, 40, 'APPROVED', 1, '2025-01-15 10:00:00', '2025-01-15 09:00:00'),
(61, 6, 'Boeuf Wellington', 'Luxe.', 4, 180, 'APPROVED', 1, '2025-01-15 12:00:00', '2025-01-15 10:00:00'),
(62, 10, 'Raclette Bowl', 'Rapide.', 1, 10, 'REJECTED', 1, '2025-01-15 11:30:00', '2025-01-15 11:00:00'),
(63, 11, 'Tacos Mexicains', 'Spicy.', 4, 30, 'APPROVED', 1, '2025-01-15 13:30:00', '2025-01-15 12:30:00'),
(64, 7, 'Gâteau Roulé', 'Maman.', 6, 45, 'APPROVED', 1, '2025-01-15 15:00:00', '2025-01-15 14:00:00'),
(65, 8, 'Omelette blanche', 'Diet.', 1, 5, 'APPROVED', 1, '2025-01-15 15:30:00', '2025-01-15 15:15:00'),
(66, 12, 'Bûche Glacée', 'Fête.', 8, 20, 'APPROVED', 1, '2025-01-15 17:00:00', '2025-01-15 16:00:00'),
(67, 10, 'Foie Gras', 'Riche.', 10, 2400, 'APPROVED', 1, '2025-01-15 18:00:00', '2025-01-15 17:00:00'),
(68, 6, 'Dinde Marrons', 'Noel.', 6, 240, 'APPROVED', 1, '2025-01-15 19:00:00', '2025-01-15 18:00:00'),
(69, 9, 'Detox Juice', 'Vert.', 1, 5, 'APPROVED', 1, '2025-01-15 19:30:00', '2025-01-15 19:00:00'),
(70, 8, 'Salade Light', 'Eau.', 1, 10, 'APPROVED', 1, '2025-01-15 20:00:00', '2025-01-15 19:45:00'),
(71, 7, 'Galette Rois', 'Fève.', 8, 60, 'APPROVED', 1, '2025-01-15 21:00:00', '2025-01-15 20:00:00');

-- ============================================================
-- 3. FULL RANDOM SUR LES STATUS (pas cohérent avec les dates de validation mais osef)
-- ============================================================
UPDATE recipes
SET status = CASE
    WHEN ABS(RANDOM()) % 100 < 5 THEN 'REJECTED'          -- 5% de refusés
    WHEN ABS(RANDOM()) % 100 < 15 THEN 'CHANGES_REQUIRED' -- 10% de modifs
    WHEN ABS(RANDOM()) % 100 < 30 THEN 'PENDING'          -- 15% en attente
    ELSE 'APPROVED'                                       -- 70% validés
END;

-- ============================================================
-- 4. Remplissage (STEPS & INGREDIENTS)
-- ============================================================
INSERT INTO recipe_steps (recipe_id, step_number, content) SELECT id, 1, 'Préparer tous les ingrédients.' FROM recipes;
INSERT INTO recipe_steps (recipe_id, step_number, content) SELECT id, 2, 'Cuisiner avec amour.' FROM recipes;
INSERT INTO recipe_steps (recipe_id, step_number, content) SELECT id, 3, 'Servir immédiatement.' FROM recipes;
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) SELECT id, 54, '1 pincée' FROM recipes;
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) SELECT id, 56, '1 filet' FROM recipes;
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) SELECT id, (ABS(RANDOM()) % 90) + 1, '200g' FROM recipes;


-- ============================================================
-- 5. INJECTION DE BUZZ "CHAOS THEORY" (VRAIE DISPARITÉ)
-- ============================================================

-- A. LES FAVORIS (Grosse disparité)
INSERT INTO favorites (user_id, recipe_id, created_at)
SELECT u.id, r.id, DATETIME('now', '-' || (ABS(RANDOM()) % 300) || ' days')
FROM users u
CROSS JOIN recipes r
WHERE (ABS(RANDOM()) % 100) < ((r.id * 17) % 90);


-- B. LES COMMENTAIRES (Vrais avis de la street)
-- On utilise un CASE énorme pour varier les textes
INSERT INTO comments (recipe_id, user_id, content, created_at)
SELECT r.id, u.id,
    CASE (ABS(RANDOM()) % 16)
        WHEN 0 THEN 'Franchement ? Une tuerie.'
        WHEN 1 THEN 'Validé par la street.'
        WHEN 2 THEN 'C''est fade, faut mettre du sel wesh.'
        WHEN 3 THEN 'Masterclass chef !'
        WHEN 4 THEN 'Banger absolu.'
        WHEN 5 THEN 'J''ai failli vomir, désolé.'
        WHEN 6 THEN 'Ma grand-mère fait mieux les yeux fermés.'
        WHEN 7 THEN 'Incroyable, je mets ça dans mes favoris direct.'
        WHEN 8 THEN 'Le poulet est CRU !!! Gordon va te tuer.'
        WHEN 9 THEN 'Simple, basique, efficace.'
        WHEN 10 THEN 'C''est carré dans l''axe.'
        WHEN 11 THEN 'Trop gras, j''aime ça.'
        WHEN 12 THEN 'La photo donne faim de ouf.'
        WHEN 13 THEN 'Recette claquée au sol.'
        WHEN 14 THEN 'A tester ce week-end !'
        ELSE 'Mouais, pas convaincu.'
    END,
    DATETIME('now', '-' || (ABS(RANDOM()) % 300) || ' days')
FROM users u
CROSS JOIN recipes r
WHERE (ABS(RANDOM()) % 100) < (((r.id * 23) % 80) / 1.5);


-- C. LES COMMENTAIRES "SCRIPTÉS" (Pour le lore)
INSERT INTO comments (recipe_id, user_id, content) VALUES
(66, 2, 'INCROYABLE !!!'),
(66, 3, 'Masterclass, je valide fort.'),
(66, 4, 'Je pleure c est trop bon, merci chef.'),
(50, 6, 'LE GRAS C EST LA VIE !'),
(61, 6, 'Enfin de la vraie cuisine, bravo.'),
(51, 8, 'Parfait pour la sèche, merci !'),
(62, 5, 'C''est n''importe quoi cette raclette...');


-- D. LES RATINGS (NOTES)
INSERT INTO ratings (user_id, recipe_id, rating, created_at)
SELECT
    u.id,
    r.id,
    CASE
        WHEN r.id = 66 THEN 5 -- La buche : 5/5 obligé
        WHEN r.id = 50 THEN 4 -- Le burger : 4/5
        WHEN r.id = 51 THEN 2 -- La salade triste : 2/5
        WHEN r.id % 2 = 0 THEN (ABS(RANDOM()) % 3) + 3 -- Entre 3 et 5
        ELSE (ABS(RANDOM()) % 5) + 1 -- Entre 1 et 5 (Chaos total)
    END,
    DATETIME('now', '-' || (ABS(RANDOM()) % 300) || ' days')
FROM users u
CROSS JOIN recipes r
WHERE (ABS(RANDOM()) % 100) < 40;