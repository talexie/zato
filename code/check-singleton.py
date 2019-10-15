# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import os
import tempfile
from datetime import datetime, timedelta
from json import dumps
from traceback import format_exc

# Bunch
from bunch import bunchify

# Dateutil
from dateutil.parser import parse as dt_parse

# Zato
from zato.server.service import Service

class CheckSingleton(Service):
    name = 'check.singleton'

    def handle(self):
        http_get = self.wsgi_environ['zato.http.GET']
        delta = int(http_get.get('delta', 30))
        if delta < 20:
            delta = 30

        now = datetime.utcnow()

        response = bunchify({
            'delta': delta,
            'now': now.isoformat(),
            'last_updated': None,
            'is_alive': False,
            'exc_details': None,
            'difference': None
        })

        try:
            redis_key = 'zato.singleton.alive.{}'.format(self.server.cluster_id)
            last_updated = self.kvdb.conn.get(redis_key)

            response.last_updated = last_updated

            last_updated = dt_parse(last_updated)
            allowed = now - timedelta(seconds=delta)
            difference = allowed - last_updated

            response.difference = str(difference)

            if difference.total_seconds() < delta:
                response.is_alive = True

        except Exception as e:
            response.exc_details = str(e)
            self.logger.warn('Caught an exception %s, e:`%s`', e, format_exc())

        self.response.payload = dumps(response)
