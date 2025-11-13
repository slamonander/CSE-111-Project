import sqlite3

# Connect to a file-based SQLite database
conn = sqlite3.connect("plants.db")  # <-- This creates 'plants.db' on disk
cursor = conn.cursor()

query = "SELECT * FROM Plant"
cursor.execute(query)  # <-- no extra tuple needed
results = cursor.fetchall()
print(results)
