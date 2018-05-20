"""interfaces

A set of interfaces used for interacting with rl-brain databases.
"""

from utils import logger_factory

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

    def _is_sqlite3(self, path):
        """Check if a given file is an sqlite3 database

        Checks if the file at the given path is an sqlite3 database.
        Assumes the file exists.

        :param path: Path to the file.
        :return True if an sqlite3 db, False otherwise
        """
        from os.path import getsize

        if getsize(path) < 100: # SQLite header is 100 bytes
            return False

        with open(path, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == 'SQLite format 3\x00'


    def _init_db(self):
        """Initialize the database

        Creates or connects to the sqlite db located at the given path.

        :return None
        """
        from os.path import isfile, abspath

        if isfile(self._db_path):
            if not self._is_sqlite3(self._db_path):
                err = 'File "{}" exists but is not an sqlite database.'.format(
                    abspath(self._db_path))
                self._logger.error(err)
                raise ValueError(err)


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