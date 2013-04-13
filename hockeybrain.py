import os
import logging

import bs4
import requests

import event_parsers
import utils
import config
import entities

logger = logging.getLogger()


def download_play_by_play_report_for_game_id(game_id):
    '''Gets stats for a given game id'''
    assert type(game_id) is int, "game_id must be an int"
    # TODO: check to see what game ids go up to
    assert game_id < 10000, "game id must be < 10000"

    url = config.PLAY_BY_PLAY_URL.format(game_id=game_id)
    logger.info('retrieving play by play from {url}'.format(url=url))
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Error retrieving game report')

    return response.content


def get_players_on_from_cell(cell):
    on_ice = []
    for player in cell.find_all('font'):
        position, player_name = player.attrs['title'].split(' - ')
        on_ice.append(entities.Player(
            name=player_name,
            number=player.text,
            position=position
        ))

    return on_ice


def get_event_from_row(row):
    cells = row.find_all('td', recursive=False)
    return {
        'id': cells[0].text,
        'period': cells[1].text,
        'strength': cells[2].text,
        'time': cells[3].contents[0],
        'type': cells[4].text,
        'description': cells[5].text,
        'visitor_on': get_players_on_from_cell(cells[6]),
        'home_on': get_players_on_from_cell(cells[7])
    }


def get_events_from_report(report):
    '''parses an html play by play report'''
    soup = bs4.BeautifulSoup(report)

    return [get_event_from_row(row)
            for table in soup.find_all('table')
            for row in table.find_all('tr')
            if 'evenColor' in row.attrs.get('class', [])]


def safely_run_parser(parser, description):
    try:
        result = parser(description)
    except (IndexError, ValueError) as exc:
        logging.error(
            'Caught parser exception for description [{0}]'.format(
                description
            ),
            exc_info=True
        )

        result = exc

    return result


def add_meta_to_events(events):
    # builds a dictionary of functions in the event_parsers module
    # ignoring anything starting with an underscore
    # TODO: along with the corresponding note in event_parsers,
    # this approach seems a bit magical
    parsers = {func: getattr(event_parsers, func)
               for func in dir(event_parsers)
               if func[0] != '_'}

    for event in events:
        if event['type'] in parsers:
            event['meta'] = safely_run_parser(
                parsers[event['type']],
                event['description']
            )
        else:
            logging.warning('[{0}] has no event parser'.format(event['type']))

    return events


def get_play_by_play_report_for_game_id(game_id):
    # is it in the file system already?
    report_path = os.path.join(
        config.PLAY_BY_PLAY_DIR,
        '{game_id}.html'.format(game_id=game_id)
    )

    try:
        with open(report_path, 'r') as report_file:
            logging.info('Using downloaded report {game_id}'.format(
                game_id=game_id
            ))
            return report_file.read()
    except FileNotFoundError:
        logging.info('Game not found, downloading from remote')
        report = download_play_by_play_report_for_game_id(game_id)
        with open(report_path, 'w') as report_file:
            report_file.write(str(report))
            logging.info('Wrote game {game_id} to {path}'.format(
                game_id=game_id,
                path=report_path
            ))

        return report


def get_game_summary_from_events(events):
    # summary = {
    #     'home': None,
    #     'visitor': None,
    #     'home_score': 0,
    #     'visitor_score': 0
    # }

    return events


def get_events_for_game(game_id):
    #TODO: cache generated data
    events = utils.thread(
        [get_play_by_play_report_for_game_id,
         get_events_from_report,
         add_meta_to_events],
        game_id
    )

    return {
        'summary': get_game_summary_from_events(events),
        'events': events
    }

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    game = get_events_for_game(563)
    events = game['events']
    fos = [e['meta'] for e in events if e['type'] == 'FAC']

    import pdb
    pdb.set_trace()
