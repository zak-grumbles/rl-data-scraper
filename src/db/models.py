"""models

    Contains definitions for database models
"""

from sqlalchemy import Column, ForeignKey, Integer
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
    shots = Column(Integer)
    assists = Column(Integer)


class Team(Base):
    """
    Definition of the teams table. Represents a team in a 3v3 match of RocketLeague
    """
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    player_1_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player_2_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player_3_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player_1 = relationship('Player', foreign_keys=[player_1_id])
    player_2 = relationship('Player', foreign_keys=[player_2_id])
    player_3 = relationship('Player', foreign_keys=[player_3_id])

