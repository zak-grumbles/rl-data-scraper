"""Stats
RocketLeagueStats API module
"""
import requests

BASE_URL = 'https://api.rocketleaguestats.com/v1/player/batch'


def get_player_stats(players, key):
    """
    Gets the stats for a batch of rocket league players.

    :param players: List of 6 players
    :param key: API authorization key
    :return: Player stats
    """
    headers = {'Authorization': key}
    payload = []
    for player in players:
        if player['platform'] == '1':
            payload.append({'platformId': player['platform'], 'uniqueId': player['online_id']})
        else:
            payload.append({'platformId': player['platform'], 'uniqueId': player['player_name']})

    stats = requests.post(BASE_URL, headers=headers, json=payload)
    return stats.json()
