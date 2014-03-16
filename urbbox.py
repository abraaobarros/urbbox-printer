from Adafruit_Thermal import *
import json

import requests
import subprocess, time, Image, socket
import RPi.GPIO as GPIO

ledPin       = 18
buttonPin    = 23
holdTime     = 4     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
dailyFlag    = False # Set after daily trigger occurs


GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)

# LED on while working
GPIO.output(ledPin, GPIO.HIGH)
time.sleep(30)




printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)



#login
login_data =  {'username':'demo', 'password':'123456'}
id_est = 1323001
s = requests.session()
s.post('http://www.urbbox.com.br/admin',login_data)

r = s.get('http://www.urbbox.com.br/backend?format=json')
pedidos = json.loads(r.text)["pedidos"]

def print_list_orders():
	GPIO.output(ledPin, GPIO.HIGH)
	for p in pedidos:
		printer.justify('C')
		printer.println("**********************")
		printer.feed(1)
		printer.setSize('L')
		printer.boldOn()
		printer.doubleHeightOn()
		printer.println("Mesa "+p["rua"])
		printer.boldOff()
		printer.println(str(p["listaItens"][0]["numero"]) + "   " + p["listaItens"][0]["nome"].encode('utf8') + "  -  "+ p["listaItens"][0]["observacao"].encode('utf8') +"  "+ str(p["listaItens"][0]["quantidade"]))
		printer.feed(2)
		printer.doubleHeightOFF()
	printer.feed(4)
	GPIO.output(ledPin, GPIO.LOW)

n_pedido = 0
def check_novos_pedidos():
	r2 = s.get("http://2.preguicosotest.appspot.com/pedidos/1323001")
	print r2.text
	qtd = json.loads(r2.text)['qtd']
	if n_pedido != qtd:
		print_list_orders()
		n_pedido=qtd


def tap():
	printer.println("Apertei")
def hold():
	printer.println("Segurei")

check_novos_pedidos()

# Poll initial button state and time
prevButtonState = GPIO.input(buttonPin)
prevTime        = time.time()
tapEnable       = False
holdEnable      = False

while(True):
	# Poll current button state and time
  buttonState = GPIO.input(buttonPin)
  t= time.time()

  # Has button state changed?
  if buttonState != prevButtonState:
    prevButtonState = buttonState   # Yes, save new state/time
    prevTime        = t
  else:                             # Button state unchanged
    if (t - prevTime) >= holdTime:  # Button held more than 'holdTime'?
      # Yes it has.  Is the hold action as-yet untriggered?
      if holdEnable == True:        # Yep!
        hold()                      # Perform hold action (usu. shutdown)
        holdEnable = False          # 1 shot...don't repeat hold action
        tapEnable  = False          # Don't do tap action on release
    elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
      # Yes.  Debounced press or release...
      if buttonState == True:       # Button released?
        if tapEnable == True:       # Ignore if prior hold()
          tap()                     # Tap triggered (button released)
          tapEnable  = False        # Disable tap and hold
          holdEnable = False
      else:                         # Button pressed
        tapEnable  = True           # Enable tap and hold actions
        holdEnable = True
 
  if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
    GPIO.output(ledPin, GPIO.HIGH)
  else:
    GPIO.output(ledPin, GPIO.LOW)

  if t > nextInterval:
    nextInterval = t + 5.0
    tap()

