import stomp
import time
import json
import settings

def fileBody(filename):
   with open(filename) as f_in:
       return(json.load(f_in))

fn = "D:/Cardo/uc/sem 2/MYOB/inputFiles/invoices/1.txt"
data = fileBody(fn)
# print(fn.split("/")[-2])
conn = stomp.Connection([(settings.STOMP_ADDRESS,settings.STOMP_PORT)])
conn.start()
conn.connect(settings.STOMP_CONNECTOR_USER,settings.STOMP_CONNECTOR_PASSWORD)

if fn.split("/")[-2] == "invoices":
	print("New invoice detected in the system")
	conn.send(body = str(data),destination = settings.STOMP_INVOICE_QUEUE)
elif fn.split("/")[-2] == "sales":
	print("New sale detected in the system")
	conn.send(body = str(data),destination = settings.STOMP_SALE_QUEUE)
	
time.sleep(1)
