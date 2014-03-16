from Adafruit_Thermal import *
import json

import requests
# import RPi.GPIO as GPIO

# ledPin       = 18
# buttonPin    = 23

# GPIO.setmode(GPIO.BCM)

# # Enable LED and button (w/pull-up on latter)
# GPIO.setup(ledPin, GPIO.OUT)
# GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# # LED on while working
# GPIO.output(ledPin, GPIO.HIGH)
# time.sleep(30)

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
# GPIO.output(ledPin, GPIO.HIGH)

#login
login_data =  {'username':'demo', 'password':'123456'}
s = requests.session()
s.post('http://www.urbbox.com.br/admin',login_data)

r = s.get('http://www.urbbox.com.br/backend?format=json')


pedidos = json.loads(r.text)["pedidos"]
for p in pedidos:
	printer.justify('C')
	printer.println("**********************")
	printer.feed(1)
	printer.setSize('L')
	printer.boldOn()
	printer.println("Mesa "+p["rua"])
	printer.boldOff()
	printer.println(str(p["listaItens"][0]["numero"]) + "   " + p["listaItens"][0]["nome"].encode('utf8') + "  -  "+ p["listaItens"][0]["observacao"].encode('utf8') +"  "+ str(p["listaItens"][0]["quantidade"]))
	printer.feed(2)
printer.feed(4)
# GPIO.output(ledPin, GPIO.LOW)


