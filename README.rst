====
twod
====

twod is a daemon that updates your twodns_ entries.


configuration
=============

twod will look for a configuration file in the following locations
(in this particular order):

- /etc/twod/twod.conf
- ~/.config/twod/twod.conf
- ~/.twod/twod.conf


Example config::

    [general]
    user = username@example.com
    password = password
    interval = 3600
    url = https://api.twodns.de/hosts/<myexamplehost>

    [logging]
    level = WARN

.. _twodns: https://www.twodns.de
