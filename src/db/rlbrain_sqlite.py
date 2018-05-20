from .rlbrain_db_interface import rlbrain_db_interface
from os.path import isfile, getsize, abspath

class rlbrain_sqlite(rlbrain_db_interface):

    def _is_sqlite3(self, path):
        """
        Checks if the file at the given path is an sqlite3 database.
        Assumes the file exists.

        :param path: Path to the file.
        :return True if an sqlite3 db, False otherwise
        """
        if getsize(path) < 100: # SQLite header is 100 bytes
            return False

        with open(path, 'rb') as fd:
            header = fd.read(100)

        return header[:16] == 'SQLite format 3\x00'


    def _init_db(self):
        """
        Creates or connects to the sqlite db located at the given path.

        :return None
        """
        if isfile(self._db_path):
            if not self._is_sqlite3(self._db_path):
                err = 'File "{}" exists but is not an sqlite database.'.format(
                    abspath(self._db_path))
                self._logger.error(err)
                raise ValueError(err)


    def __init__(self, db_path):
        """
        Creates a new sqlite database if one is not found at db_path.
        The db schema is then applied by _init_db

        :param db_path: Path to the existing/desired sqlite database
        :return None
        """
        self._db_path = db_path
        self._init_logger()
        self._init_db()