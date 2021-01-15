# Streamer

This application is deployed on AWS EC2 instance.

For demo visit: http://ec2-52-66-129-179.ap-south-1.compute.amazonaws.com/auth/signup/


## Installation Guide

1. Install python3

2. clone this repository: 
git clone https://github.com/vivekj52/Video_Streamer.git

3. Inside project directory, activate virtual environment by running:
source streamerEnv/bin/activate

4. Edit Local configuration file Video_Streamer/config.ini

Change name, username, password in [database] section.
Change default_video and upload_path in [media_location] section.

5. Run: python manage.py makemigrations

6. Run: python manage.py migrate

7. Run python manage.py runserver

Local server will start at default port 8000

## URLS

Signup: http://localhost:8000/auth/signup/
Login: http://localhost:8000/auth/login/
Player Page: http://localhost:8000/streamer/play
Upload Page: http://localhost:8000/streamer/upload
admin controls: http://localhost:8000/admin/

