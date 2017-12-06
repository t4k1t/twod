====
twod
====

``twod`` is a daemon that updates your TwoDNS_ host IP entries.


configuration
=============

``twod`` will look for a configuration file in ``/etc/twod/twodrc``. Optionally
you can tell ``twod`` to use a specified configuration file instead by using
the ``-c`` parameter.

Example config::

    [general]
    user      = username@example.com
    token     = token
    host_url  = https://api.twodns.de/hosts/myexamplehost
    interval  = 3600
    timeout   = 16
    redirects = 2

    [ip_service]
    mode      = random
    ip_urls   = https://icanhazip.com https://ipinfo.io/ip

    [logging]
    level     = WARNING


installation
============

Gentoo GNU/Linux
^^^^^^^^^^^^^^^^

1. Install ``twod`` from `my little overlay <https://github.com/twisted-pear/my-little-overlay>`_.

2. Copy ``/usr/share/doc/twod-<version>/examples/twodrc.example`` to
   ``/etc/twodrc`` and change the settings according to your setup.


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


tests
=====

Tests can be run by simply installing and invoking tox:

   $ tox



.. _TwoDNS: https://www.twodns.de
.. _my_little_overlay: https://github.com/twisted-pear/my-little-overlay
.. _Sphinx: http://sphinx-doc.org
