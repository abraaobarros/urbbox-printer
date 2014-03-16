from Adafruit_Thermal import *
import json

import requests

printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

#login
login_data =  {'username':'demo', 'password':'123456'}
s = requests.session()
s.post('http://www.urbbox.com.br/admin',login_data)

r = s.get('http://www.urbbox.com.br/backend?format=json')


pedidos = json.loads(r.text)["pedidos"]
for p in pedidos:
	printer.println("*********** Mesa "+p["rua"] + " ***********")
	printer.println(str(p["listaItens"][0]["numero"]) + "   " + p["listaItens"][0]["nome"].encode('utf8') + "  -  "+ p["listaItens"][0]["observacao"].encode('utf8') +"  "+ str(p["listaItens"][0]["quantidade"]))
	printer.feed(2)
printer.feed(4)


