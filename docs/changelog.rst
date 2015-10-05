.. _changelog:

Changelog
=========

0.4.0
-----

* Add config setting for maximum number of redirects to follow on HTTP
  requests.

* Update man pages.

* Add CLI argument for pidfile location.

* Make interval, timeout, redirects, ip_mode and loglevel settings optional.

* Never exit on errors caused by HTTP requests.

0.3.2
-----

* Add config setting for HTTP timeout.

* Fix terminology for token setting. [`#1 <https://github.com/tablet-mode/twod/issues/1>`_]

* Catch connection and response timeouts. [`#2 <https://github.com/tablet-mode/twod/issues/2>`_]

* Normalise version string in setup.py.

* Add IP validation.

* Get rid of "Unexpected error" exceptions.

0.3.1
-----

* Add python dependencies to setup.py.

* Implement simpler version handling.

* Fix capitalisation of `TwoDNS <https://twodns.de>`_.

* Improve error handling for config parsing.
