import logging
import argparse
import sys

from utils import logger_factory

def init_logging(verbose):
    """
    Sets up the basic logging configuration and gets a logger for this module

    :return new Logger object for this module
    """
    log_format = '%(asctime)s %(name)s:%(levelname)s - %(message)s'

    logging.basicConfig(format=log_format, filename='rlbrain_data_scraper.log')

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

    try:
        repo = get_database(args.database)
    except ValueError as value_err:
        print(str(value_err) + ' Exiting.')
        logger.info('Exception encountered. Terminating early.')
        sys.exit()


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
    
    return parser.parse_args()


def main():
    """
    Main function.

    :return None
    """
    args = parse_arguments()
    run(args)


if __name__ == '__main__':
    main()