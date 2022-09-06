--food data
INSERT INTO food (id, name, protein_gr, total_carbohydrate_gr, total_fat_gr, calcium_gr, potassium_gr, alcohol_gr, iron_gr, vitamin_a_gr, vitamin_c_gr, caffeine_gr, calories) VALUES (1, 'ground beef', '20.9', '0', '7', '10', '336', '0', '2', '14', '0', '0', '172');
INSERT INTO food (id, name, protein_gr, total_carbohydrate_gr, total_fat_gr, calcium_gr, potassium_gr, alcohol_gr, iron_gr, vitamin_a_gr, vitamin_c_gr, caffeine_gr, calories) VALUES (2, 'chickpeas', '8.9', '27.4', '2.6', '49', '291', '0', '3', '25', '1', '0', '164');
INSERT INTO food (id, name, protein_gr, total_carbohydrate_gr, total_fat_gr, calcium_gr, potassium_gr, alcohol_gr, iron_gr, vitamin_a_gr, vitamin_c_gr, caffeine_gr, calories) VALUES (3, 'long grain white rice raw', '7.1', '80', '0.7', '28', '115', '0', '1', '0', '0', '0', '365');
INSERT INTO food (id, name, protein_gr, total_carbohydrate_gr, total_fat_gr, calcium_gr, potassium_gr, alcohol_gr, iron_gr, vitamin_a_gr, vitamin_c_gr, caffeine_gr, calories) VALUES (4, 'apple with skin raw', '0.3', '13.8', '0.2', '6', '107', '0', '1', '55', '5', '0', '52');

--meals data
INSERT INTO meals (id, user_id, food_id, type, amount_gr) VALUES (4, 3, 1, 'lunch', '2');
INSERT INTO meals (id, user_id, food_id, type, amount_gr) VALUES (6, 3, 2, 'dinner', '3');
INSERT INTO meals (id, user_id, food_id, type, amount_gr) VALUES (9, 3, 2, 'breakfast', '100');
INSERT INTO meals (id, user_id, food_id, type, amount_gr) VALUES (10, 3, 1, 'breakfast', '100');
INSERT INTO meals (id, user_id, food_id, type, amount_gr) VALUES (11, 3, 4, 'breakfast', '100');

--users
INSERT INTO users (id, username, hash) VALUES (3, 'matias', 'pbkdf2:sha256:260000$uB50SMn1S8RCiC87$258f15e0569757e6de2b4e8ec268d943483c7674980caaea130b5ba4622f5c8c');
INSERT INTO users (id, username, hash) VALUES (4, 'pepito', 'pbkdf2:sha256:260000$ipOpe7HQSsFLTOws$7a81c8f92cb811106b6f328ed523527e500b75ecab57a46ef90a5bc49a7fa894');
