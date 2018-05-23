
CREATE_PLAYERS_TABLE = '''CREATE TABLE players
    (id varchar(50) PRIMARY KEY, platform INT, wins INT, goals INT,
    mvps INT, saves INT, shots INT, assists INT);'''

CREATE_MATCHES_TABLE = '''CREATE TABLE matches
    (id varchar(50) PRIMARY KEY, winner INT);'''

CREATE_TEAMS_TABLE_SQLITE = '''CREATE TABLE teams 
    (id varchar(50) PRIMARY KEY, player_0 varchar(50), player_1 varchar(50),
    player_2 varchar(50), match varchar(50), team INT,
    FOREIGN KEY(player_0) REFERENCES players(id),
    FOREIGN KEY(player_1) REFERENCES players(id),
    FOREIGN KEY(player_2) REFERENCES players(id),
    FOREIGN KEY(match) REFERENCES matches(id));'''