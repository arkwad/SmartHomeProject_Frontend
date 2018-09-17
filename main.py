# ==========================================================
#   File: main.py
#   Author: Arkadiusz Wadowski
#   Email: wadowski.arkadiusz@gmail.com
#   Created: 18.04.2018
# ==========================================================
'''
*  Copyright (c) 2018, Arkadiusz Wadowski
*  All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions are met:
*  1. Redistributions of source code must retain the above copyright
*     notice, this list of conditions and the following disclaimer.
*  2. Redistributions in binary form must reproduce the above copyright
*     notice, this list of conditions and the following disclaimer in the
*     documentation and/or other materials provided with the distribution.
*  3. Neither the name of the copyright holder nor the
*     names of its contributors may be used to endorse or promote products
*     derived from this software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
*  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
*  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
*  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
*  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
*  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
*  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
*  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
*  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
*  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
'''

from flask import Flask, request, render_template
import mysql.connector
import json
import time
import datetime

add_dev = ("INSERT INTO devices "
           "(name, temperature, humidity, pressure, air_quality, movement_detected, date) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s)")

find_device_last_record = ("SELECT * FROM SmartHome.devices WHERE id IN ( SELECT MAX(id) FROM SmartHome.devices GROUP BY name ) and name = %s;")

search_for_last_records = ("SELECT * FROM SmartHome.devices WHERE id IN ( SELECT MAX(id) FROM SmartHome.devices GROUP BY name );")

search_for_device_records_1h = ("SELECT * FROM SmartHome.devices WHERE "
				"DATE_SUB(NOW(), INTERVAL 3 DAY) < date "
				"and name = %s;")

search_for_device_records_30min =("SELECT * FROM SmartHome.devices WHERE "
				  "DATE_SUB(NOW(), INTERVAL 30 MINUTE) < date "
				  "and name = %s;")

search_for_device_records_15min =("SELECT * FROM SmartHome.devices WHERE "
				  "DATE_SUB(NOW(), INTERVAL 15 MINUTE) < date "
				  "and name = %s;")
app = Flask(__name__)
	
@app.route("/measurements", methods=['POST'])
def add_measurements():
    if request.method == 'POST':
	try:
	    # check if received json is correct
	    jdata = json.loads(request.data)
	except ValueError:
	    return "JSON NOK!"
	# set up connection with database
        cnx = mysql.connector.connect(user='arek', password='baza', host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock', database='SmartHome')
	# create cursor
        cursor = cnx.cursor()
	# get current timestamp 
	ts = time.time()
	# change format to acceptable by mysql
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	# prepare data set to be stored in database
    	data_dev = (jdata['name'], str(jdata['temperature']), str(jdata['humidity']), str(jdata['pressure']), str(jdata['air_quality']), str(jdata['movement_detected']), timestamp)
	# execute query to add row in table    	
	cursor.execute(add_dev, data_dev)
	# commit changes    	
	cnx.commit()
	# close database connection
    	cursor.close()
    	cnx.close()

	return "JSON OK!"

@app.route("/", methods=["GET"])
def root():
    return render_template('index.html')

@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html')

@app.route("/devices", methods=["GET"])
def devices():
    # set up connection with database
    cnx = mysql.connector.connect(user='arek', password='baza', host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock',  database='SmartHome')
    # create cursor
    cursor = cnx.cursor()
    cursor.execute(search_for_last_records)
    # get the search result
    data = cursor.fetchall()
    # commit changes 
    cnx.commit()
    # close database connection
    cursor.close()
    cnx.close()
    return render_template('devices.html', data = data)

@app.route("/devices/<device_name>", methods=["GET"])
def device_details(device_name):
    return render_template('device_details.html', device_name = device_name)

@app.route("/devices/<device_name>/<time>/<value>", methods=["GET"])
def device_measurements_filter(device_name, time, value):
    # set up connection with database
    cnx = mysql.connector.connect(user='arek', password='baza', host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock', database='SmartHome')
    # create cursor
    cursor = cnx.cursor()

    if time == "15min":
	cursor.execute(search_for_device_records_15min, (device_name,))
    elif time == "30min":
	cursor.execute(search_for_device_records_30min, (device_name,))
    elif time == "1h":
	cursor.execute(search_for_device_records_1h, (device_name,))
    else:
	return "Wrong time frame!"

    # get the search result
    data = cursor.fetchall()
    print data
    # commit changes 
    cnx.commit()
    # close database connection
    cursor.close()
    cnx.close()
    return render_template("device_measurements.html", device_name = device_name, time = time, value = value, data = data);

if __name__ == "__main__":
    app.run(host = '0.0.0.0')

