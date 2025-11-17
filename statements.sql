--1)A user wants to know what kind of plants need less light
SELECT p.name, l.light_type, w.watering_type, h.humidity_type, t.temperature_type
FROM Plants p
JOIN Light l ON p.light_id = l.light_id
JOIN Watering w ON p.watering_id = w.watering_id
JOIN Humidity h ON p.humidity_id = h.humidity_id
JOIN Temperature t ON p.temperature_id = t.temperature_id
WHERE l.light_type IN ('Partial shade', 'Shade');

--2) User wants to favorite the plant Basil
INSERT INTO Favorites (user_id, plant_id)
VALUES (1, (SELECT plant_id FROM Plants WHERE name = 'Basil'));

--3) User wants to see all favorite plants
SELECT f.favorite_id, p.name, l.light_type, w.watering_type
FROM Favorites f
JOIN Plants p ON f.plant_id = p.plant_id
JOIN Light l ON p.light_id = l.light_id
JOIN Watering w ON p.watering_id = w.watering_id
WHERE f.user_id = 1;

--4)User wants to find a plant the doesnt need a lot of watering
SELECT p.name, w.watering_type
FROM Plants p
JOIN Watering w ON p.watering_id = w.watering_id
WHERE w.watering_type IN ('Low', 'Minimal', 'Infrequent');

--5)User wants to find plants that can be propogated by cutting
SELECT p.name, pg.propagation_type
FROM Plants p
JOIN Propagation pg ON p.propagation_id = pg.propagation_id
WHERE pg.propagation_type = 'Cuttings';

--6)User wants to find what kind of plants are good in low himidity
SELECT p.name, h.humidity_type
FROM Plants p
JOIN Humidity h ON p.humidity_id = h.humidity_id
WHERE h.humidity_type IN ('Low', 'Moderate');

--7) User wants to find detailed information on a single plant
SELECT p.name, l.light_type, w.watering_type, h.humidity_type,
       t.temperature_type, f.fertilizer_type, pr.pruning_type, 
       pg.propagation_type
FROM Plants p
JOIN Light l ON p.light_id = l.light_id
JOIN Watering w ON p.watering_id = w.watering_id
JOIN Humidity h ON p.humidity_id = h.humidity_id
JOIN Temperature t ON p.temperature_id = t.temperature_id
JOIN Fertilizer f ON p.fertilizer_id = f.fertilizer_id
JOIN Pruning pr ON p.pruning_id = pr.pruning_id
JOIN Propagation pg ON p.propagation_id = pg.propagation_id
WHERE p.name = 'Rosemary';

--8)user wants to search a plant by name
SELECT plant_id, name
FROM Plants
WHERE name LIKE '%' || :search || '%';

--9)User wants to display all plants in the database
SELECT plant_id, name
FROM Plants
ORDER BY name ASC;

--10)User wants to filter plants based on certain care
SELECT p.name, l.light_type, w.watering_type, h.humidity_type
FROM Plants p
JOIN Light l        ON p.light_id = l.light_id
JOIN Watering w     ON p.watering_id = w.watering_id
JOIN Humidity h     ON p.humidity_id = h.humidity_id
WHERE (:light IS NULL OR l.light_type = :light)
  AND (:water IS NULL OR w.watering_type = :water)
  AND (:humidity IS NULL OR h.humidity_type = :humidity);

--11)User wants to show the care infomration for a plant
SELECT p.name, l.light_type, w.watering_type, h.humidity_type,
       t.temperature_type, f.fertilizer_type, pr.pruning_type,
       pg.propagation_type
FROM Plants p
JOIN Light l        ON p.light_id = l.light_id
JOIN Watering w     ON p.watering_id = w.watering_id
JOIN Humidity h     ON p.humidity_id = h.humidity_id
JOIN Temperature t  ON p.temperature_id = t.temperature_id
JOIN Fertilizer f   ON p.fertilizer_id = f.fertilizer_id
JOIN Pruning pr     ON p.pruning_id = pr.pruning_id
JOIN Propagation pg ON p.propagation_id = pg.propagation_id
WHERE p.plant_id = :plant_id;

--12)User wants to update plant data
INSERT INTO Plants 
(name, light_id, watering_id, humidity_id, temperature_id, fertilizer_id, pruning_id, propagation_id)
VALUES (:name, :light_id, :watering_id, :humidity_id, :temperature_id, :fertilizer_id, :pruning_id, :propagation_id);

--13)User wants to edit plant data
UPDATE Plants
SET name = :name,
    light_id = :light_id,
    watering_id = :watering_id,
    humidity_id = :humidity_id,
    temperature_id = :temperature_id,
    fertilizer_id = :fertilizer_id,
    pruning_id = :pruning_id,
    propagation_id = :propagation_id
WHERE plant_id = :plant_id;

--14)User wants to delete plant data
DELETE FROM Plants
WHERE plant_id = :plant_id;

--15)User wants to favorite a specific plant
INSERT INTO Favorites (user_id, plant_id)
VALUES (:user_id, :plant_id);

--16)Show all favorites for a specific user (only 1 in this case, the local machine running it)
SELECT p.plant_id, p.name
FROM Favorites f
JOIN Plants p ON f.plant_id = p.plant_id
WHERE f.user_id = :user_id;

--17)User wants to add plant notes:
INSERT INTO Notes (plant_id, note_text)
VALUES (:plant_id, :note); 

--18)User wants to show notess for a plant
SELECT note_id, note_text, timestamp
FROM Notes
WHERE plant_id = :plant_id
ORDER BY timestamp DESC;

--19)User wants to remove plant from favorutes
DELETE FROM Favorites
WHERE user_id = :user_id
  AND plant_id = :plant_id;

--20)User wants to see plants and their notes
SELECT p.name, n.note_text, n.timestamp 
FROM Notes n
JOIN Plants p ON n.plant_id = p.plant_id
ORDER BY n.timestamp DESC;