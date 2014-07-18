====
twod
====

``twod`` is a daemon that updates your TwoDNS_ entries.


dependencies
============

- python2 (>=dev-lang/python-2.7)
- python-daemon (>=dev-python/python-daemon-1.6)
- requests (>=dev-python/requests-1.2.3)


configuration
=============

``twod`` will look for a configuration file in ``/etc/twod/twod.conf``. Optionally
you can tell ``twod`` to use a specified configuration file instead by using
the ``-c`` parameter. 


Example config:

.. literalinclude:: docs/examples/twodrc.example
   :language: ini


usage
=====

Gentoo GNU/Linux
^^^^^^^^^^^^^^^^

Get the twod ebuild from the my_little_overlay_ overlay. After installing it
you can control ``twod`` like any other service:

    $ /etc/init.d/twod start

To run daemon manually:
    
    $ python2 <path/to/twod.py>


.. _TwoDNS: https://www.twodns.de
.. _my_little_overlay: https://github.com/twisted-pear/my-little-overlay
