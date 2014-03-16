from Adafruit_Thermal import *
import json

import httplib, urllib

params = urllib.urlencode({'@username': 'demo', '@password': '123456'})
headers = {"Content-type": "application/x-www-form-urlencoded",
	           "Accept": "text/plain"}
conn = httplib.HTTPConnection("www.urbbox.com.br/admin?format=json")
conn.request("POST", "", params, headers)
response = conn.getresponse()



printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
printer.println(response.read())

