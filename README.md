noipupdater
===========

Python script which uses the no-ip.com API to update the IP.

Usage
-----

Configure the script with
* correct API key (`username:password` encoded with base64),
* hostname,
* stored IP file (current IP) and
* log file, then

run it (`python noipupdater.py`).

For general use
---------------

Place this in your cron file:

    */15 * * * * python /file/location/noipupdater.py

This will update your IP every fifteen minutes.

Enjoy the always up to date DNS!