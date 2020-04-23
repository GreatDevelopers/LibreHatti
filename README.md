LibreHatti
==========

REQUIREMENTS
------------
    1.Apache2
    2.mysql-server
    3.python2.7
    4.python-pip
    5.python-mysqldb
    6.django 1.7

#### Installation of LibreHatti

    cd path/to/LibreHatti/
    ./install.sh

#### OR

Installation of Requirements

1) Apache2

Run following command in terminal to install

     $ sudo apt-get install apache2

2) mysql-server

Run following command in terminal

    $ sudo apt-get install mysql-server

3) python2.7

Run following command in terminal

    $ sudo apt-get install python

4) python-pip

Run following command in terminal

    $ sudo apt-get install python-pip

5) python-mysqldb

Run following command in terminal

    $ sudo apt-get install python-mysqldb

6) Python modules

Run following command in terminal

    $ sudo pip install -r requirements.txt

7) Exim4

Run following command in terminal

    $ sudo apt-get install exim4

and configure it using [this](https://jasvirsinghgrewal91.wordpress.com/2013/06/23/e-mail-server-exim4/)


Steps for Installation of LibreHatti:

1) Fork the repository [LibreHatti](https://github.com/GreatDevelopers/LibreHatti/) and clone the forked repository

    $ git clone 'link to your forked repository'

2) Create a database for LibreHatti.

    $ mysql -u root -p
    $ create database librehatti;
    $ quit

3) Edit settings.py file in LibreHatti/src/librehatti directory. Things to be edited are:

Line No 10 : DATABASES

    NAME : librehatti
    USER : Your MySQL username
    PASSWORD : Your MySQl password

Line No 43 : STATICFILES_DIRS

4) Edit config.py accordingly.

5) Goto the project directory and run the following commands.

    $ cd src
    $ python manage.py syncdb
    $ python manage.py runserver 127.0.0.1:8090

6) Open 'localhost:8090' in your browser.
