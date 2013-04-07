import os
import logging

import bs4
import requests

import event_parsers

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


def convert_row_to_event(cells):
    return {
        'id': cells[0].text,
        'period': cells[1].text,
        'strength': cells[2].text,
        'time': cells[3].contents[0],
        'type': cells[4].text,
        'description': cells[5].text
    }


def convert_report_to_events(report):
    '''parses an html play by play report'''
    soup = bs4.BeautifulSoup(report)

    return [convert_row_to_event(row.find_all('td'))
            for table in soup.find_all('table')
            for row in table.find_all('tr')
            if 'evenColor' in row.attrs.get('class', [])]


def parse_game_events(events):
    parsers = {func: getattr(event_parsers, func)
               for func in dir(event_parsers)
               if func[0] != '_'}

    for event, parser in [(event, parsers[event['type']])
                          for event in events if event['type'] in parsers]:
        event['meta'] = parser(event['description'])

    for event in events:
        if event['type'] in parsers:
            event['meta'] = parsers[event['type']](event['description'])
        else:
            logging.warning('Parser not found for event: [{0}]'.format(event['type']))

    return events


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
               convert_report_to_events,
               parse_game_events],
              563)

import pdb; pdb.set_trace()
