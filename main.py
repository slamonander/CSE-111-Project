import sqlite3

# Connect to your single database
conn = sqlite3.connect('/Users/georgeperez/Desktop/CSE111 Docker/project/plants.db')
cur = conn.cursor()

# Helper function: insert attribute or get existing ID
def get_or_create_id(table, column, value):
    if value is None:
        return None
    cur.execute(f"SELECT {table.lower()}_id FROM {table} WHERE {column} = ?", (value,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
    return cur.lastrowid

# Fetch all plants from the old giant table
cur.execute("SELECT * FROM Plant")  # Your old table
rows = cur.fetchall()

for row in rows:
    name = row[0]
    light = row[1]
    watering = row[2]
    humidity = row[3]
    temperature = row[4]
    fertilizer = row[5]
    pruning = row[6]
    propagation = row[7]
    note = row[8] if len(row) > 8 else None

    # Get or create IDs
    light_id = get_or_create_id('Light', 'light_type', light)
    watering_id = get_or_create_id('Watering', 'watering_type', watering)
    humidity_id = get_or_create_id('Humidity', 'humidity_type', humidity)
    temperature_id = get_or_create_id('Temperature', 'temperature_type', temperature)
    fertilizer_id = get_or_create_id('Fertilizer', 'fertilizer_type', fertilizer)
    pruning_id = get_or_create_id('Pruning', 'pruning_type', pruning)
    propagation_id = get_or_create_id('Propagation', 'propagation_type', propagation)

    # Insert into normalized Plants table
    cur.execute("""
        INSERT INTO Plants
        (name, light_id, watering_id, humidity_id, temperature_id, fertilizer_id, pruning_id, propagation_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, light_id, watering_id, humidity_id, temperature_id, fertilizer_id, pruning_id, propagation_id))
    plant_id = cur.lastrowid

    # Insert note if it exists
    if note and note.strip():
        cur.execute("INSERT INTO Notes (plant_id, note_text) VALUES (?, ?)", (plant_id, note.strip()))

# Commit all changes and close connection
conn.commit()
conn.close()

print("Migration complete!")