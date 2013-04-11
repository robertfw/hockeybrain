import logging
import bottle
import settings

import hockeybrain

logging.basicConfig(level=logging.DEBUG)

app = bottle.Bottle()

if settings.DEBUG:
    bottle.debug(True)


@app.route('/static/<filepath:path>')
def static(filepath):
    return bottle.static_file(filepath, settings.STATIC_PATH)


@app.route('/api/game/<game_id:int>')
def game(game_id):
    return {'events': hockeybrain.get_events_for_game(game_id)}

if __name__ == '__main__':
    kwargs = {
        'host': settings.HOST,
        'port': settings.PORT
    }

    if settings.DEBUG:
        kwargs['reloader'] = True

    app.run(**kwargs)
