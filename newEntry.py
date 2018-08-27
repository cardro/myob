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

# client = MongoClient('localhost', 27017)
# db = client["test"]


invoiceDict = {
 'uid': '2',
 'invoiceNumber': 'IV00000002',
 'issueDate': '2014-08-19', 
 'itemName': 'soda water', 
 'itemUid': '2', 
 'unitOfMeasure': 'Volume', 
 'quantity': 750, 
 'total': 1000, 
 'purchaseOrderNumber': 'PO0000002'}

def invoiceFlow(invoiceDict):
	print("invoiceFlow reached")
	docExists = mongoCode.checkIfItemExistsInInventory(invoiceDict)
	print("Item exists in inventory : {0}".format(docExists))
	priceChange = False
	cocktailPriceChange = False
	oldPrice = 0
	newPrice = 0
	if docExists is True:
		priceChange = mongoCode.checkForPriceChange(invoiceDict)
		print("price change : {0}".format(priceChange))
		mongoCode.updateInventoryWithNewInvoice(invoiceDict)
		if priceChange:
			mongoCode.updateCocktailPrice(invoiceDict)
			cocktailPriceChange, oldPrice,newPrice = mongoCode.cocktailPriceDifference(invoiceDict)
			if cocktailPriceChange:
				print("change of price")
	else:
		mongoCode.createInventoryItemWithNewInvoice(invoiceDict)
		mongoCode.createIngredientItemWithNewInvoice(invoiceDict)
	print(oldPrice)
	print(newPrice)

	if newPrice-oldPrice > 1:
		print("Notify")

invoiceFlow(invoiceDict)
# mongoCode.setCocktailNamesToIngredients()
# mongoCode.cocktailPriceDifference(invoiceDict)

saleDict = {
	"uid" : "59",
	"invoiceNumber" : "IV00000229",
	"issueDate" : "2014-08-19",
	"name" : "long island iced tea",
	"quantity" : 1,
	"purchaseOrderNumber" : "PO0000056",
	"price" : 4
}

def salesFlow(saleDict):
	print("sale flow called")
	# mongoCode.addSaleToDB(saleDict)
	# mongoCode.updateStock(saleDict)

# saleFlow(saleDict)

# sumProfit = mongoCode.checkNotify()
# if(sumProfit > 10 or sumProfit < -10):
# 	print("Notify {0}".format(sumProfit))