import sqlite3

# Connect to your database
conn = sqlite3.connect('/Users/georgeperez/Desktop/CSE111 Docker/project/plants.db')
cur = conn.cursor()

# -----------------------------
# Helper function
# -----------------------------
user_id=1

def get_or_create_id(table, column, value):
    if value is None:
        return None
    cur.execute(f"SELECT {table.lower()}_id FROM {table} WHERE {column} = ?", (value,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
    return cur.lastrowid

#Show all plants function only by name, not plant id
#SELECT plant_id, name..... if you want all ids and name
def show_all_plants():
    cur.execute("""
        SELECT DISTINCT(name) FROM Plants ORDER BY name ASC
    """)
    rows = cur.fetchall()
    for row in rows:
        print(row)
        
def get_favorites(user_id):
    cur.execute("""
        SELECT p.plant_id, p.name FROM Favorites f
        JOIN Plants p ON f.plant_id = p.plant_id
        WHERE f.user_id = ?
    """, (user_id,))
    return cur.fetchall()

def show_favorites(user_id):
    favorites = get_favorites(user_id)
    if not favorites:
        print("You have no favorite plants.")
        return
    print("\n--- Your Favorite Plants ---")
    for plant_id, name in favorites:
        print(f"{plant_id}: {name}")   

def search_plant_by_name_or_id(query):
    try:
        # If query is an integer, search by ID
        plant_id = int(query)
        cur.execute("SELECT plant_id, name FROM Plants WHERE plant_id = ?", (plant_id,))
    except ValueError:
        # Otherwise, search by name
        cur.execute("SELECT plant_id, name FROM Plants WHERE name LIKE ?", (f"%{query}%",))
    
    rows = cur.fetchall()
    if not rows:
        print("No plants found.")
    for row in rows:
        print(row)

def show_plant_info(plant_id):
    cur.execute("""
        SELECT p.name, l.light_type, w.watering_type, h.humidity_type,
               t.temperature_type, f.fertilizer_type, pr.pruning_type, pg.propagation_type,
               GROUP_CONCAT(n.note_text || ' [' || n.timestamp || ']', CHAR(10)) AS notes
        FROM Plants p
        JOIN Light l ON p.light_id = l.light_id
        JOIN Watering w ON p.watering_id = w.watering_id
        JOIN Humidity h ON p.humidity_id = h.humidity_id
        JOIN Temperature t ON p.temperature_id = t.temperature_id
        JOIN Fertilizer f ON p.fertilizer_id = f.fertilizer_id
        JOIN Pruning pr ON p.pruning_id = pr.pruning_id
        JOIN Propagation pg ON p.propagation_id = pg.propagation_id
        LEFT JOIN Notes n ON p.plant_id = n.plant_id
        WHERE p.plant_id = ?
        GROUP BY p.plant_id
    """, (plant_id,))
    
    row = cur.fetchone()
    if row:
        labels = ["Name", "Light", "Watering", "Humidity", "Temperature", "Fertilizer", "Pruning", "Propagation", "Notes"]
        for label, value in zip(labels, row):
            print(f"{label}: {value if value else 'None'}")
    else:
        print("Plant not found.")

def add_plant(name, light=None, watering=None, humidity=None, temperature=None,
              fertilizer=None, pruning=None, propagation=None):
    light_id = get_or_create_id('Light', 'light_type', light)
    watering_id = get_or_create_id('Watering', 'watering_type', watering)
    humidity_id = get_or_create_id('Humidity', 'humidity_type', humidity)
    temperature_id = get_or_create_id('Temperature', 'temperature_type', temperature)
    fertilizer_id = get_or_create_id('Fertilizer', 'fertilizer_type', fertilizer)
    pruning_id = get_or_create_id('Pruning', 'pruning_type', pruning)
    propagation_id = get_or_create_id('Propagation', 'propagation_type', propagation)

    cur.execute("""
        INSERT INTO Plants (name, light_id, watering_id, humidity_id, temperature_id,
                            fertilizer_id, pruning_id, propagation_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, light_id, watering_id, humidity_id, temperature_id, fertilizer_id, pruning_id, propagation_id))
    conn.commit()
    print(f"Added plant: {name}")

def edit_plant(plant_id, **updates):
    print("Leave blank any attribute you don't want to change.")
    name = input("Name: ").strip() or None
    light = input("Light: ").strip() or None
    watering = input("Watering: ").strip() or None
    humidity = input("Humidity: ").strip() or None
    temperature = input("Temperature: ").strip() or None
    fertilizer = input("Fertilizer: ").strip() or None
    pruning = input("Pruning: ").strip() or None
    propagation = input("Propagation: ").strip() or None
    updates = {}
    if name: updates["name"] = name
    if light: updates["light_id"] = get_or_create_id('Light', 'light_type', light)
    if watering: updates["watering_id"] = get_or_create_id('Watering', 'watering_type', watering)
    if humidity: updates["humidity_id"] = get_or_create_id('Humidity', 'humidity_type', humidity)
    if temperature: updates["temperature_id"] = get_or_create_id('Temperature', 'temperature_type', temperature)
    if fertilizer: updates["fertilizer_id"] = get_or_create_id('Fertilizer', 'fertilizer_type', fertilizer)
    if pruning: updates["pruning_id"] = get_or_create_id('Pruning', 'pruning_type', pruning)
    if propagation: updates["propagation_id"] = get_or_create_id('Propagation', 'propagation_type', propagation)
    # Nothing to update
    if not updates:
        print("No changes made.")
        return
    # Build SQL dynamically
    set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
    values = list(updates.values())
    values.append(plant_id)
    cur.execute(f"UPDATE Plants SET {set_clause} WHERE plant_id = ?", values)
    conn.commit()
    print("Plant updated successfully!")

def delete_plant(plant_id):
    cur.execute("DELETE FROM Plants WHERE plant_id = ?", (plant_id,))
    conn.commit()
    print(f"Deleted plant ID {plant_id}")

def add_note(plant_id, note):
    cur.execute("INSERT INTO Notes (plant_id, note_text) VALUES (?, ?)", (plant_id, note))
    conn.commit()
    print("Note added.")

def show_notes(plant_id):
    cur.execute("SELECT note_id, note_text, timestamp FROM Notes WHERE plant_id = ? ORDER BY timestamp DESC", (plant_id,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def add_favorite(user_id, plant_id):
    cur.execute("INSERT INTO Favorites (user_id, plant_id) VALUES (?, ?)", (user_id, plant_id))
    conn.commit()
    print("Added to favorites.")

def remove_favorite(user_id, plant_id):
    cur.execute("DELETE FROM Favorites WHERE user_id = ? AND plant_id = ?", (user_id, plant_id))
    conn.commit()
    print("Removed from favorites.")

def show_favorites(user_id):
    cur.execute("""
        SELECT p.plant_id, p.name FROM Favorites f
        JOIN Plants p ON f.plant_id = p.plant_id
        WHERE f.user_id = ?
    """, (user_id,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def filter_plants(light=None, watering=None, humidity=None, temperature=None, fertilizer=None, pruning=None, propagation=None):
    query = """
    SELECT p.name, l.light_type, w.watering_type, h.humidity_type,
        t.temperature_type, f.fertilizer_type, pr.pruning_type, pg.propagation_type
    FROM Plants p
    JOIN Light l ON p.light_id = l.light_id
    JOIN Watering w ON p.watering_id = w.watering_id
    JOIN Humidity h ON p.humidity_id = h.humidity_id
    JOIN Temperature t ON p.temperature_id = t.temperature_id
    JOIN Fertilizer f ON p.fertilizer_id = f.fertilizer_id
    JOIN Pruning pr ON p.pruning_id = pr.pruning_id
    JOIN Propagation pg ON p.propagation_id = pg.propagation_id
    WHERE 1=1
    """    
    params = []
    filters = {
        "l.light_type": light,
        "w.watering_type": watering,
        "h.humidity_type": humidity,
        "t.temperature_type": temperature,
        "f.fertilizer_type": fertilizer,
        "pr.pruning_type": pruning,
        "pg.propagation_type": propagation
    }

    for col, val in filters.items():
        if val:
            query += f" AND {col} = ?"
            params.append(val)
        
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# -----------------------------
# Menu
# -----------------------------
def main_menu():
    while True:
        print("\n--- Plant Database Menu ---")
        print("1. Show all plants")
        print("2. Search plant by ID/Name")
        print("3. Show full info for a plant")
        print("4. Update Plant Database")
        print("5. Filter plants by care")
        print("6. Show Favorites")
        print("0. Exit")
        choice = input("Enter option: ").strip()

        if choice == "1":
            show_all_plants()

        elif choice == "2":
            plant_operations_menu()

        elif choice == "3":
            plant_id = input("Enter plant ID: ")
            show_plant_info(plant_id)

        elif choice == "4":
            database_management_menu()

        elif choice == "5":
            light = input("Filter by light (leave blank to skip): ").strip() or None
            watering = input("Filter by watering (leave blank to skip): ").strip() or None
            humidity = input("Filter by humidity (leave blank to skip): ").strip() or None
            temperature = input("Filter by temperature (leave blank to skip): ").strip() or None
            fertilizer = input("Filter by fertilizer (leave blank to skip): ").strip() or None
            pruning = input("Filter by pruning (leave blank to skip): ").strip() or None
            propagation = input("Filter by propagation (leave blank to skip): ").strip() or None
            filter_plants(light, watering, humidity, temperature, fertilizer, pruning, propagation)
            
        elif choice == "6":
            show_favorites(user_id)

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

def plant_operations_menu():
    query = input("Enter plant ID or name: ").strip()
    results = search_plant_by_name_or_id(query)
    if not results:
        return

    plant_id = results[0][0]  # take first match

    def show_menu():
        print("\n--- Plant Operations Menu ---")
        print("1. Show plant details")
        print("2. Add favorite")
        print("3. Remove favorite")
        print("4. Add note")
        print("5. Edit plant details")
        print("6. Delete plant")
        print("7. Back to main menu")
        print("0. End operations")

    def handle_choice(choice):
        if choice == "1":
            show_plant_info(plant_id)
        elif choice == "2":
            add_favorite(user_id, plant_id)
        elif choice == "3":
            remove_favorite(user_id, plant_id)
        elif choice == "4":
            note = input("Enter note: ")
            add_note(plant_id, note)
        elif choice == "5":
            name = input("New name (leave blank to skip): ").strip()
            if name:
                edit_plant(plant_id, name=name)
            else:
                print("No changes made.")
        elif choice == "6":
            confirm = input("Are you sure you want to delete this plant? (y/n) ").lower()
            if confirm == "y":
                delete_plant(plant_id)
                return "exit"
        elif choice == "7":
            return "back"
        elif choice == "0":
            exit()
        else:
            print("Invalid choice. Try again.")
        return None

    while True:
        show_menu()
        choice = input("Enter option: ").strip()
        result = handle_choice(choice)
        if result == "exit" or result == "back":
            break

def database_management_menu():
    while True:
        print("\n--- Database Management Menu ---")
        print("1. Add plant")
        print("2. Edit plant")
        print("3. Delete plant")
        print("4. Add favorite")
        print("5. Remove favorite")
        print("6. Add note")
        print("7. Back to main menu")
        print("0. End operations")
        choice = input("Enter option: ").strip()

        if choice == "1":
            name = input("Plant name: ")
            light = input("Light: ") or None
            watering = input("Watering: ") or None
            humidity = input("Humidity: ") or None
            temperature = input("Temperature: ") or None
            fertilizer = input("Fertilizer: ") or None
            pruning = input("Pruning: ") or None
            propagation = input("Propagation: ") or None
            add_plant(name, light, watering, humidity, temperature, fertilizer, pruning, propagation)

        elif choice == "2":
            plant_id = input("Plant ID to edit: ")
            name = input("New name (leave blank to skip): ") or None
            edit_plant(plant_id, name=name) if name else print("No changes made.")

        elif choice == "3":
            plant_id = input("Plant ID to delete: ")
            confirm = input("Are you sure? (y/n): ").lower()
            if confirm == "y":
                delete_plant(plant_id)

        elif choice == "4":
            plant_id = input("Plant ID to favorite: ")
            add_favorite(user_id, plant_id)

        elif choice == "5":
            plant_id = input("Plant ID to remove from favorites: ")
            remove_favorite(user_id, plant_id)

        elif choice == "6":
            plant_id = input("Plant ID to add note: ")
            note = input("Note: ")
            add_note(plant_id, note)

        elif choice == "7":
            break

        elif choice == "0":
            exit()

        else:
            print("Invalid choice. Try again.")

# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    main_menu()