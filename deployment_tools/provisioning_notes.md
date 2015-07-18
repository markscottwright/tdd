Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

## Nginx Virtual host config

* see nginx.template.conf
* replace SITENAME with, say www.markscottwright.com

## Upstart job

* see gunicorn-upstart.template.conf
* replace SITENAME with, say www.markscottwright.com

## Folder structure
Assume we have a user account at /home/wrightm

/home/wrightm
-   sites
    -   SITENAME
        -   database
        -   source
        -   static
        -   virtualenv


