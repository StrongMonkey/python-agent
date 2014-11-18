import logging

from cattle import utils
from cattle.type_manager import get_type, PUBLISHER

log = logging.getLogger('progress')


class EventProgress(object):
    def __init__(self, req, parent=None):
        self._req = req
        self._parent = parent

    def update(self, msg, progress=None, data=None):
        resp = utils.reply(self._req, data)
        resp['transitioning'] = 'yes'
        resp['transitioningMessage'] = msg
        resp['transitioningProgress'] = progress

        if self._parent is not None:
            resp = utils.reply(self._parent, resp)
            resp['transitioning'] = 'yes'
            resp['transitioningMessage'] = msg
            resp['transitioningProgress'] = progress

        publisher = get_type(PUBLISHER)
        try:
            publisher.publish(resp)
        except:
            pass


Progress = EventProgress


class LogProgress(object):
    def __init__(self):
        pass

    def update(self, msg, progress=None, data=None):
        log.info('Progress %s %s', msg, progress)
