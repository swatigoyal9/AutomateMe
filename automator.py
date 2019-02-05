import os
import ipaddress
import subprocess
import mysql.connector
from bs4 import BeautifulSoup
import datetime

#------fetching data from testcases
files = os.listdir("/root/Cyber/testcases/")
txt_files = filter(lambda x: x[-4:] == '.txt', files)


for x in txt_files:
    with open(x, 'r') as text_file:
        soup = BeautifulSoup(text_file.read(), "html.parser")
        #----- getting data from testcase in form of ipaddress, timestamp, port, destination ip and destination port
        ip_address = soup.find('ip_address').text if soup.find('ip_address') is not None else None
        py_timestamp = soup.find('timestamp').text if soup.find('timestamp') is not None else None
        port = soup.find('port').text if soup.find('port') is not None else None
        destination_ip = soup.find('destination_ip').text if soup.find('destination_ip') is not None else None
        destination_port = soup.find('destination_port').text if soup.find('destination_port') is not None else None
        #-------timezone related manipulation
        format = '%Y-%m-%dT%H:%M:%SZ'
        time1 = None
        formats = [
            '%Y-%m-%dT%H:%M:%s.%SSSZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%f+00:00',
            '%Y-%m-%dT%H:%M:%S+00:00'
        ]
        for frmt in formats:
            try:
                time1 = datetime.datetime.strptime(py_timestamp, str(frmt))
            except ValueError as ex:
                continue
        if time1 is  None:
            print("Invalid File: "+x)
            continue

        py_timestamp = time1 - datetime.timedelta(hours=4)
        time2 = py_timestamp
        time4 = time2
        py_timestamp = py_timestamp.strftime(format)
        py_minute = time2.minute
        time2 = time2.hour+1

        py_timestamp2 = str(py_timestamp)
        py_timestamp3 = py_timestamp2[:-6]
        time3 = str(time2)
        if len(time3) == 1:
            time3 = '0'+time3
        #--------fetching data from natlogs
        file_name = 'nat.csv.20160321'+time3+'.csv.gz'
        command_output = None
        search_command = 'zgrep "' + py_timestamp3 + '" /root/Cyber/data/natlogs/'+file_name + ' | grep "' + ip_address +','+port+'"'
        command_output = subprocess.check_output(search_command, shell=True)
        if command_output==None:
            print("Sorry there is no log file regarding this data")
        else:
            split_output = command_output.split()
            arr = []
            arr1 = []
            for i in split_output:
                i = str(i)
                min_data = i.split(':')
                arr.append(min_data[1])

            for i in arr:
                q = int(i)
                w = int(py_minute)
                if(q>=w):
                    arr1.append(q-w)

                else:
                    arr1.append(w-q)
            e = arr1.index(min(arr1))
            r = str(split_output[e])
            split_2 = r.split(",")
            res_2 = split_2[2]
            #print(res_2)

        #db = MySQLdb.connect(host="localhost", port=3306, user="", passwd = "", db = "logs_db")

        #cursor = db.cursor()



        #time4 = str(time4)[:-5]
        #final = reduce(lambda a,b: a<<8 | b, map(int, res_2.split(".")))
            final = int(ipaddress.ip_address(res_2))
        #print(final)
            data = None
            try:
                try:
                    #------setting up sql connection---------
                    cnx = mysql.connector.connect(user='', password='', host='127.0.0.1', database='logs_db')
                    cursor = cnx.cursor(buffered=True)
                    #------query to get mac address------------
                    step3 = "select mac_string from dhcp where ip_decimal = '"+str(final)+"' and timestamp <= '"+str(time4)+"' order by timestamp desc;"
                    cursor.execute(step3)
                    data = cursor.fetchone()
                    #print(data)
                except mysql.connector.Error as err:
                    print("Something went wrong in dhcp database: {}".format(err))

            finally:
                cnx.close()

            if data ==None:
                print("No data found")

            for i in data:
                data1 = i
            username =0
            if "172.19." in res_2:

                    try:
                        try:
                            cnx = mysql.connector.connect(user='', password='', host='127.0.0.1', database='logs_db')
                            cursor = cnx.cursor(buffered=True)
                            #-------query to get username from radacct table if ipaddress starts with "172.19."-----
                            step4 ="select distinct username from radacct where CallingStationId = '"+data1+"';"
                            cursor.execute(step4)
                            data = cursor.fetchone()
                            for i in data:
                                username = i
                        except mysql.connector.Error as err:
                            print("Something went wrong in radacct database: {}".format(err))
                    finally:
                        cnx.close()
            else:
                    try:
                        try:
                            cnx = mysql.connector.connect(user='', password='', host='127.0.0.1', database='logs_db')
                            cursor = cnx.cursor(buffered=True)
                            step4 = "select distinct contact from contactinfo where mac_string = '" + data1 + "';"
                            #print(step4)
                            cursor.execute(step4)
                            data = cursor.fetchone()
                            for i in data:
                                username = i
                        except mysql.connector.Error as err:
                            print("Something went wrong in contactinfo database: {}".format(err))
                    finally:
                        #-------connection closed---------------
                        cnx.close()

            if username == 0:
                print("Sorry No user found")
            else:
                #-------printing final result-------------------
                print("*********Culprit Found**********")
                print("Username: "+username)
                print("Mac Address: "+data1)






