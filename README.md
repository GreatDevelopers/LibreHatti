LibreHatti
==========

Required Installations.<br>
1. sudo apt-get install mysql-server<br>
2. sudo apt-get install python-mysqldb<br>

Steps for Installation.<br>
1. Fork the repositery https://github.com/GreatDevelopers/LibreHatti/ and clone the forked repositery.<br>
2. Create a database for LibreHatti.<br>
3. Edit settings.py. Things to be edited are:<br>
  -> information in DATABASES.<br>
  -> STATIC_ROOT<br>
  -> STATICFILES_DIRS<br>
4. Run the command 'python manage.py migrate'<br>
5. Run the command 'pyhton manage.py runserver 127.0.0.1:8090'<br>
6. Open 'localhost:8090' in your browser.<br>
