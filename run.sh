#!/bin/bash
cd /home/web/task || exit
. venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:8080 main_app:app
