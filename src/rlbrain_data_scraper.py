import logging
import argparse
import json
import time

from utils import logger_factory
from apis import replays, stats


def init_logging(verbose):
    """
    Sets up the basic logging configuration and gets a logger for this module

    :return new Logger object for this module
    """
    from os import path, makedirs

    if not path.exists('../logs'):
        makedirs('../logs')

    log_format = '%(asctime)s %(name)s:%(levelname)s - %(message)s'

    logging.basicConfig(format=log_format, filename='../logs/rlbrain_data_scraper.log')

    if verbose is True:
        return logger_factory.make_logger(__name__, logging.DEBUG)
    else:
        return logger_factory.make_logger(__name__)


def get_database(db_type):
    """
    Creates a new database object based on the given db_type

    :param db_type: string indicating what type of database to use
    :return an object that implements the rlbrain_database_interface
    """
    repo = None
    if db_type == 'sqlite':
        from db.interfaces import RLBrainSqliteDB

        db_path = input('SQLite DB path: ')
        repo = RLBrainSqliteDB(db_path)

    return repo


def run(args):
    """
    Runs the data scraper. Calls various apis and saves data out to the
    database.

    :param args: argparse Namespace containing command-line arguments
    :return None
    """
    init_logging(args.verbose)
    logger = logging.getLogger(__name__)
    logger.info('Starting...')

    conf = read_config(args.config)

    repo = get_database(args.database)

    matches = replays.get_replays(7100)

    for match in matches:
        from db.models import Match, Player, Team

        players = match['player_set']

        if len(players) is not 6:
            continue

        players_stats = stats.get_player_stats(players, conf['apis']['stats']['key'])

        team_0 = []
        team_1 = []
        players_to_save = []

        missing_player_stats = False
        for player in players:
            new_player = Player(player)

            if new_player.team == 0:
                team_0.append(new_player)
            else:
                team_1.append(new_player)

            if player['platform'] == '1':
                new_player_stats = [s for s in players_stats if s['uniqueId'] == player['online_id']]
            else:
                new_player_stats = [s for s in players_stats if s['displayName'] == player['player_name']]

            if len(new_player_stats) == 0:
                missing_player_stats = True
                break
            else:
                new_player.update_stats(new_player_stats[0]['stats'])
                players_to_save.append(new_player)

        if missing_player_stats:
            continue
        else:
            for p in players_to_save:
                repo.save_player(p)

        db_team_0 = Team(team_0)
        db_team_1 = Team(team_1)

        repo.save_team(db_team_0)
        repo.save_team(db_team_1)
        time.sleep(conf['apis']['stats']['delay'])


def parse_arguments():
    """
    Parses command line arguments and returns them

    :return Parsed arguments in an argparse Namespace object
    """
    parser = argparse.ArgumentParser(description='Data scraper for rl-brain')
    parser.add_argument('-n', '--num_matches', metavar='NumberOfMatches', type=int,
                        help='Number of matches to scrape.')
    parser.add_argument('-db', '--database', metavar='DBType', type=str,
                        default='sqlite', help='Type of database to use.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Enable verbose logging to the console.')
    parser.add_argument('-c', '--config', metavar='ConfigPath', type=str,
                        default='config.json', help='Path to config json file.')

    return parser.parse_args()


def read_config(path):
    with open(path) as config:
        conf_data = config.read()

    conf = json.loads(conf_data)
    return conf


def main():
    """
    Main function.

    :return None
    """
    args = parse_arguments()
    run(args)


if __name__ == '__main__':
    main()
