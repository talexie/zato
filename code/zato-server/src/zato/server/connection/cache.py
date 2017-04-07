# -*- coding: utf-8 -*-

"""
Copyright (C) 2017, Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from logging import getLogger

# gevent
from gevent.lock import RLock

# Zato
from zato.cache import Cache

# ################################################################################################################################

logger = getLogger(__name__)

# ################################################################################################################################

class _NotConfiguredAPI(object):
    def set(self, *args, **kwargs):
        raise Exception('Default cache is not configured')
    get = set

# ################################################################################################################################

class CacheAPI(object):
    """ Base class for all cache objects.
    """
    def __init__(self):
        self.lock = RLock()
        self.default = _NotConfiguredAPI()
        self._set_api_calls()

    def _set_if_default(self, config, cache):
        if config.is_default:
            self.default = cache
            self._set_api_calls()

    def _set_api_calls(self):
        self.set = self.default.set
        self.get = self.default.get

# ################################################################################################################################

class BuiltinAPI(CacheAPI):
    """ Holds all built-in caches.
    """
    def __init__(self):
        super(BuiltinAPI, self).__init__()
        self.caches = {}

# ################################################################################################################################

    def _create(self, config):
        cache = Cache(config.max_size, config.max_item_size, config.extend_expiry_on_get, config.extend_expiry_on_set)
        self.caches[config.name] = cache
        self._set_if_default(config, cache)

# ################################################################################################################################

    def create(self, config):
        with self.lock:
            self._create(config)

# ################################################################################################################################

    def _edit(self, config):
        logger.warn('333 %s', config)

# ################################################################################################################################

    def edit(self, config):
        with self.lock:
            self._edit(config)

# ################################################################################################################################

    def _delete(self):
        pass

# ################################################################################################################################

    def delete(self):
        pass

# ################################################################################################################################

    def _clear(self):
        pass

# ################################################################################################################################

    def clear(self):
        pass


# ################################################################################################################################

    def get_size(self, name):
        pass

# ################################################################################################################################
