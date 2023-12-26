DROP TABLE IF EXISTS freethrowlog;

CREATE TABLE freethrowlog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessionDate TEXT NOT NULL,
    ftMade INTEGER NOT NULL,
    ftAttempted INTEGER NOT NULL
    
)