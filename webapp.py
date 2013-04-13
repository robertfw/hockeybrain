import os
import logging

import pystache
import bottle

import config
import hockeybrain

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

application = bottle.Bottle()

bottle.debug(config.DEBUG)


class TemplateNotFoundError(Exception):
    pass


def render(template, context=None):
    if context is None:
        context = {}

    try:
        tpl_path = os.path.join(config.TEMPLATES_DIR, template)
        with open(tpl_path) as tpl_file:
            return pystache.render(tpl_file.read(), context)
    except FileNotFoundError:
        raise TemplateNotFoundError('Could not find {0}'.format(tpl_path))


@application.route('/static/<filepath:path>')
def static(filepath):
    return bottle.static_file(filepath, config.STATIC_PATH)


@application.route('/api/game/<game_id:int>')
def game(game_id):
    return {'events': hockeybrain.get_events_for_game(game_id)}


@application.route('/')
def index():
    return render('index.moustache', {
        'version': config.VERSION,
        'build': config.BUILD,
        'user': {
            'name': 'robertfw',
            'email': 'radicalphoenix@gmail.com'
        },
        'games': [
        ]
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
