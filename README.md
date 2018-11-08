# Linux Server Deployment
## Udacity Full Stack Web Development ND Project 3

___________________________________________

## IP Address 

54.205.228.170:2200

## Complete URL

54.205.228.170.xip.io

## Installed Software

In order to have a properly running Python Flask application, certain packages needed to be installed. `sudo apt-get install` was used to install all necessary packages unless otherwise noted.

*`apache2` for the web server
*`python3-dev` for required python packages
*`libapache2-mod-wsgi-py3` for the python3 WSGI mod to run our application
*`git` to get our files from github and have a version maintenance
*`python3-pip` to allow for the installation of other python packages
*`python-flask`
*`python-sqlalchemy` 
*`python-psycopg2`
*`oauth2client` to allow for OAuth2 processes
*`requests` to allow for submission handling on the website
*`httplib2`
*`postgresql` for database management
*`pip3 install flask-dance[sqla]` to handle OAuth2 requests

On Amazon's Lightsail website, I added the port 2200 so that it could be used for SSH access. I then modified the `/etc/ssh/sshd_config` file such that the server can only be remote accessed from port 2200, that root login is not allowed, and that a key is required to remote connect.

## 3rd Party Resources used

*Troubleshooting initial setup of the server was done through https://github.com/harushimo/linux-server-configuration (with the exception of the `ufw`).

*Updated .conf file configuration from https://hk.saowen.com/a/0a0048ca7141440d0553425e8df46b16cdf4c13f50df4c5888256393d34bb1b9

*All other troubleshooting was accomplished through the error logs and Udacity Coursework.

