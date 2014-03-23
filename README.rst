====
twod
====

twod is a daemon that updates your twodns_ entries.


dependencies
============

- python2 (dev-lang/python)
- python-daemon (dev-python/python-daemon)
- requests (dev-python/requests)


configuration
=============

twod will look for a configuration file in the following locations
(in this particular order):

- /etc/twod/twod.conf
- ~/.config/twod/twod.conf


Example config::

    [general]
    user = username@example.com
    password = password
    interval = 3600
    url = https://api.twodns.de/hosts/<myexamplehost>
    
    [ip_service]
    mode = random
    urls = https://icanhazip.com https://ipinfo.io/ip

    [logging]
    level = WARN

.. _twodns: https://www.twodns.de


usage
=====

To run daemon:
    
    $ python2 <path/to/twod.py>
