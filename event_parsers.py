import utils
import entities
# Functions in this file that do not start with an underscore will be used to
# parse game events, with the event type being the function name
# TODO: this seems a bit too magical


def _format_player_number(number):
    return number.replace('#', '')


def MISS(desc):
    bits = desc.split(',')

    team, number, name = bits[0].split(' ')

    return {
        'team': entities.Team(team),
        'player': entities.Player(
            name=name,
            number=number
        ),
        'shot_type': bits[1].strip(),
        'where': bits[2].strip(),
        'zone': bits[3].strip(),
        'distance': bits[4].strip()
    }


def FAC(desc):
    bits = desc.split(' ')
    vs = bits[5:]
    faceoffers = utils.split_list_around_value(vs, 'vs')
    if faceoffers[0][0] == bits[0]:
        winner = faceoffers[0]
        loser = faceoffers[1]
    else:
        winner = faceoffers[1]
        loser = faceoffers[0]

    return {
        'location': bits[2][:-1],
        'winner_team': entities.Team(winner[0]),
        'winner_player': entities.Player(' '.join(winner[2:]), winner[1]),
        'loser_team': entities.Team(loser[0]),
        'loser_player': entities.Player(' '.join(loser[2:]), loser[1])
    }


def HIT(desc):
    bits = desc.split(' ')

    return {
        'hitter_team': entities.Team(bits[0]),
        'hitter_player': entities.Player(
            name=bits[2],
            number=_format_player_number(bits[1])
        ),

        'hittee_team': entities.Team(bits[4]),
        'hittee_player': entities.Player(
            name=bits[6],
            number=_format_player_number(bits[5])
        ),
        'location': bits[7][:-1]
    }


def PENL(desc):
    bits = desc.split(' ')
    return bits


def TAKE(desc):
    bits = desc.split(' ')
    return bits


def SHOT(desc):
    bits = desc.split(' ')
    return {
        'shooter_team': entities.Team(bits[0]),
        'hit': bits[1],
        'shooter_player': entities.Player(
            name=bits[4],
            number=_format_player_number(bits[3])
        ),
        'shot_type': bits[5],
        'location': bits[6][:-1],
        'distance_in_feet': bits[8]
    }


def BLOCK(desc):
    bits = desc.split(' ')

    return {
        'shooter_team': entities.Team(bits[0]),
        'shooter_player': entities.Player(
            name=bits[2],
            number=_format_player_number(bits[1])
        ),

        'block_type': bits[3],

        'blocker_team': entities.Team(bits[6]),
        'blocker_player': entities.Player(
            name=bits[8],
            number=_format_player_number(bits[7])
        ),

        'shot_type': bits[9],
        'location': bits[10][:-1]
    }


def PEND(desc):
    return {
        'time': desc.split(' ')[4]
    }


def GOAL(desc):
    bits = desc.split(' ')
    return bits


def GIVE(desc):
    bits = desc.split(' ')
    return bits


def GEND(desc):
    return {
        'time': desc.split(' ')[4]
    }


def STOP(desc):
    bits = desc.split(' ')
    return bits


def PSTR(desc):
    return {
        'local_time': desc.split(' ')[4]
    }
