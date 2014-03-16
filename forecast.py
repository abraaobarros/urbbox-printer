#!/usr/bin/python

# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from Yahoo! weather, prints current conditions and
# forecasts for next two days.  See timetemp.py for a different
# weather example using nice bitmaps.
# Written by Adafruit Industries.  MIT license.
# 
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
# 
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import urllib, time,json, urllib2
from Adafruit_Thermal import *
from xml.dom.minidom import parseString

# WOEID indicates the geographic location for the forecast.  It is
# not a ZIP code or other common indicator.  Instead, it can be found
# by 'manually' visiting http://weather.yahoo.com, entering a location
# and requesting a forecast, then copy the number from the end of the
# current URL string and paste it here.
username = 'demo'
password = '123456'

# Dumps one forecast line to the printer
def forecast(idx):
	tag     = 'yweather:forecast'
	day     = dom.getElementsByTagName(tag)[idx].getAttribute('day')
	lo      = dom.getElementsByTagName(tag)[idx].getAttribute('low')
	hi      = dom.getElementsByTagName(tag)[idx].getAttribute('high')
	cond    = dom.getElementsByTagName(tag)[idx].getAttribute('text')
	printer.print(day + ': low ' + lo )
	printer.print(deg)
	printer.print(' high ' + hi)
	printer.print(deg)
	printer.println(' ' + cond)

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# Fetch forecast data from Yahoo!, parse resulting XML
# dom = parseString(urllib.urlopen(
#         'www.urbbox.com.br' + WOEID).read())

# make request
# headers = {
#     'Host': 'urbbox.com.br',
#     'Connection': 'keep-alive',
#     'Origin': 'http://www.urbbox.com.br',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
#     'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
#     'Referer': 'http://www.urbbox.com.br/admin',
#     'Accept-Encoding': 'gzip,deflate,sdch',
#     'Accept-Language': 'en-US,en;q=0.8',
#     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#     'Cookie': 'PHPSESSID=lvetilatpgs9okgrntk1nvn595'
# }

# data = {
#     'username': 'demo',
# 	'password': '123456'
# }

# data = urllib.urlencode(data)
# req = urllib2.Request('https://www.urbbox.com.br/admin', data, headers) 
# response = urllib2.urlopen(req)



# Print heading
printer.inverseOn()
printer.print('{:^32}'.format("Abraao e muito foda"))
printer.inverseOff()

# # Print current conditions
# printer.boldOn()
# printer.print('{:^32}'.format('Current conditions:'))
# printer.boldOff()
# printer.print('{:^32}'.format(
#   dom.getElementsByTagName('pubDate')[0].firstChild.data))
# temp = dom.getElementsByTagName('yweather:condition')[0].getAttribute('temp')
# cond = dom.getElementsByTagName('yweather:condition')[0].getAttribute('text')
# printer.print(temp)
# printer.print(deg)
# printer.println(' ' + cond)
# printer.boldOn()

# # Print forecast
# printer.print('{:^32}'.format('Forecast:'))
# printer.boldOff()
forecast(0)
forecast(1)

printer.feed(3)
