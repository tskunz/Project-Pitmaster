"""SQL schema: 5 tables for cook session data."""

CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS cook_sessions (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        meat_category TEXT NOT NULL,
        cut_type TEXT NOT NULL,
        weight_lbs REAL NOT NULL,
        thickness_inches REAL NOT NULL,
        equipment_type TEXT NOT NULL,
        smoker_temp_f REAL NOT NULL,
        target_temp_f REAL NOT NULL,
        dinner_time TEXT,
        altitude_ft REAL DEFAULT 0,
        wrap_type TEXT DEFAULT 'none',
        current_state TEXT DEFAULT 'setup',
        confidence TEXT DEFAULT 'low',
        weather_ambient_temp REAL,
        weather_wind_speed REAL,
        weather_humidity REAL,
        is_finished INTEGER DEFAULT 0,
        quality_rating TEXT,
        quality_notes TEXT DEFAULT ''
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS probe_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        temp_f REAL NOT NULL,
        smoker_temp_f REAL,
        elapsed_minutes REAL NOT NULL,
        FOREIGN KEY (session_id) REFERENCES cook_sessions(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS lid_open_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        duration_seconds REAL DEFAULT 30,
        FOREIGN KEY (session_id) REFERENCES cook_sessions(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS intervention_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        wrap_type TEXT NOT NULL,
        temp_at_wrap_f REAL NOT NULL,
        elapsed_minutes REAL NOT NULL,
        FOREIGN KEY (session_id) REFERENCES cook_sessions(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        p10_minutes REAL NOT NULL,
        p50_minutes REAL NOT NULL,
        p90_minutes REAL NOT NULL,
        confidence TEXT NOT NULL,
        current_state TEXT NOT NULL,
        stall_probability REAL DEFAULT 0,
        readings_count INTEGER DEFAULT 0,
        FOREIGN KEY (session_id) REFERENCES cook_sessions(id)
    )
    """,
]
