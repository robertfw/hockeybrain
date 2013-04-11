import logging
import bottle
import settings

import hockeybrain

logging.basicConfig(level=logging.DEBUG)

app = bottle.Bottle()

if settings.DEBUG:
    bottle.debug(True)


@app.route('/')
def index():
    return 'omg'


@app.route('/game/<game_id>')
def game(game_id):
    return bottle.Response(hockeybrain.get_game(int(game_id)))


if __name__ == '__main__':
    kwargs = {
        'host': settings.HOST,
        'port': settings.PORT
    }

    if settings.DEBUG:
        kwargs['reloader'] = True
        func = bottle.debug
    else:
        func = bottle.run

    app.run(**kwargs)
