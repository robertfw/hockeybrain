import os
import logging
from collections import defaultdict
from pprint import pprint

import bs4
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

config = {
    'play_by_play_url': 'http://www.nhl.com/scores/htmlreports/20122013/PL02{game_id:04d}.HTM',
    'play_by_play_dir': 'playbyplayreports'
}


def get_games(from_date=None, to_date=None):
    '''Returns a list of game ids'''
    pass


def retrieve_play_by_play_report(game_id):
    '''Gets stats for a given game id'''
    assert type(game_id) is int, "game_id must be an int"
    # TODO: check to see what game ids go up to
    assert game_id < 10000, "game id must be < 10000"

    url = config['play_by_play_url'].format(game_id=game_id)
    logger.info('making request to {url}'.format(url=url))
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Error retrieving game report')

    return response.content


def convert_raw_row_to_event(cells):
    return {
        'id': cells[0].text,
        'period': cells[1].text,
        'strength': cells[2].text,
        'time': cells[3].contents[0],
        'type': cells[4].text,
        'description': cells[5].text
    }


def convert_raw_report_to_events(report):
    '''parses an html play by play report'''
    soup = bs4.BeautifulSoup(report)

    return [convert_raw_row_to_event(row.find_all('td'))
            for table in soup.find_all('table')
            for row in table.find_all('tr')
            if 'evenColor' in row.attrs.get('class', [])]


def format_player_number(number):
    return number.replace('#', '')


def parse_miss(desc):
    bits = desc.split(',')

    team, number, player = bits[0].split(' ')

    return {
        'team': team,
        'number': number,
        'player': player,
        'shot_type': bits[1].strip(),
        'where': bits[2].strip(),
        'zone': bits[3].strip(),
        'distance': bits[4].strip()
    }


def parse_faceoff(desc):
    bits = desc.split(' ')
    return {
        'location': bits[2][:-1],
        'player_1_team': bits[5],
        'player_1_number': format_player_number(bits[6]),
        'player_1_name': bits[7],
        'player_2_team': bits[9],
        'player_2_number': format_player_number(bits[10]),
        'player_2_name': bits[11],
    }


def parse_hit(desc):
    bits = desc.split(' ')

    return {
        'hitter_team': bits[0],
        'hitter_number': format_player_number(bits[1]),
        'hitter_name': bits[2],
        'hittee_team': bits[4],
        'hittee_number': format_player_number(bits[5]),
        'hittee_name': bits[6],
        'location': bits[7][:-1]
    }


def parse_game_events(events):
    types = {
        'MISS': parse_miss,
        'FAC': parse_faceoff,
        'HIT': parse_hit
    }

    for event in [event for event in events if event['type'] in types]:
        event['meta'] = types[event['type']](event['description'])

    return events


def sort_into_periods(events):
    periods = defaultdict(list)
    for event in events:
        periods[event['period']].append(event)

    return periods


def get_play_by_play_report(game_id):
    # is it in the file system already?
    report_path = os.path.join(
        config['play_by_play_dir'],
        '{game_id}.html'.format(game_id=game_id)
    )

    try:
        with open(report_path, 'r') as report_file:
            return report_file.read()
    except FileNotFoundError:
        report = retrieve_play_by_play_report(game_id)
        with open(report_path, 'w') as report_file:
            report_file.write(str(report))

        return report


def thread(functions, *args, **kwargs):
    '''Provides the result of running a
       series of functions, using provided
       args and kwargs as the input to the
       first function in the list, and feeding
       the result at each step into the next
       function

       Inspired by clojures thread macro
    '''
    result = functions[0](*args, **kwargs)

    for function in functions[1:]:
        result = function(result)

    return result


game = thread([get_play_by_play_report,
               convert_raw_report_to_events,
               parse_game_events],
              563)

import pdb; pdb.set_trace()
