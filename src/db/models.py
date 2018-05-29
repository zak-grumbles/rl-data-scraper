from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    team_0_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    team_1_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    team_0 = relationship('Team', foreign_keys=[team_0_id])
    team_1 = relationship('Team', foreign_keys=[team_1_id])
    winner = Column(Integer, nullable=False)


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    platform = Column(Integer)
    wins = Column(Integer)
    goals = Column(Integer)
    mvps = Column(Integer)
    shots = Column(Integer)
    assists = Column(Integer)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    player_1_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    player_2_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    player_3_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    player_1 = relationship('Player', foreign_keys=[player_1_id])
    player_2 = relationship('Player', foreign_keys=[player_2_id])
    player_3 = relationship('Player', foreign_keys=[player_3_id])

