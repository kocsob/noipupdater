noipupdater
===========

Python script which uses the no-ip.com API to update the IP.

Usage
-----

    noipupdater.py [-h] --api_key FILE --hostname NAME
               [--stored_ip_file FILE] [--log_file FILE] [--log_level LEVEL]
    
    optional arguments:
      -h, --help            show this help message and exit
      --api_key FILE        file's path, which contains base64 encoded 'username:password'
      --hostname NAME       NoIP hostname
      --stored_ip_file FILE stored ip file path (default: /dev/shm/current_ip)
      --log_file FILE       log file path (default: /var/log/noipupd.log)
      --log_level LEVEL     logging level (default: INFO)

For general use
---------------

Place this in your cron file:

    */15 * * * * /file/location/noipupdater.py --api_key api.key --hostname hostname

This will update your IP every fifteen minutes.

Enjoy the always up to date DNS!