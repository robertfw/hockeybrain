import os
import logging

import bottle

import config
import utils
import nhlapi

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

application = bottle.Bottle()

bottle.debug(config.DEBUG)


@application.route('/static/<filepath:path>')
def static(filepath):
    return bottle.static_file(filepath, config.STATIC_PATH)


@application.route('/api/game/<game_id:int>')
def game(game_id):
    return {'game': nhlapi.get_game(game_id)}


@application.route('/')
def index():
    return utils.render('index.moustache', {
        'version': config.VERSION
    })


if __name__ == '__main__':
    kwargs = {
        'host': config.HOST,
        'port': config.PORT
    }

    if config.DEBUG:
        kwargs['reloader'] = True
        kwargs['debug'] = True

    application.run(**kwargs)
else:
    # make sure we're working out of the base directory
    os.chdir(config.BASE_DIR)
