from string import Template

CREATE_PLAYERS_TABLE = '''CREATE TABLE players
    (id varchar(50) PRIMARY KEY, platform INT, wins INT, goals INT,
    mvps INT, saves INT, shots INT, assists INT);'''

SAVE_PLAYER = Template('INSERT INTO players\n'
                       'VALUES($id, $platform, $wins, $goals, $mvps, $saves, $shots, $assists);')

CREATE_MATCHES_TABLE = '''CREATE TABLE matches
    (id varchar(50) PRIMARY KEY, winner INT);'''

SAVE_MATCH = Template('INSERT INTO matches\n'
                      'VALUES($id, $winnder);')

CREATE_TEAMS_TABLE_SQLITE = '''CREATE TABLE teams 
    (id varchar(50) PRIMARY KEY, player_0 varchar(50), player_1 varchar(50),
    player_2 varchar(50), match varchar(50), team INT,
    FOREIGN KEY(player_0) REFERENCES players(id),
    FOREIGN KEY(player_1) REFERENCES players(id),
    FOREIGN KEY(player_2) REFERENCES players(id),
    FOREIGN KEY(match) REFERENCES matches(id));'''

SAVE_TEAM = Template('INSERT INTO teams\n'
                     'VALUES $id, $player_0, $player_1, $player_2, $match, $team')