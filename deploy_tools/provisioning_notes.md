Provisioning a new site
=========================

## Required packages:
* nginx
* Python 3.9
* vitrualenv + pip
* Git

eg, on Ubuntu
    
    $ sudo apt-get install git, python3.9, python3.9-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with e.g., dev.my-domain.com

## Systemd service

* see gunicorn-systemd.template.conf
* replace SITENAME with e.g., dev.my-domain.com

## Folder structure
Assume we have an user account at home/username

    /home/username
        └── sites
            └── SITENAME
                 ├── database
                 ├── source
                 ├── static
                 └── virtualenv
