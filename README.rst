====
twod
====

``twod`` is a daemon that updates your TwoDNS_ host IP entries.


dependencies
============

- python2 (>=dev-lang/python-2.7)
- python-daemon (>=dev-python/python-daemon-1.6)
- requests (>=dev-python/requests-1.2.3)


configuration
=============

``twod`` will look for a configuration file in ``/etc/twod/twodrc``. Optionally
you can tell ``twod`` to use a specified configuration file instead by using
the ``-c`` parameter.

Example config::

    [general]
    user     = username@example.com
    password = password
    interval = 3600
    host_url = https://api.twodns.de/hosts/myexamplehost

    [ip_service]
    mode     = random
    ip_urls  = https://icanhazip.com https://ipinfo.io/ip

    [logging]
    level    = WARN


installation
============

Gentoo GNU/Linux
^^^^^^^^^^^^^^^^

1. Install ``twod`` from `my little overlay <https://github.com/twisted-pear/my-little-overlay>`_.

2. Copy ``docs/example/twodrc.example`` to ``/etc/twod/twodrc`` and change the
   settings according to your setup.


usage
=====

After installing ``twod`` you can control it like any other service:

    $ /etc/init.d/twod start

To run the daemon manually you can just call the ``twod`` binary:

    $ twod


documentation
=============

You can find detailed documentation at
`twod's Read the Docs page <https://twod.readthedocs.org/en/latest/>`_,
powered by Sphinx_.



.. _TwoDNS: https://www.twodns.de
.. _my_little_overlay: https://github.com/twisted-pear/my-little-overlay
.. _Sphinx: http://sphinx-doc.org
