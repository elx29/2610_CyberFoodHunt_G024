
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

--Sample event
INSERT INTO event (event_id, user_id, event_name, event_location, description, start_date, end_date) 
VALUES
(1, 1, 'Ramadan Bazaar 2025',    'MMU Carpark Lot C', 'Daily bazaar from 4pm. Lots of local kuih!',   '2025-03-01', '2025-03-31'),
(2, 2, 'Street Food Truck Rally','Tamarind Square',   'Different food trucks every weekend. Free entry.','2025-04-10', '2025-04-13');

--Sample review
--Link user2(Lixin) to post1(John's post about KFC)
INSERT INTO review (user_id, restaurant_id, post_id, rating, comment)
VALUES
(2,1,1,5,'I agree! The chicken at KFC is amazing!'),
(2,2,2,4,'The cakes at Secret Recipe are delicious but a bit pricey.'),
(1,3,3,4,'Glaze Eatery has a nice vibe and good food. Will visit again!');

--Sample bookmark
INSERT INTO bookmark (user_id, restaurant_id)
VALUES
(1, 2),   -- John bookmarked Secret Recipe
(1, 3),   -- John bookmarked Glaze Eatery
(2, 1);   -- Lixin bookmarked KFC


SELECT 'Users' AS name, COUNT(*) FROM user
UNION ALL
SELECT 'Restaurants', COUNT(*) FROM restaurant
UNION ALL
SELECT 'Reviews', COUNT(*) FROM review
UNION ALL
SELECT 'Bookmarks', COUNT(*) FROM bookmark;

