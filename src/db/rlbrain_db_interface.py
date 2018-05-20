from utils import logger_factory

class RLBrainDBInterface:
    """
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