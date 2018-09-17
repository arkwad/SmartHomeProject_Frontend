# ==========================================================
#   File: http_client_test.py
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

## !!Dependencies!!: sudo pip install requests
import requests
import time
import json

if __name__ == "__main__":
    try:
        serverUrl = 'http://127.0.0.1:5000/measurements'

	temp = ["23", "20", "26","21", "23", "25"]
	pressure = ["102", "1002", "999","1100", "1050", "1000"]
	humidity = ["71", "55", "54","59", "23", "31"]
	movement = ["false", "false", "false","true", "true", "true"]
	air = ["64", "150", "96","111", "115", "85"]
	for x in range(0, 9):
		data  = "{\"name\":\"bedroom\",\"temperature\":"+temp[x]+",\"humidity\":"+humidity[x]+",\"pressure\":"+pressure[x]+",\"movement_detected\":"+movement[x]+",\"air_quality\":"+air[x]+"}"
		requests.post(serverUrl, data, timeout = 5)

		print data
        	time.sleep(2)

    except KeyboardInterrupt:
        print ("Cya!")
