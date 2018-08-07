"""Replays
RocketLeagueReplays API module
"""
import requests

BASE_URL = 'https://www.rocketleaguereplays.com/api/replays/?page='


def get_replays(page_num):
    """
    Requests a page of replay data from the RocketLeagueReplaysAPI

    :param page_num: Page number to request
    :return: list of matches returned
    """
    url = f'{BASE_URL}{page_num}'
    result = requests.get(url).json()
    matches = result['results']
    return matches
