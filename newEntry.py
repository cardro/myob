##################################################################################################################
# with open("D:/Cardo/uc/sem 2/MYOB/code/invoiceDocument") as f:
# 	data = json.loads(f.read())

# invoiceDict["uid"] = data["uid"]
# invoiceDict["invoiceNumber"] = data["invoiceNumber"]
# invoiceDict["issueDate"] = data["issueDate"]
# invoiceDict["itemName"] = data["lines"][0]["item"]["name"]
# invoiceDict["itemUid"] = data["lines"][0]["item"]["uid"]
# invoiceDict["unitOfMeasure"] = data["lines"][0]["unitOfMeasure"]
# invoiceDict["quantity"] = data["lines"][0]["quantity"]
# invoiceDict["unitPrice"] = data["lines"][0]["unitPrice"]
# invoiceDict["total"] = data["lines"][0]["total"]
# invoiceDict["purchaseOrderNumber"] = data["purchaseOrderNumber"]
####################################################################################################################


import json
import pretty
import pprint
from pymongo import MongoClient
import mongoCode

# print("***********")

data = {}
invoiceDict = {}

client = MongoClient('localhost', 27017)
db = client["test"]


invoiceDict = {
 'uid': '2',
 'invoiceNumber': 'IV00000002',
 'issueDate': '2014-08-19', 
 'itemName': 'salt', 
 'itemUid': '2', 
 'unitOfMeasure': 'Weight', 
 'quantity': 7500, 
 'total': 10, 
 'purchaseOrderNumber': 'PO0000002'}



def flow(invoiceDict):
	docExists = mongoCode.checkIfItemExistsInInventory(invoiceDict)
	# yes
	priceChange = False
	if docExists is True:
		priceChange = mongoCode.checkForPriceChange(invoiceDict)
		# yes
		mongoCode.updateInventoryWithNewInvoice(invoiceDict)
		# change invoice
		if priceChange:
			mongoCode.cocktailPriceDifference(invoiceDict)
			# Check whats the change amount
			mongoCode.updateCocktailPrice(invoiceDict)
			# update price change

	else:
		mongoCode.createInventoryItemWithNewInvoice(invoiceDict)
		mongoCode.createIngredientItemWithNewInvoice(invoiceDict)
		# add ingredient to inventory
	# print(docExists)
flow(invoiceDict)
mongoCode.setCocktailNamesToIngredients()

