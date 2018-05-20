import logging
import argparse
import sys

from utils import logger_factory

def init_logging(verbose):
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
        from db import rlbrain_sqlite

        db_path = input('SQLite DB path: ')
        repo = rlbrain_sqlite.rlbrain_sqlite(db_path)

    return repo


def run(args):
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
    parser.add_argument('-v', '--verbose', action='store_true',
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