DROP TABLE IF EXISTS RouteCounty;
DROP TABLE IF EXISTS Segment;
DROP TABLE IF EXISTS Postmile;
DROP TABLE IF EXISTS Alignment;
DROP TABLE IF EXISTS Direction;
DROP TABLE IF EXISTS County;
DROP TABLE IF EXISTS Route;
DROP TABLE IF EXISTS temp_highways;

CREATE TABLE temp_highways (
    OBJECTID INTEGER,
    Route TEXT,
    RteSuffix TEXT,
    RouteS TEXT,
    PMRouteID TEXT,
    County TEXT,
    District INTEGER,
    PMPrefix TEXT,
    bPM REAL,
    ePM REAL,
    PMSuffix TEXT,
    bPMc REAL,
    ePMc REAL,
    bOdometer REAL,
    eOdometer REAL,
    AlignCode TEXT,
    RouteType TEXT,
    Direction TEXT,
    Shape_Length REAL
);

CREATE TABLE Route (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_number TEXT,
    pmrouteid TEXT,
    route_type TEXT
);

CREATE TABLE County (
    county_id INTEGER PRIMARY KEY AUTOINCREMENT,
    county_code TEXT UNIQUE,
    district INTEGER
);

CREATE TABLE Direction (
    direction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    direction_code TEXT UNIQUE
);

CREATE TABLE Alignment (
    alignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    align_code TEXT UNIQUE
);

CREATE TABLE Postmile (
    pm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pm_prefix TEXT,
    pm_suffix TEXT
);

-- Central table
CREATE TABLE Segment (
    segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    objectid INTEGER,
    route_id INTEGER,
    county_id INTEGER,
    direction_id INTEGER,
    alignment_id INTEGER,
    pm_id INTEGER,
    bPM REAL,
    ePM REAL,
    bOdometer REAL,
    eOdometer REAL,
    shape_length REAL,
    FOREIGN KEY(route_id) REFERENCES Route(route_id),
    FOREIGN KEY(county_id) REFERENCES County(county_id),
    FOREIGN KEY(direction_id) REFERENCES Direction(direction_id),
    FOREIGN KEY(alignment_id) REFERENCES Alignment(alignment_id),
    FOREIGN KEY(pm_id) REFERENCES Postmile(pm_id)
);

--POPULATE COMES AFTER ALL THE TABLES ARE MADE
--Populate route table
INSERT OR IGNORE INTO Route (route_number, pmrouteid, route_type)
SELECT DISTINCT Route, PMRouteID, RouteType
FROM temp_highways;

--Populate county table
INSERT OR IGNORE INTO County (county_code, district)
SELECT DISTINCT County, District
FROM temp_highways;

--Populate Direction table
INSERT OR IGNORE INTO Direction (direction_code)
SELECT DISTINCT Direction
FROM temp_highways;

--Populate alignment table
INSERT OR IGNORE INTO Alignment (align_code)
SELECT DISTINCT AlignCode
FROM temp_highways;

--Populate postmile table
INSERT OR IGNORE INTO Postmile (pm_prefix, pm_suffix)
SELECT DISTINCT PMPrefix, PMSuffix
FROM temp_highways;

--Populate segment table
INSERT INTO Segment (
    objectid, route_id, county_id, direction_id, alignment_id, pm_id,
    bPM, ePM, bOdometer, eOdometer, shape_length
)
SELECT
    t.OBJECTID,
    r.route_id,
    c.county_id,
    d.direction_id,
    a.alignment_id,
    p.pm_id,
    t.bPM,
    t.ePM,
    t.bOdometer,
    t.eOdometer,
    t.Shape_Length
FROM temp_highways t
JOIN Route r ON t.Route = r.route_number AND t.PMRouteID = r.pmrouteid
JOIN County c ON t.County = c.county_code
JOIN Direction d ON t.Direction = d.direction_code
JOIN Alignment a ON t.AlignCode = a.align_code
JOIN Postmile p ON t.PMPrefix = p.pm_prefix AND t.PMSuffix = p.pm_suffix;

--Drop the temp table
DROP TABLE temp_highways;

