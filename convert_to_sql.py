import pandas as pd
import sqlite3

df = pd.read_csv("highway_network_lines.csv")

createDB = sqlite3.connect("highway.db")

df.to_sql("a_table", createDB, if_exists="replace", index=False)

createDB.close()
print("CSV imported to database.")