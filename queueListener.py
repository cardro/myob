import stomp
import time
import json
import newEntry
import settings

class invoiceListener(object):

	def __init__(self):
		self.message_list = []
	
	def on_message(self, headers, msg):
		data = json.dumps(msg)
		print(data)
		newEntry.invoiceFlow(data)

	def on_error(self):
		print("ERROR")

invCon = stomp.Connection([(settings.STOMP_ADDRESS,settings.STOMP_PORT)])
invCon.set_listener('invoiceListener', invoiceListener()) 
invCon.start()
invCon.connect(settings.STOMP_CONNECTOR_USER,settings.STOMP_CONNECTOR_PASSWORD)
invCon.subscribe(destination = settings.STOMP_INVOICE_QUEUE, id = 1, ack = 'auto')
time.sleep(1)


class salesListener(object):

	def __init__(self):
		self.message_list = []
	
	def on_message(self, headers, msg):
		data = json.dumps(msg)
		print(data)
		newEntry.salesFlow(data)

	def on_error(self):
		print("ERROR")

salesCon = stomp.Connection([(settings.STOMP_ADDRESS,settings.STOMP_PORT)])
salesCon.set_listener('salesListener', salesListener()) 
salesCon.start()
salesCon.connect(settings.STOMP_CONNECTOR_USER,settings.STOMP_CONNECTOR_PASSWORD)
salesCon.subscribe(destination = settings.STOMP_SALE_QUEUE, id = 1, ack = 'auto')
time.sleep(1)