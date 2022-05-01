CREATE TABLE tournament_register (
    tournament_index INTEGER PRIMARY KEY AUTOINCREMENT,
    tournament_name TINYTEXT NOT NULL,
    tournament_path TINYTEXT NOT NULL,
    tournament_date INTEGER NOT NULL,
    match_code_root TINYTEXT NOT NULL UNIQUE,
    match_code_view TINYTEXT NOT NULL UNIQUE
);

CREATE TABLE tournament_info (
    tourn_idx INTEGER NOT NULL,
    round_count INTEGER DEFAULT 0   
);

/*
CREATE TABLE [IF NOT EXISTS] tmp.schools (
    school_idx INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TINYTEXT NOT NULL UNIQUE
);

CREATE TABLE [IF NOT EXISTS] tmp.players (
    player_idx INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TINYTEXT NOT NULL UNIQUE,
    school_idx INTEGER NOT NULL,
    FOREIGN KEY(school_idx) REFERENCES tmp.schools(school_idx),
    tourn_wins INTEGER DEFAULT 0,
    tourn_draws INTEGER DEFAULT 0,
    tourn_loss INTEGER DEFAULT 0,
    tourn_points INTEGER DEFAULT 0,
    white_count INTEGER DEFAULT 0,
    black_count INTEGER DEFAULT 0
);

CREATE TABLE [IF NOT EXISTS] tmp.matches (
    round_idx INTEGER NOT NULL,
    match_idx INTEGER NOT NULL,
    PRIMARY KEY (round_idx, match_idx),
    white_player_idx INTEGER NOT NULL,
    FOREIGN KEY(white_player_idx) REFERENCES tmp.players(player_idx),
    black_player_idx INTEGER NOT NULL,
    FOREIGN KEY(blackplayer_idx) REFERENCES tmp.players(player_idx),
    result TINYTEXT DEFAULT NULL,
    CONSTRAINT check_result CHECK (result IN ('white', 'black', 'draw'))
);
*/

