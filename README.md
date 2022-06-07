# SUDS

Project? Well, I wanted to make my own monitoring tool as a fun little task.

SUDS = Simple Up Down Service

If you read the instructions, you can set it up yourself! It's not nifty by any means but it can at least tell you if something is up or down.

Utilizes Python 3.10 and Django 4.0.4

Tl;dr - Do a git clone, open up two terminals, activate the virtual environment in both terminals, then run the python file inside of svc_pingparallel and in the other terminal do **py manage.py runserver 0.0.0.0:8000**

Disclaimer: Don't use in a production environment. The API is wide open and is exempt from CSRF. 
