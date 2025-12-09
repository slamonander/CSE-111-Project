from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app)
DB_PATH = "plants.db"

# -----------------------------
# Helper function
# -----------------------------
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


# -----------------------------
# Get full plant list
# -----------------------------
@app.route("/plants")
def get_plants():
    plants = query_db("""
        SELECT p.plant_id, p.name, l.light_type, w.watering_type, h.humidity_type
        FROM Plants p
        LEFT JOIN Light l ON p.light_id = l.light_id
        LEFT JOIN Watering w ON p.watering_id = w.watering_id
        LEFT JOIN Humidity h ON p.humidity_id = h.humidity_id
        ORDER BY p.name ASC
    """)
    return jsonify([dict(p) for p in plants])


# -----------------------------
# Plant details by ID
# -----------------------------
@app.route("/plants/<int:plant_id>")
def plant_details(plant_id):
    plant = query_db("""
        SELECT p.name, l.light_type, w.watering_type, h.humidity_type,
               t.temperature_type, f.fertilizer_type, pr.pruning_type, pg.propagation_type
        FROM Plants p
        LEFT JOIN Light l ON p.light_id = l.light_id
        LEFT JOIN Watering w ON p.watering_id = w.watering_id
        LEFT JOIN Humidity h ON p.humidity_id = h.humidity_id
        LEFT JOIN Temperature t ON p.temperature_id = t.temperature_id
        LEFT JOIN Fertilizer f ON p.fertilizer_id = f.fertilizer_id
        LEFT JOIN Pruning pr ON p.pruning_id = pr.pruning_id
        LEFT JOIN Propagation pg ON p.propagation_id = pg.propagation_id
        WHERE p.plant_id = ?
    """, (plant_id,), one=True)

    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    return jsonify(dict(plant))


# -----------------------------
# Search plants by name
# -----------------------------
@app.route("/search")
def search_plants():
    term = request.args.get("name", "")
    plants = query_db("""
        SELECT plant_id, name, l.light_type, w.watering_type, h.humidity_type
        FROM Plants p
        LEFT JOIN Light l ON p.light_id = l.light_id
        LEFT JOIN Watering w ON p.watering_id = w.watering_id
        LEFT JOIN Humidity h ON p.humidity_id = h.humidity_id
        WHERE p.name LIKE ?
    """, (f"%{term}%",))

    return jsonify([dict(p) for p in plants])


# -----------------------------
# Add a favorite plant
# -----------------------------
@app.route("/favorite/<int:plant_id>", methods=["POST"])
def favorite_plant(plant_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO Favorites (user_id, plant_id) VALUES (?, ?)", (1, plant_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Plant added to favorites!"})


# -----------------------------
# Filter plants
# -----------------------------
@app.route("/filter")
def filter_plants():
    light = request.args.get("light")
    water = request.args.get("water")
    humidity = request.args.get("humidity")

    plants = query_db("""
        SELECT p.plant_id, p.name, l.light_type, w.watering_type, h.humidity_type
        FROM Plants p
        LEFT JOIN Light l ON p.light_id = l.light_id
        LEFT JOIN Watering w ON p.watering_id = w.watering_id
        LEFT JOIN Humidity h ON p.humidity_id = h.humidity_id
        WHERE (? IS NULL OR l.light_type = ?)
          AND (? IS NULL OR w.watering_type = ?)
          AND (? IS NULL OR h.humidity_type = ?)
        ORDER BY p.name ASC
    """, (
        light, light,
        water, water,
        humidity, humidity
    ))

    return jsonify([dict(p) for p in plants])


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/watering-types")
def get_watering_types():
    types = query_db("SELECT DISTINCT watering_type FROM Watering ORDER BY watering_type ASC")
    return jsonify([t["watering_type"] for t in types if t["watering_type"]])

# Get all favorites for user 1
@app.route("/favorites")
def get_favorites_endpoint():
    favorites = query_db("""
        SELECT p.plant_id, p.name
        FROM Favorites f
        JOIN Plants p ON f.plant_id = p.plant_id
        WHERE f.user_id = 1
    """)
    return jsonify([dict(p) for p in favorites])

# Remove a favorite
@app.route("/favorite/<int:plant_id>", methods=["DELETE"])
def remove_favorite(plant_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM Favorites WHERE user_id = 1 AND plant_id = ?", (plant_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Plant removed from favorites!"})
