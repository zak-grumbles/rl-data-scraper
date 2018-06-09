"""models

    Contains definitions for database models
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Match(Base):
    """
    Definition of the matches table. Represents a single 3v3 match of rocket league.
    """
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    team_0_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team_1_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team_0 = relationship('Team', foreign_keys=[team_0_id])
    team_1 = relationship('Team', foreign_keys=[team_1_id])
    winner = Column(Integer, nullable=False)


class Player(Base):
    """
    Definition of the players table. Represents a RocketLeague player.
    """
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    platform = Column(Integer)
    wins = Column(Integer)
    goals = Column(Integer)
    mvps = Column(Integer)
    saves = Column(Integer)
    shots = Column(Integer)
    assists = Column(Integer)

    def __init__(self, json_data):
        self.id = json_data['id']

        # not mapped
        self.team = json_data['team']
        if json_data['platform'] == '1':
            self.online_id = json_data['online_id']
        else:
            self.online_id = json_data['player_name']

        self.platform = int(json_data['platform'])

    def update_stats(self, stats):
        self.wins = stats['wins']
        self.goals = stats['goals']
        self.mvps = stats['mvps']
        self.saves = stats['saves']
        self.shots = stats['shots']
        self.assists = stats['assists']


class Team(Base):
    """
    Definition of the teams table. Represents a team in a 3v3 match of RocketLeague
    """
    __tablename__ = 'teams'

    id = Column(String(32), primary_key=True)
    player_1_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player_2_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player_3_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player_1 = relationship('Player', foreign_keys=[player_1_id])
    player_2 = relationship('Player', foreign_keys=[player_2_id])
    player_3 = relationship('Player', foreign_keys=[player_3_id])

    def __init__(self, team_array):
        from uuid import uuid4

        self.id = str(uuid4())

        self.player_1_id = team_array[0].id
        self.player_2_id = team_array[1].id
        self.player_3_id = team_array[2].id
