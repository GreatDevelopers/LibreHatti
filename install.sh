sudo apt-get install apache2 mysql-server python python-pip python-mysqldb
sudo pip install -r requirements.txt
sudo apt-get install exim4

while [ true ]
do 
    echo " To Conifgure Exim (a mail transfer agent)" 
    echo " To know how to configure Exim https://jasvirsinghgrewal91.wordpress.com/2013/06/23/e-mail-server-exim4/" 
    echo " Enter Y to start configuration else N"
    read config
    if [ "$config" == "Y" -o "$config" == "y" ]; 
    then
        sudo dpkg-reconfigure exim4-config
        echo "******************Information for Exim******************"
        echo "Enter a valid email address"
        read  user
        echo "Enter Password "
        read  -s password
        sudo sed '$ a\ *:$user@example.com: $password ' /etc/exim4/passwd.client
        break
    fi
    if [ "$config"  ==  "N" -o "$config" == "n" ]
    then    
        break
    fi
done

echo "******************Information for database******************"
echo "Enter DB_USER "
read  user
echo "Enter DB_Password "
read  -s password
mysql -u$user -e "create database librehatti;" -p$password

cd src/librehatti/

sed -i -e "s/'NAME': 'db_name'/'NAME': 'librehatti'/g" settings.py
sed -i -e "s/'USER': 'db_user'/'USER': '$user'/g" settings.py
sed -i -e "s/'PASSWORD': 'db_password'/'PASSWORD': '$password'/g" settings.py

cd ../
python manage.py makemigrations
python manage.py migrate
