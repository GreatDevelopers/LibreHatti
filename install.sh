sudo apt-get install apache2 mysql-server python python-pip python-mysqldb
sudo pip install -r requirements.txt
sudo apt-get install exim4

#sudo dpkg-reconfigure exim4-config
#sudo gedit /etc/exim4/passwd.client
#*:USERNAME@example.com:PASSWORD.

echo "******************Information for database******************"
echo "DB_USER "
read  user
echo "DB_Password "
read  -s password
mysql -u$user -e "create database librehatti;" -p$password

cd src/librehatti/

sed -i -e "s/'NAME': 'db_name'/'NAME': 'librehatti'/g" settings.py
sed -i -e "s/'USER': 'db_user'/'USER': '$user'/g" settings.py
sed -i -e "s/'PASSWORD': 'db_password'/'PASSWORD': '$password'/g" settings.py

cd ../
python manage.py syncdb
