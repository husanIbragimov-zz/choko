#!/bin/bash
cd /var/www/choko
source /var/www/choko/venv/bin/activate
python3 manage.py runserver 0.0.0.0:80
