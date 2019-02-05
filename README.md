

CONTENTS

I.	Installations Required

II.	MINIMUM SYSTEM REQUIREMENTS

III.	Libraries Imported

IV.	KNOWN ISSUES AND WORKAROUNDS

V.	Running file



I. Installations Required

In Kali
1. Start mysql by using command: service start mysql
2. Enter mysql: mysql
3. create database: ./create_table.sh
4. insert databae: ./insertcsv.sh
5. Install pip:
	apt-get update
	apt-get -y install python-pip
5. install mysql_connector:
	pip install MySQL-python
	pip install --user mysql-connector-python
	sudo apt-get install python-dev
	sudo apt-get install libmysqlclient-dev
6. install beautifulsoup4
	pip install beautifulsoup4
7. save files under Cyber folder. files are:
	data, testcases and scripts
8. unzip natlogs.tar in data folder


II. MINIMUM SYSTEM REQUIREMENTS 


In Kali
1. mysql should be running
2. python should be running
3. pip should be running



III. Libraries Imported
import os
import ipaddress
import subprocess
import mysql.connector
from bs4 import BeautifulSoup
import datetime

IV. KNOWN ISSUES AND WORK AROUNDS 
1. Sometimes default python which is python2 will not work. For that purpose we can switch to python3
2. Instead of mysql_connector, we can use MySQLdb as well


V.Run the file
1. using nano editor: nano automator.py
2. run: python ./automator.py






