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

Installation of Requiremets

1) Apache2

Run following command in terminal to install
    
     $ sudo apt-get install apache2
     
2) mysql-server

Run following commands in terminal
    
    $ sudo apt-get install mysql-server
    
3) python2.7

Run following commands in terminal
    
    $ sudo apt-get install python
    
4) python-pip

Run following commands in terminal
    
    $ sudo apt-get install python-pip

5) python-mysqldb

Run following commands in terminal
    
    $ sudo apt-get install python-mysqldb

6) Django 1.7

Run following commands in terminal
    
    sudo pip install https://www.djangoproject.com/download/1.7.b4/tarball/


Steps for Installation of LibreHatti.

1) Fork the repositery [LibreHatti](https://github.com/GreatDevelopers/LibreHatti/) and clone the forked repositery
    
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
    
4) Goto the project directory and run the following commands.
    
    $ cd src
    $ python manage.py migrate
    $ python manage.py runserver 127.0.0.1:8090
    
5) Open 'localhost:8090' in your browser.
