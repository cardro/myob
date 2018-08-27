# mongod --port 27017 --dbpath "D:\test data"
# https://secure.myob.com/oauth2/account/authorize?client_id=[2c4hxqjuee8tzwmv9dtusuca]&redirect_uri=[http://ec2-18-221-93-157.us-east-2.compute.amazonaws.com]&response_type=code&scope=la.global


from pymongo import MongoClient
import json
import csv
import uuid
from random import randint
import statistics
import datetime
import statistics
from time import strftime

client = MongoClient('localhost', 27017)
db = client["test"]

def checkIfItemExistsInInventory(invoiceDict):
	if(db["inventory"].find({"IngredientName":invoiceDict['itemName']}).count()>0):
		return True
	else:
		return False

def updateInventoryWithNewInvoice(invoiceDict):
	docs = db["inventory"].find({"IngredientName":invoiceDict['itemName']})
	pl = []
	invID = []
	wl = []
	vl = []
	s = 0
	ap = []
	for i in docs:
		invID = i["invoiceID"]
		invID.append(invoiceDict["invoiceNumber"])
		pl = i["priceList"]
		pl.append(invoiceDict["total"])
		ap = i["averagePrice"]
		if "addedOn" in i.keys():
			timeStamp = i["addedOn"]
		else:
			timeStamp = []
		if invoiceDict["unitOfMeasure"] == "Weight":
			wl = i["weightList"]
			wl.append(invoiceDict["quantity"])
			s = sum(wl)
			ap.append(sum(pl)/s)
			timeStamp.append(strftime("%d-%m-%Y %H:%M:%S"))
			db["inventory"].update_one({"IngredientName":invoiceDict['itemName']},
				{"$set":
					{
					"invoiceID" : invID,
					"priceList" : pl,
					"weightList" : wl,
					"averagePrice" : ap,
					"stock" : s,
					"addedOn" : timeStamp
					}
				}
			)
		elif invoiceDict["unitOfMeasure"] == "Volume":
			vl = i["volumeList"]
			vl.append(invoiceDict["quantity"])
			s = sum(vl)
			ap.append(sum(pl)/s)
			timeStamp.append(strftime("%d-%m-%Y %H:%M:%S"))
			db["inventory"].update_one({"IngredientName":invoiceDict['itemName']},
				{"$set":
					{
					"invoiceID" : invID,
					"priceList" : pl,
					"volumeList" : vl,
					"averagePrice" : ap,
					"stock" : s,
					"addedOn" : timeStamp
					}
				}
			)
	print("updated item {0} in inventroy".format(invoiceDict['itemName']))
	
def createInventoryItemWithNewInvoice(invoiceDict):
	doc = {}
	doc["IngredientName"] = invoiceDict["itemName"]
	doc["invoiceID"] = [] 
	doc["invoiceID"].append(invoiceDict["invoiceNumber"])
	doc["priceList"] = []
	doc["priceList"].append(invoiceDict["total"])
	doc["averagePrice"] = []
	doc["averagePrice"].append(float(invoiceDict["total"]/invoiceDict["quantity"]))
	doc["addedOn"] = [strftime("%d-%m-%Y %H:%M:%S")]
	if invoiceDict["unitOfMeasure"] == "Weight":
		doc["stock"] = invoiceDict["quantity"]
		doc["weightList"] = [invoiceDict["quantity"]]
	elif invoiceDict["unitOfMeasure"] == "Volume":
		doc["stock"] = invoiceDict["quantity"]
		doc["volumeList"] = [invoiceDict["quantity"]]
	doc["level"] = "low"
	db["inventory"].insert_one(doc)

def checkForPriceChange(invoiceDict):
	unitPrice = float(invoiceDict["total"]/invoiceDict["quantity"])
	docs = db["inventory"].find({"IngredientName":invoiceDict['itemName']})
	for i in docs:
		if invoiceDict["unitOfMeasure"] == "Weight":
			inventoryPrice = i["averagePrice"][-1]
		elif invoiceDict["unitOfMeasure"] == "Volume":
			inventoryPrice = i["averagePrice"][-1]
	print("Inventory price = {0} \nUnit price = {1} \nPrice difference = {2}".format(inventoryPrice,unitPrice,(inventoryPrice-unitPrice)))
	if unitPrice != inventoryPrice:
		return True
	else:
		return False

def updateCocktailPrice(invoiceDict):
	cocktailList = getCocktailsAffected(invoiceDict["itemName"])
	for cocktail in cocktailList:
		print("setting price of {0}".format(cocktail))
		setCocktailPrice(cocktail)

def setCocktailNamesToIngredients():
	doc = db["ingredient"].find()
	ingredientList = []
	for i in doc:
		ingredientList.append(i["IngredientName"])
	ingredientDict = {}
	for key in ingredientList:
		ingredientDict[key] = []
	doc1 = db["cocktails"].find()
	for j in doc1:
		for key,value in j["Ingredients"].items():
			for name in ingredientList:
				if key in name:
					ingredientDict[name].append(j["CocktailName"])
	for i in ingredientList:
		db["ingredient"].update_one({"IngredientName":i},
			{"$set":{"cocktails" : ingredientDict[i]}})

def getCocktailsAffected(itemName):
	print(itemName+"#####")
	try:
		doc = db["ingredient"].find_one({"IngredientName":itemName})["cocktails"]
		ans = []
		print(doc)
		for i in doc:
			ans.append(i)
		return ans
	except Exception as e:
		print("Not used in any cocktail")	
		pass

def createIngredientItemWithNewInvoice(invoiceDict):
	db["ingredient"].insert_one({"IngredientName" : invoiceDict["itemName"]})

def getPricePerPart(ingName):
	doc = db["inventory"].find_one({"IngredientName":ingName})["averagePrice"][-1]
	return doc

def changeAveragePriceToList():
	doc = db["inventory"].find()
	ap = []
	for i in doc:
		if "weightList" in i.keys():
			bl = i["weightList"]
		if "volumeList" in i.keys():
			bl = i["volumeList"]
		pl = i["priceList"]
		for index,value in enumerate(pl):
			t1 = sum(pl[0:index+1])
			t2 = sum(bl[0:index+1])
			t3 = t1/t2
			ap.append(t3)
		print(ap)
		db["inventory"].update_one({"IngredientName":i["IngredientName"]},{
			"$set":{"averagePrice" : ap}})	
		ap =[]

def setCocktailPrice(cocktail):
	doc = db["cocktails"].find_one({"CocktailName":cocktail})["Ingredients"]
	costList = []
	ingredientList = []
	qty = []
	t1 = []
	t2 = []
	for key,value in doc.items():
	 	ingredientList.append(key)
	 	t2 = [key,value[0]]
	 	t1.append(t2)
	j=0
	for i in ingredientList:
		t1[j].append(getPricePerPart(i)*t1[j][1])  
		j = j+1
	d1 = {}
	cp = 0
	acp = db["cocktails"].find_one({"CocktailName":cocktail})["costPrice"]
	asp = db["cocktails"].find_one({"CocktailName":cocktail})["sellingPrice"]
	for k in t1:
		d1[k[0]] = [k[1],k[2]]
		cp += k[2]
	acp.append(cp+10)
	asp.append((cp+10)*1.75)
	ccp = acp[-1]
	csp = asp[-1]  
	db["cocktails"].update_one({"CocktailName":cocktail},
		{"$set":{"Ingredients" : d1,"costPrice" : acp,"sellingPrice" : asp, "currentCostPrice": ccp, "currentSellingPrice":csp}})
	print("cost price updated for {0} to {1}".format(cocktail,ccp))

def setAllCocktailPrices():
	for i in db["cocktails"].find({}):
		setCocktailPrice(i["CocktailName"])

def cocktailPriceDifference(invoiceDict):
	cocktailList = getCocktailsAffected(invoiceDict["itemName"])
	for cocktail in cocktailList:
		l1 = db["cocktails"].find_one({"CocktailName":cocktail})["costPrice"]
		print(cocktail)
		if (l1[-1] != l1[-2]):
			print("price changed from {0} to {1}".format(l1[-2],l1[-1]))
			return (True,l1[-2],l1[-1])
		else:
			return (False,l1[-2],l1[-1])

def updateStock(saleDict):
	name = saleDict["name"]
	doc = db["cocktails"].find({"CocktailName":name})
	for i in doc:
		for key,value in i["Ingredients"].items():
			stock = db["inventory"].find_one({"IngredientName":key})["stock"]
			stock = float(stock-value[0])
			db["inventory"].update_one({"IngredientName":key},{"$set":{"stock" : stock}})
# cocktailPriceDifference({'itemName': 'lime'})

def addSaleToDB(saleDict):
	doc = db["sales"].find({"cocktail":saleDict["name"],"date":saleDict["issueDate"]})
	if doc.count() == 0:
		print("yes")
		addNewSale(saleDict)
	else:
		print("yo")
		updateCurrentDaySale(saleDict)

def addNewSale(saleDict):
	doc = {}
	doc["cocktail"] = saleDict["name"]
	doc["quantity"] = [saleDict["quantity"]]
	doc["date"] = saleDict["issueDate"]
	doc["time"] = [strftime("%H:%M:%S")]
	doc["total"] = sum(doc["quantity"])
	doc["profit"] = float(saleDict["price"]-db["cocktails"].find_one({"CocktailName":saleDict["name"]})["currentSellingPrice"]) 
	db["sales"].insert_one(doc)

def updateCurrentDaySale(saleDict):
	print("works")
	doc = db["sales"].find_one({"cocktail":saleDict["name"],"date":saleDict["issueDate"]})
	q = doc["quantity"]
	q.append(saleDict["quantity"])
	print(q)
	t = doc["time"]
	t.append(strftime("%H:%M:%S"))
	print(t)
	tot = doc["total"]+saleDict["quantity"]
	p = float(doc["profit"] + (saleDict["price"]-db["cocktails"].find_one({"CocktailName":saleDict["name"]})["currentSellingPrice"]))
	db["sales"].update_one({"cocktail":saleDict["name"],"date":saleDict["issueDate"]},{
		"$set":{
		"quantity" : q,
		"time" : t,
		"total" : tot,
		"profit" : p
		}
		})
	
def checkNotify():
	doc = db["sales"].find()
	s = 0
	for i in doc:
		s = s + i["profit"]
		# print(i["profit"])
	return s