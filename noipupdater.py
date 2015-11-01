#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'Balazs Kocso'
__version__ = '1.1'

""" NoIPUpdater

Python script which uses the no-ip.com API to update the IP.
"""

import argparse
import urllib
import urllib2
import logging
import logging.handlers
import socket

logger = logging.getLogger("NoIPUpdater")

IP_IDENTIFIERS = [
    "http://ipv4.icanhazip.com/",
    "http://v4.ident.me/",
    "https://api.ipify.org/",
    "http://curlmyip.com/",
    "http://ifconfig.me/ip"
]

def main():
    iterator = iter(IP_IDENTIFIERS)
    current_ip = None
    try:
        while not current_ip:
            url = iterator.next()
            try:
                f = urllib2.urlopen(url)
                response = f.read()
                current_ip = response.strip()
                logger.debug("Current IP is %s." % (current_ip))
                break
            except (urllib2.URLError, socket.timeout):
                pass
    except StopIteration:
        logger.warning("Couldn't get the current IP.")
        return

    try:
        with open(args.stored_ip_file, 'r') as fp:
            stored_ip = fp.read()
    except IOError:
        stored_ip = None

    if stored_ip is not None and current_ip == stored_ip:
        logger.debug("IP not changed (%s)." % (current_ip))
        return

    try:
        with open(args.api_key, 'r') as fp:
            api_key = fp.read().strip()
    except (OSError, IOError) as e:
        logger.warning(e.message)
        return

    try:
        get_params = urllib.urlencode({
            "hostname": args.hostname,
            "myip": current_ip
        })
        request = urllib2.Request("https://dynupdate.no-ip.com/nic/update?%s" % (get_params))
        request.add_header("Authorization", "Basic " + api_key)
        request.add_header("User-Agent", "Python No-IP Updater %s by %s" % (__version__, __author__))
        f = urllib2.urlopen(request)
        response = f.read()

        if response.startswith("good"):
            logger.info("IP changed to: %s" % (current_ip))
        elif response.startswith("nochg"):
            logger.debug("IP already sent (%s)." % (current_ip))
        else:
            logger.warning(response)

    except urllib2.HTTPError as err:
        logger.warning(err.read())
        return
    except urllib2.URLError as err:
        logger.warning(err.reason)
        return

    with open(args.stored_ip_file, 'w') as fp:
        fp.write(current_ip)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NoIP updater script.")
    parser.add_argument("--api_key", metavar="FILE", required=True,
        help="file's path, which contains the base64 encoded 'username:password'")
    parser.add_argument("--hostname", metavar="NAME", required=True,
        help="NoIP hostname")
    parser.add_argument("--stored_ip_file", metavar="FILE", default="/dev/shm/current_ip",
        help="stored ip file path (default: /dev/shm/current_ip)")
    parser.add_argument("--log_file", metavar="FILE", default="/var/log/noipupd.log",
        help="log file path (default: /var/log/noipupd.log)")
    parser.add_argument("--log_level", metavar="LEVEL", default="INFO",
        help="logging level (default: INFO)")
    args = parser.parse_args()

    handler = logging.handlers.RotatingFileHandler(args.log_file, maxBytes=10 * 1024 ** 2, backupCount=5)
    fmt = logging.Formatter('[%(levelname)0.1s %(asctime)s %(name)s] %(message)s', datefmt="%y%m%d %H:%M:%S")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    numeric_loglevel = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_loglevel, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)
    logger.setLevel(numeric_loglevel)

    try:
        main()
    except Exception as e:
        logger.exception(e.message)
