---Testing with fake value
INSERT INTO user (username, email, password) 
VALUES 
('John ', 'nameisjohn@gmail.com', 'password123'),
('Lixin', 'lixin@gmail.com', 'imnotshowing');

--Add real place 
INSERT INTO restaurant (restaurant_name, location, cuisine, is_halal, min_price, max_price) 
VALUES 
('KFC','Edusphere DT Cyberjaya','Fast Food', 1, 10, 30),
('Secret Recipe', 'Shaftbury Square', 'Cafe', 1, 15, 40),
('Glaze Eatery', 'Tamarind Square', 'Western', 1, 20, 40),
('Canton Boy', 'Dpulze Shopping Centre', 'Chinese', 1, 10, 25);

--Sample post
--Link user1(John) to restaurant1(KFC)
INSERT INTO post (user_id, restaurant_id, title, description, image) 
VALUES
(1, 1, 'Finger Lickin Good Chicken!', 'I really enjoyed the crispy chicken at KFC. Highly recommend!', 'kfc_chicken.jpg'),
(1, 2, 'Delicious Cakes', 'A must-try for dessert lovers!', 'secret_recipe_cakes.jpg'),
(2, 3, 'Great Ambience', 'Glaze Eatery has a cozy atmosphere and tasty food.', 'glaze_eatery.jpg');

--Sample review
--Link user2(Lixin) to post1(John's post about KFC)
INSERT INTO review (user_id, restaurant_id, post_id, rating, comment)
VALUES
(2,1,1,5,'I agree! The chicken at KFC is amazing!'),
(2,2,2,4,'The cakes at Secret Recipe are delicious but a bit pricey.'),
(1,3,3,4,'Glaze Eatery has a nice vibe and good food. Will visit again!');


SELECT * FROM restaurant;