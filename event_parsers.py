# Functions in this file that do not start with an underscore will be used to
# parse game events, with the event type being the function name
# TODO: this seems a bit too magical


def _format_player_number(number):
    return number.replace('#', '')


def MISS(desc):
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


def FAC(desc):
    bits = desc.split(' ')
    return {
        'winner': bits[0],
        'location': bits[2][:-1],
        'player_1_team': bits[5],
        'player_1_number': _format_player_number(bits[6]),
        'player_1_name': bits[7],
        'player_2_team': bits[9],
        'player_2_number': _format_player_number(bits[10]),
        'player_2_name': bits[11],
    }


def HIT(desc):
    bits = desc.split(' ')

    return {
        'hitter_team': bits[0],
        'hitter_number': _format_player_number(bits[1]),
        'hitter_name': bits[2],
        'hittee_team': bits[4],
        'hittee_number': _format_player_number(bits[5]),
        'hittee_name': bits[6],
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
        'shooter_team': bits[0],
        'hit': bits[1],
        'shooter_number': _format_player_number(bits[3]),
        'shooter_name': bits[4],
        'shot_type': bits[5],
        'location': bits[6][:-1],
        'distance_in_feet': bits[8]
    }


def BLOCK(desc):
    bits = desc.split(' ')

    return {
        'shooter_team': bits[0],
        'shooter_number': _format_player_number(bits[1]),
        'shooter_name': bits[2],
        'block_type': bits[3],
        'blocker_team': bits[6],
        'blocker_number': _format_player_number(bits[7]),
        'blocker_name': bits[8],
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
    bits = desc.split(' ')
    return bits
