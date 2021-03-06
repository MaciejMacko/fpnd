#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Target:   Python 3.6

import datetime

from diskcache import Index
from node_tools import update_state, get_cachedir
from node_tools import ENODATA, NODE_SETTINGS

try:
    from datetime import timezone
    utc = timezone.utc
except ImportError:
    from daemon.timezone import UTC
    utc = UTC()


cache = Index(get_cachedir())
max_age = NODE_SETTINGS['max_cache_age']
utc_stamp = datetime.datetime.now(utc)  # use local time for console

# reset timestamp if needed
if 'utc-time' in cache:
    stamp = cache['utc-time']
    cache_age = utc_stamp - stamp  # this is a timedelta
    print('Cache age is: {} sec'.format(cache_age.seconds))
    print('Maximum cache age: {} sec'.format(max_age))
    if cache_age.seconds > max_age:
        print('Cache data is too old!!')
        print('Stale data will be removed!!')
        cache.clear()

size = len(cache)
print('{} items currently in cache.'.format(size))
print('Cache items: {}'.format(list(cache)))

try:
    res = update_state()
    size = len(cache)
except:  # noqa: E722
    print('No data available, cache was NOT updated')
else:
    if size < 1:
        print('No data available (live or cached)')
        exit(1)

if size > 0:
    print('Get data result: {}'.format(res))
    size = len(cache)
    print('{} items now in cache.'.format(size))
    print('Cache items: {}'.format(list(cache)))

    if res is ENODATA or res is None:
        cache.update([('utc-time', stamp)])
        print('Old cache time is: {}'.format(stamp.isoformat(' ', 'seconds')))
    else:
        cache.update([('utc-time', utc_stamp)])
        print('New cache time is: {}'.format(utc_stamp.isoformat(' ', 'seconds')))
else:
    print('Cache empty and API returned ENODATA')
