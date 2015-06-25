# !/usr/bin/python
# -*- coding: utf8 -*-

__version__ = '1.0'
__author__ = 'Balazs Kocso'

""" NoIPUpdater

Python script which uses the no-ip.com API to update the IP.
"""

API_KEY = "api_key"    # base64.b64encode("username:password")
HOSTNAME = "hostname"
STORED_IP_FILE = "/dev/shm/current_ip"
LOG_FILE = "/var/log/noipupd.log"

import urllib
import urllib2
import logging
import logging.handlers

logger = logging.getLogger("NoIPUpdater")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 ** 2, backupCount=5)
fmt = logging.Formatter('[%(levelname)0.1s %(asctime)s %(name)s] %(message)s', datefmt="%y%m%d %H:%M:%S")
handler.setFormatter(fmt)
logger.addHandler(handler)

IP_IDENTIFIERS = [
    "http://ipv4.icanhazip.com/",
    "http://v4.ident.me/",
    "https://api.ipify.org/",
    "http://curlmyip.com/",
    "http://ifconfig.me/ip"
]

def main():
    iterator = iter(IP_IDENTIFIERS)
    try :
        while True:
            url = iterator.next()
            try:
                f = urllib2.urlopen(url)
                response = f.read()
                current_ip = response.strip()
                logger.debug("Current IP is %s." % (current_ip))
                break
            except urllib2.URLError:
                pass
    except StopIteration:
        logger.warning("Couldn't get the current IP.")
        return

    try:
        with open(STORED_IP_FILE, 'r') as fp:
            stored_ip = fp.read()
    except IOError:
        stored_ip = None

    if stored_ip is not None and current_ip == stored_ip:
        logger.debug("IP not changed (%s)." % (current_ip))
        return

    try:
        get_params = urllib.urlencode({
            "hostname": HOSTNAME,
            "myip": current_ip
        })
        request = urllib2.Request("https://dynupdate.no-ip.com/nic/update?%s" % (get_params))
        request.add_header("Authorization", "Basic " + API_KEY)
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

    with open(STORED_IP_FILE, 'w') as fp:
        fp.write(current_ip)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e.message)
