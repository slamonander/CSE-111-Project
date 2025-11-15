CREATE TABLE Plants (
    plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,

    light_id INTEGER,
    watering_id INTEGER,
    humidity_id INTEGER,
    temperature_id INTEGER,
    fertilizer_id INTEGER,
    pruning_id INTEGER,
    propagation_id INTEGER,

    FOREIGN KEY (light_id) REFERENCES Light(light_id),
    FOREIGN KEY (watering_id) REFERENCES Watering(watering_id),
    FOREIGN KEY (humidity_id) REFERENCES Humidity(humidity_id),
    FOREIGN KEY (temperature_id) REFERENCES Temperature(temperature_id),
    FOREIGN KEY (fertilizer_id) REFERENCES Fertilizer(fertilizer_id),
    FOREIGN KEY (pruning_id) REFERENCES Pruning(pruning_id),
    FOREIGN KEY (propagation_id) REFERENCES Propagation(propagation_id)
);

CREATE TABLE Light (
    light_id INTEGER PRIMARY KEY AUTOINCREMENT,
    light_type TEXT UNIQUE NOT NULL
);

CREATE TABLE Watering (
    watering_id INTEGER PRIMARY KEY AUTOINCREMENT,
    watering_type TEXT UNIQUE NOT NULL
);

CREATE TABLE Humidity (
    humidity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    humidity_type TEXT UNIQUE NOT NULL
);

CREATE TABLE Temperature (
    temperature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature_type TEXT UNIQUE NOT NULL
);

CREATE TABLE Fertilizer (
    fertilizer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fertilizer_type TEXT UNIQUE NOT NULL
);

CREATE TABLE Pruning (
    pruning_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pruning_type TEXT UNIQUE NOT NULL
);

CREATE TABLE Propagation (
    propagation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    propagation_type TEXT UNIQUE NOT NULL
);

CREATE TABLE Notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER NOT NULL,
    note_text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
);

CREATE TABLE Favorites (
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plant_id INTEGER NOT NULL,
    FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
);