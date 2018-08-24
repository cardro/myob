# mongod --port 27017 --dbpath "D:\test data"

# def addInvoiceToInventory(itemName, itemVolume, itemPrice):
# 	documentExists = checkIfDocumentExists(itemName)
# 	print(documentExists)
# 	if documentExists is True:
# 		updateDocument(itemName, itemVolume, itemPrice)
# 	else:
# 		createDocument(itemName, itemVolume, itemPrice)
# addInvoiceToInventory()

from pymongo import MongoClient
import json
import csv
import uuid
from random import randint
import statistics
import datetime
import statistics
import time 

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
	ap = 0
	for i in docs:
		invID = i["invoiceID"]
		invID.append(invoiceDict["invoiceNumber"])
		pl = i["priceList"]
		pl.append(invoiceDict["total"])
		if invoiceDict["unitOfMeasure"] == "Weight":
			wl = i["weightList"]
			wl.append(invoiceDict["quantity"])
			s = sum(wl)
			ap = sum(pl)/s
			db["inventory"].update_one({"IngredientName":invoiceDict['itemName']},
				{"$set":
					{
					"invoiceID" : invID,
					"priceList" : pl,
					"weightList" : wl,
					"averagePrice" : ap,
					"stock" : s
					}
				}
			)
		elif invoiceDict["unitOfMeasure"] == "Volume":
			vl = i["volumeList"]
			vl.append(invoiceDict["quantity"])
			s = sum(vl)
			ap = sum(pl)/s
			db["inventory"].update_one({"IngredientName":invoiceDict['itemName']},
				{"$set":
					{
					"invoiceID" : invID,
					"priceList" : pl,
					"volumeList" : vl,
					"averagePrice" : ap,
					"stock" : s
					}
				}
			)
	
def createInventoryItemWithNewInvoice(invoiceDict):
	doc = {}
	doc["IngredientName"] = invoiceDict["itemName"]
	doc["invoiceID"] = [] 
	doc["invoiceID"].append(invoiceDict["invoiceNumber"])
	doc["priceList"] = []
	doc["priceList"].append(invoiceDict["total"])
	doc["averagePrice"] = invoiceDict["total"]
	if invoiceDict["unitOfMeasure"] == "Weight":
		doc["stock"] = invoiceDict["quantity"]
		doc["weightList"] = [invoiceDict["quantity"]]
	elif invoiceDict["unitOfMeasure"] == "Volume":
		doc["stock"] = invoiceDict["quantity"]
		doc["volumeList"] = [invoiceDict["quantity"]]
	doc["level"] = "low"
	db["inventory"].insert_one(doc)

def checkForPriceChange(invoiceDict):
	unitPrice = invoiceDict["quantity"]/invoiceDict["total"]
	docs = db["inventory"].find({"IngredientName":invoiceDict['itemName']})
	for i in docs:
		if invoiceDict["unitOfMeasure"] == "Weight":
			inventoryPrice = sum(i["weightList"])/sum(i["priceList"])
		elif invoiceDict["unitOfMeasure"] == "Volume":
			inventoryPrice = sum(i["volumeList"])/sum(i["priceList"])
	if unitPrice != inventoryPrice:
		return True
	else:
		return False

def updateCocktailPrice(invoiceDict):
	cocktailList = getCocktailsAffected(invoiceDict["itemName"])
	for cocktail in cocktailList:
		setCocktailPrice(cocktail)

def setCocktailNamesToIngredients():
	doc = db["ingredient"].find()
	ingredientList = []
	for i in doc:
		ingredientList.append(i["IngredientName"])
	# print(ingredientList)
	ingredientDict = {}
	for key in ingredientList:
		ingredientDict[key] = []
	doc1 = db["cocktails"].find()
	for j in doc1:
		# print(j["Ingredients"])
		for key,value in j["Ingredients"].items():
			for name in ingredientList:
				if key in name:
					# ingredientDict[name] = []
					ingredientDict[name].append(j["CocktailName"])
	# print(ingredientDict)
	for i in ingredientList:
		# print(i)
		db["ingredient"].update_one({"IngredientName":i},
			{"$set":
				{
					"cocktails" : ingredientDict[i]
			}})

def getCocktailsAffected(itemName):
	try:
		doc = db["ingredient"].find_one({"IngredientName":itemName})["cocktails"]
		ans = []
		for i in doc:
			ans.append(i)
		return ans
	except Exception as e:
		print("Not used in any cocktail")	
		pass
	

def createIngredientItemWithNewInvoice(invoiceDict):
	db["ingredient"].insert_one({"IngredientName" : invoiceDict["itemName"]})

def getPricePerPart(ingName):
	doc = db["inventory"].find_one({"IngredientName":ingName})["averagePrice"]
	return float(doc)

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
	for k in t1:
		d1[k[0]] = [k[1],k[2]]
		cp += k[2]
	sp = cp*2
	db["cocktails"].update_one({"CocktailName":cocktail},
		{"$set":{"Ingredients" : d1,"Cost Price" : cp,"Selling Price" : sp}})

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
		# pl = i["averagePrice"]
		# ap = pl[-1]
		# for index,value in enumerate(pl):
		# 	temp = pl[0:index+1]
		# 	ap.append(temp)
	
# changeAveragePriceToList()

# def cocktailPriceDifference():

# def insertRecipeToCollection():
# 	d = {}
# 	with open("D:/Cardo/uc/sem 2/MYOB/data.csv","r") as datafile:
# 		r = csv.reader(datafile)
# 		for rownum, row in enumerate(r):
# 			# print("*")
# 			if rownum<1:
# 				continue
# 			else:
# 				for i in range(1,8):
# 					if i != "":
# 						d[row[i]] = row[i+7]
# 				# vol = 		
# 				db["recipe"].insert({
# 					"Cocktail": row[0],
# 					"recipe":d,
# 					"Volume":row[-2],
# 					"Cost":row[-1]
# 					},check_keys=False)
# 				d = {}

# def insertIngredientsToCollection():
# 	d = {}
# 	with open("D:/Cardo/uc/sem 2/MYOB/data.csv") as datafile:
# 		r = csv.reader(datafile)
# 		for rownum,row in enumerate(r):
# 			db["recipe"].insert_one({"Cocktail":key})
# 			for j in value:
# 				d[j[0]]= j[1]
# 			db["recipe"].update_one({"Cocktail":key},{"$set":{"ingredients":d}})
# 			d = {}

# def createDocument(itemName, itemVolume, itemPrice):
# 	db["inventory"].insert_one(
# 		{
# 			"Ingredient":itemName,
# 			"Volume" : [itemVolume],
# 			"Price" : [itemPrice]
# 		}
# 	)

# def updateDocument(itemName, itemVolume, itemPrice):
# 	print("yolo")
# 	db["inventory"].update(
# 		{
# 			"Ingredient":itemName
# 			},
# 		{"$push":
# 			{
# 				"Volume" : itemVolume,
# 				"Price" : itemPrice
# 			}
# 		},
# 		upsert = True
# 	)

# def checkIfDocumentExists(itemName):
# 	print("checkIfDocumentExists called")
# 	if(db["inventory"].find({"Ingredient":itemName}).count() > 0):
# 		return True
# 	else:
# 		return False

# def setPricePerMl(ingName):
# 	doc = newdb["ingredient"].find({"IngredientName":ingName}) 
# 	price = 0
# 	vol = 0
# 	for i in doc:
# 		price = i["Price"]
# 		vol = i["Volume"]
# 	val = (price/vol)
# 	print(val)
# 	newdb["ingredient"].update_one(
# 		{"IngredientName":ingName},
# 			{"$set":
# 				{"PricePerml" : val 
# 				}
# 			},
# 			upsert = True
# 		)

# def setPricePerGram(ingName):
# 	doc = newdb["ingredient"].find({"IngredientName":ingName}) 
# 	price = 0
# 	weight = 0
# 	for i in doc:
# 		price = i["Price"]
# 		weight = i["Weight"]
# 	val = (price/weight)
# 	print(val)
# 	newdb["ingredient"].update_one(
# 		{"IngredientName":ingName},
# 			{"$set":
# 				{"PricePergram" : val 
# 				}
# 			},
# 			upsert = True
# 		)

# def getPricePerGram(ingName):	
# 	doc = db["ingredient"].find({"IngredientName":ingName})
# 	price = -1
# 	for i in doc:
# 		price = i["PricePergram"]
# 	return float(price)

# def getPricePerML(ingName):	
# 	doc = db["inventory"].find({"IngredientName":ingName})
# 	price = -1
# 	for i in doc:
# 		price = i["averagePrice"]
# 	return float(price)

# getPricePerML("new item")

# def setPricePerPart(ingName):
# 	doc = newdb["ingredient"].find({"IngredientName":ingName})
# 	for d in doc:
# 		if d["Volume"] > 0 and d["Weight"] == 0:
# 			setPricePerMl(ingName)
# 		elif d["Volume"] == 0 and d["Weight"] > 0:
# 			setPricePerGram(ingName)

# def setAllPricePerParts():
# 	doc = newdb["ingredient"].find({})
# 	for d in doc:
# 		setPricePerPart(d["IngredientName"])

# def setCostOfCocktail(CocktailName):
# 	doc = newdb["cocktails"].find_one({"CocktailName":CocktailName})["Ingredients"]
# 	costList = []
# 	ingredientList = []
# 	qty = []
# 	for key,value in doc.items():
# 	 	ingredientList.append(key)
# 	 	if (value[0] > 0):
# 	 		qty.append(value[0])
# 	 	else:
# 	 		qty.append(value[2])
# 	# print(qty)
# 	j = 0
# 	for i in ingredientList:
# 		a1 = getPricePerML(i)
# 		if(a1 != 0):
# 			costList.append([i,a1,1,qty[j]])
# 		else:
# 			costList.append([i,getPricePerGram(i),3,qty[j]])
# 		j = j + 1
# 	# print(costList)
# 	ing = {}
# 	cp = []
# 	for i in costList:
# 		cName = i[0]
# 		pricePerPart = i[1]
# 		listPosition = i[2]
# 		qty = i[3]
# 		ans = pricePerPart*qty
# 		cp.append(ans)
# 		l1 = []
# 		if (listPosition == 1):
# 			l1 = [qty,ans,0,0]
# 		else:
# 			l1 = [0,0,qty,ans]
# 		ing[cName] = l1
# 	costPrice = sum(cp)
# 	newdb["cocktails"].update_one({"CocktailName":CocktailName},
# 			{"$set":{"Ingredients":ing,
# 			"Cost Price": costPrice,
# 			"Selling Price": costPrice*2}},
# 		upsert = True)	

# def setAllCocktailPrices():
# 	doc = newdb["cocktails"].find({})
# 	for d in doc:
# 		# print(d["CocktailName"])
# 		setCostOfCocktail(d["CocktailName"])

# def getAllIngredients():
# 	doc = newdb["ingredient"].find({})
# 	ingredientList = []
# 	for d in doc:
# 		ingredientList.append(d["IngredientName"])
# 	return ingredientList

# def addIngredientsToInventory(inventoryList):
# 	for i in inventoryList:
# 		newdb["inventory"].insert_one(
# 			{
# 				"IngredientName":i,
# 				"invoiceID" : ["0"],
#     			"priceList" : [0],
#     			"volumeList" : [0],
#     			"averagePrice" : 0,
#     			"stock" : 0,
#     			"level" : "low"}
#     			)

# def updateVolumeInInventory(newInvoiceList):
# 	newdb["inventory"].update_one({"IngredientName":newInvoiceList[0]},
# 		{"$push":
# 		{	"invoiceID": randint(0,1000000),
# 			"priceList":float(newInvoiceList[1]),
# 			"volumeList":float(newInvoiceList[2])
# 			}
# 		})

# def updateWeightInInventory(newInvoiceList):
# 	newdb["inventory"].update_one({"IngredientName":newInvoiceList[0]},
# 		{"$push":
# 		{	"invoiceID": randint(0,1000000),
# 			"priceList":float(newInvoiceList[1]),
# 			"weightList":float(newInvoiceList[2])
# 			}
# 		})
# 	doc = newdb["inventory"].find({"IngredientName":newInvoiceList[0]})
# 	avgPrice = 0
# 	stock = 0
# 	for i in doc:
# 		avgPrice = statistics.mean(i["priceList"])
# 		stock = sum(i["weightList"])
# 	newdb["inventory"].update_one({"IngredientName":newInvoiceList[0]},
# 		{"$set":
# 		{	"averagePrice": avgPrice,
# 			"stock": stock
# 			}
# 		})

# def updateInventory(newInvoiceList):
# 	if newInvoiceList[3] == "v":
# 		updateVolumeInInventory(newInvoiceList)
# 	elif newInvoiceList [3] == "w":
# 		updateWeightInInventory(newInvoiceList)