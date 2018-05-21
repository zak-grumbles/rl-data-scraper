"""interfaces

A set of interfaces used for interacting with rl-brain databases.
"""

from utils import logger_factory
import sqlite3


class RLBrainDBInterface:
    """Interaface definition for rl-brain databases

    Interface for creating and interacting with
    an rl-brain database
    """

    def save_player(self, player):
        raise NotImplementedError('\'save_player\' method not implemented')

    def save_match(self, match):
        raise NotImplementedError('\'save_match\' method not implemented')

    def _init_logger(self):
        """
        Initializes the logger for this module

        :return None
        """
        self._logger = logger_factory.make_logger(__name__)


class RLBrainSqliteDB(RLBrainDBInterface):
    """SQLite3 interface for rl-brain databases

    Interface for interacting/creating an sqlite3 rl-brain database
    """

    def _create_tables(self):
        query = '''SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=\'{}\';'''

        self._cursor.execute(query.format('players'))
        names = self._cursor.fetchall()
        if len(names) == 0:
            from .queries import CREATE_PLAYERS_TABLE
            self._logger.info('players table not found. Creating...')
            self._cursor.execute(CREATE_PLAYERS_TABLE)
        else:
            self._logger.info('players table found.')

        self._cursor.execute(query.format('matches'))
        names = self._cursor.fetchall()
        if len(names) == 0:
            from .queries import CREATE_MATCHES_TABLE
            self._logger.info('matches table not found. Creating...')
            self._cursor.execute(CREATE_MATCHES_TABLE)
        else:
            self._logger.info('matches table found.')

        self._cursor.execute(query.format('teams'))
        names = self._cursor.fetchall()
        if len(names) == 0:
            from .queries import CREATE_TEAMS_TABLE_SQLITE
            self._logger.info('teams table not found. Creating...')
            self._cursor.execute(CREATE_TEAMS_TABLE_SQLITE)
        else:
            self._logger.info('teams table found.')

    def _init_db(self):
        """Initialize the database

        Creates or connects to the sqlite db located at the given path.

        :return None
        """

        self._conn = sqlite3.connect(self._db_path)
        self._cursor = self._conn.cursor()
        self._create_tables()

    def __init__(self, db_path):
        """Constructor

        Creates a new sqlite database if one is not found at db_path.
        The db schema is then applied by _init_db

        :param db_path: Path to the existing/desired sqlite database
        :return None
        """
        self._db_path = db_path
        self._init_logger()
        self._init_db()
