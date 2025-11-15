--A user wants to know what kind of plants need less light
SELECT p.name, l.light_type, w.watering_type, h.humidity_type, t.temperature_type
FROM Plants p
JOIN Light l ON p.light_id = l.light_id
JOIN Watering w ON p.watering_id = w.watering_id
JOIN Humidity h ON p.humidity_id = h.humidity_id
JOIN Temperature t ON p.temperature_id = t.temperature_id
WHERE l.light_type IN ('Partial shade', 'Shade');