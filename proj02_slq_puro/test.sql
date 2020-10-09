CREATE TABLE estacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    local TEXT NOT NULL,
    longitude TEXT NOT NULL,
    latitude TEXT NOT NULL);


CREATE TABLE sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    estacao INTEGER NOT NULL,
    FOREIGN KEY (estacao) REFERENCES estacao (id));
