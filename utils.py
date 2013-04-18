import os

import pystache

import config
import exceptions


def thread(functions, *args, **kwargs):
    '''Provides the result of running a
       series of functions, using provided
       args and kwargs as the input to the
       first function in the list, and feeding
       the result at each step into the next
       function

       Inspired by thread macro in clojure
    '''
    result = functions[0](*args, **kwargs)

    for function in functions[1:]:
        result = function(result)

    return result


def split_list_around_value(alist, splitter):
    split_index = alist.index(splitter)
    return (alist[:split_index], alist[split_index + 1:])


def render(template, context=None):
    if context is None:
        context = {}

    try:
        tpl_path = os.path.join(config.TEMPLATES_DIR, template)
        with open(tpl_path) as tpl_file:
            return pystache.render(tpl_file.read(), context)
    except FileNotFoundError:
        raise exceptions.TemplateNotFoundError(
            'Could not find {0}'.format(tpl_path)
        )
