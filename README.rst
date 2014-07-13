====
twod
====

twod is a daemon that updates your twodns_ entries.


dependencies
============

- python2 (>=dev-lang/python-2.7)
- python-daemon (>=dev-python/python-daemon-1.6)
- requests (>=dev-python/requests-1.2.3)


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


usage
=====

Gentoo GNU/Linux
^^^^^^^^^^^^^^^^

Get the twod ebuild from the my_little_overlay_ overlay. After installing it
you can control ``twod`` like any other service:

    $ /etc/init.d/twod start

To run daemon manually:
    
    $ python2 <path/to/twod.py>


.. _twodns: https://www.twodns.de
.. _my_little_overlay: https://github.com/twisted-pear/my-little-overlay
