LibreHatti
==========


Setting virtualenvs
===================

curl -O http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
sudo easy_install pip
 
pip completion --bash >> ~/.bashrc

and run source ~/.bashrc to enable

Use pip to install virtualenv and virtualenvwrapper

sudo pip install virtualenv
sudo pip install virtualenvwrapper
 
export WORKON_HOME=`~/.virtualenvs`
 
mkdir $WORKON_HOME
 
echo "export WORKON_HOME=$WORKON_HOME" >> ~/.bashrc
 
Setup virtualenvwrapper
 
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
echo "export PIP_VIRTUALENV_BASE=$WORKON_HOME" >> ~/.bashrc

Source ~/.bashrc to load the changes

source ~/.bashrc

Test if it works

Now we create our first virtual environment
 
mkvirtualenv test

You will see that the environment will be set up, and your prompt now includes the name of your active environment in parentheses. Also if you now run
 
python -c "import sys; print sys.path"

you should see a lot of /home/user/.virtualenv/... because it now doesn't use your system site-packages.

You can deactivate your environment by running
 
deactivate

and if you want to work on it again, simply type
 
workon test

Finally, if you want to delete your environment, type
 
rmvirtualenv test
  




REQUIREMENTS
------------
    1.Apache2
    2.mysql-server
    3.python3x
    4.python-pip
    5.PyMySQL
    6.django 1.8

Installation of Requirements

1) Apache2

Run following command in terminal to install
    
     $ sudo apt-get install apache2
     
2) mysql-server

Run following command in terminal
    
    $ sudo apt-get install mysql-server
    
3) Python 3x

Follow the link given below
    http://askubuntu.com/questions/449555/how-to-install-python-3-4-on-ubuntu
    	
    
5) PyMySQL

Run following command in terminal
    
    $ pip install PyMySQL

6) Python modules

Run following command in terminal
    
    $ pip install -r requirements.txt

7) Exim4

Run following command in terminal

    $ sudo apt-get install exim4

and configure it using [this](https://jasvirsinghgrewal91.wordpress.com/2013/06/23/e-mail-server-exim4/)


Steps for Installation of LibreHatti:

1) Fork the repository [LibreHatti](https://github.com/GreatDevelopers/ofau/tree/py3dj8) and clone the forked repository
    
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
    $ python manage.py migrate
    $ python manage.py runserver
    
6) Open 'http://127.0.0.1:8000/' in your browser.
