#!/usr/bin/env python2

"""twod TwoDNS host IP updater daemon.

twod is a client for the TwoDNS dynamic DNS service.

Copyright (C) 2014 Tablet Mode <tablet-mode AT monochromatic DOT cc>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/].

"""

import logging.handlers
import logging.config

from argparse import ArgumentParser
from ConfigParser import (SafeConfigParser, MissingSectionHeaderError,
                          NoSectionError, NoOptionError)
from json import dumps, loads
from lockfile.pidlockfile import PIDLockFile
from os import path
from random import randint
from re import match
from time import sleep

from daemon import DaemonContext
from requests import get, put, exceptions

from _version import __version__


class _ServiceGenerator:

    """Select service URL depending on mode."""

    def __init__(self, services):
        self.services = services
        self.cur = -1

    def __iter__(self):
        return self

    def next(self, mode):
        self.cur = self.cur + 1
        if mode == 'round_robin':
            if self.cur < len(self.services):
                service = self.services[self.cur]
            else:
                self.cur = 0
                service = self.services[self.cur]
            return service
        elif mode == 'random':
            self.cur = randint(0, (len(self.services) - 1))
            service = self.services[self.cur]
            return service


class _Data:

    """This is where the fun begins."""

    def __init__(self, conf):
        self.log = logging.getLogger('twod')
        self.ident = (conf['user'], conf['password'])
        self.url = conf['url']
        self.ip_mode = conf['ip_mode']
        ip_url = conf['ip_url'].split(' ')
        self.gen = _ServiceGenerator(ip_url)
        self.rec_ip = self._get_rec_ip()

    def _get_service_url(self):
        return self.gen.next(self.ip_mode)

    def _get_ext_ip(self):
        """Get external IP.

        Returns external IP as string.
        Returns False on failure.

        """
        self.log.debug("Fetching external ip...")
        try:
            ip_request = get(self._get_service_url(), verify=True, timeout=16)
            ip_request.raise_for_status()
        except (exceptions.ConnectionError, exceptions.HTTPError) as e:
            message = "Error while fetching external IP: %s" % e
            self.log.warning(message)
            return False
        except Exception as e:
            message = "Unexpected error while fetching external IP: %s" % e
            self.log.critical(message)
            raise
        else:
            ip = ip_request.text.rstrip()
            return ip

    def _get_rec_ip(self):
        """Get IP stored by TwoDNS.

        Returns IP as string. Returns False on failure.

        """
        self.log.debug("Fetching TwoDNS ip...")
        try:
            rec_request = get(
                self.url, auth=self.ident, verify=True, timeout=16)
            rec_request.raise_for_status()
        except (exceptions.ConnectionError, exceptions.HTTPError) as e:
            message = "Error while fetching IP from TwoDNS: %s" % e
            self.log.warning(message)
            return False
        except Exception as e:
            message = "Unexpected error while fetching IP from TwoDNS: %s" % e
            self.log.critical(message)
            raise
        else:
            rec_json = loads(rec_request.text)
            ip = rec_json['ip_address']
            return ip

    def _check_ip(self):
        """Check if external IP matches recorded IP.

        Returns external IP as string if IPs differ. Returns False if the IPs
        match or an error occured.

        """
        self.log.debug("Checking if recorded IP matches current IP...")
        ext_ip = self._get_ext_ip()
        # something went wrong while fetching external IP but it's possible to
        # continue
        if not ext_ip:
            return False

        rec_ip = self.rec_ip
        if ext_ip == rec_ip:
            self.log.debug("IP has not changed.")
            return False
        else:
            return ext_ip

    def _update_ip(self, new_ip):
        """Update IP stored at TwoDNS."""
        self.log.debug("Updating recorded IP...")
        try:
            payload = {"ip_address": new_ip}
            r = put(
                self.url, auth=self.ident, data=dumps(payload), verify=True,
                timeout=16)
        except (exceptions.ConnectionError, exceptions.HTTPError) as e:
            message = "Error while updating IP: %s" % e
            self.log.warning(message)
            return False
        except Exception as e:
            message = "Unexpected error while updating IP: %s" % e
            self.log.critical(message)
            raise
        else:
            if(r.status_code == 200):
                message = "IP changed to %s." % new_ip
                self.log.info(message)
                self.rec_ip = new_ip
            else:
                message = "Failed to update IP."
                self.log.warning(message)
                return r.status_code


class Twod:

    """Twod class."""

    def __init__(self, config_path='/etc/twod/twodrc'):
        """Initialisation.

        * Setup logging
        * Read configuration
        * Initialise Data class

        """
        self._setup_logger()
        conf = self._read_config(config_path)
        self._setup_logger(conf['loglevel'])
        self.interval = conf['interval']
        self.conf = conf

    def _is_url(self, url):
        if not match(r'http(s)?://', url):
            raise ValueError(
                "Invalid URL: '%s' - has to start with 'http(s)'" % url)
        return url

    def _is_mode(self, mode):
        if mode not in ('random', 'round_robin'):
            raise ValueError("Invalid mode: '%s'" % mode)
        return mode

    def _setup_logger(self, level='WARN'):
        """Setup logging."""
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'daemon': {
                    'format': '%(asctime)s %(module)s[%(process)d]: '
                              '%(message)s'
                },
            },
            'handlers': {
                'syslog': {
                    'formatter': 'daemon',
                    'class': 'logging.handlers.SysLogHandler',
                    'address': '/dev/log',
                    'level': 'DEBUG',
                },
                'stderr': {
                    'formatter': 'daemon',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stderr',
                    'level': 'DEBUG',
                },
            },
            'loggers': {
                'twod': {
                    'handlers': ['syslog', 'stderr'],
                    'level': level,
                    'propagate': True
                }
            }
        })
        self.log = logging.getLogger('twod')

    def _read_config(self, config_path):
        """Read config.

        Exit on invalid config.

        """
        self.log.debug("Reading config...")
        conf = {}
        config = SafeConfigParser()
        try:
            # Check if config is even readable
            f = open(path.expanduser(config_path), 'r')

            # Read config
            config.readfp(f)
            f.close()

            conf['user'] = config.get('general', 'user')
            conf['password'] = config.get('general', 'password')
            conf['url'] = self._is_url(config.get('general', 'host_url'))
            conf['interval'] = config.getint('general', 'interval')
            conf['ip_mode'] = self._is_mode(config.get('ip_service', 'mode'))
            conf['ip_url'] = self._is_url(config.get('ip_service', 'ip_urls'))
            conf['loglevel'] = config.get('logging', 'level')
        except (MissingSectionHeaderError, NoSectionError, NoOptionError,
                ValueError, IOError) as e:
            message = "Configuration error: %s" % e
            self.log.critical(message)
            exit(1)
        except Exception as e:
            message = "Unexpected error while reading config: %s" % e
            self.log.critical(message)
            exit(1)
        return conf

    def run(self):
        """Main loop."""
        data = _Data(self.conf)
        while(True):
            changed_ip = data._check_ip()
            if changed_ip:
                data._update_ip(changed_ip)
            sleep(self.interval)


def main():
    """Main function."""
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', metavar='FILE',
                        help="load configuration from FILE")
    parser.add_argument('-D', '--no-detach', dest='nodetach',
                        action='store_true', help="do not detach from console")
    parser.add_argument('-V', '--version', action='version',
                        version='twod ' + __version__)
    args = parser.parse_args()

    if args.config and not path.isfile(path.expanduser(args.config)):
        parser.error("'%s' is not a file" % args.config)

    twod = Twod(args.config) if args.config else Twod()
    if args.nodetach:
        twod.run()
    else:
        twod.log.debug("Moving to background...")
        with DaemonContext(pidfile=PIDLockFile('/var/run/twod.pid')):
            twod.run()


if __name__ == '__main__':
    main()
