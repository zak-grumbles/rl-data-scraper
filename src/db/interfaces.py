"""interfaces

A set of interfaces used for interacting with rl-brain databases.
"""

from . import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session


class RLBrainDBInterface:
    """Interface definition for rl-brain databases

    Interface for creating and interacting with
    an rl-brain database
    """

    def save_player(self, player):
        self._db_session.add(player)
        self._db_session.commit()

    def save_match(self, match):
        self._db_session.add(match)
        self._db_session.commit()

    def save_team(self, team):
        self._db_session.add(team)
        self._db_session.commit()

    def _init_logger(self):
        """
        Initializes the logger for this module

        :return None
        """
        #self._logger = logger_factory.make_logger(__name__)

    def __init__(self):
        self._db_session_maker = sessionmaker(bind=self._db_engine)
        self._db_session = session.DBSession()


class RLBrainSqliteDB(RLBrainDBInterface):
    """SQLite3 interface for rl-brain databases

    Interface for interacting/creating an sqlite3 rl-brain database
    """

    def __init__(self, db_path):
        """Constructor

        Creates a new sqlite database if one is not found at db_path.
        The db schema is then applied by _init_db

        :param db_path: Path to the existing/desired sqlite database
        :return None
        """
        self._init_logger()
        self._db_path = db_path
        self._engine = create_engine(f'sqlite:///{self._db_path}')
        models.Base.metadata.create_all(self._engine)
