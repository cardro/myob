# cd D:\\Cardo\\uc\\sem 2\\MYOB
import csv
import time
import pprint
import json
import random 

cocktailNames = []
ingredientNames = {}
ingredientList = []
headersList = []
columnLenght = 0
neededColumnIndex = []
rowCols = []



def getHeaderList():
	with open("D:/Cardo/uc/sem 2/MYOB/all_drinks.csv",'r') as csvFile:
		f = csv.reader(csvFile)
		for row in f:
			print(row)
			for col in row:
				headersList.append(col)  
			break
# getHeaderList()

def noOfColumns():
	with open("D:/Cardo/uc/sem 2/MYOB/all_drinks.csv",'r') as csvFile:
		f = csv.reader(csvFile)
		for row in f:
			columnLenght = len(row)
			print(columnLenght)
			break
# noOfColumns()

def checkAllRowsHaveData():
	with open("D:/Cardo/uc/sem 2/MYOB/all_drinks.csv",'r') as csvFile:
		f = csv.reader(csvFile)
		print("start")
		for rowNum , row in enumerate(f):
			if(len(row) != 41):
				print(rowNum)
		print("end")
# checkAllRowsHaveData()

def checkForNull():
	with open("D:/Cardo/uc/sem 2/MYOB/all_drinks.csv",'r') as csvFile:
		f = csv.reader(csvFile)
		print("start")
		for rowNum , row in enumerate(f):
			for col in row:
				if col is None:
					print(rowNum)
		print("end")
# checkForNull()

def setColsIndex():
	for i in range(0,42):
		if i == 1:
			neededColumnIndex.append(i)
		elif i in range(3,6):
			neededColumnIndex.append(i)
		elif i in range(9,24):
			neededColumnIndex.append(i)
		elif i in range(25,40):
			neededColumnIndex.append(i)
		else:
			continue
# setColsIndex()
# print(neededColumnIndex)

def pickCols():
	with open("D:/Cardo/uc/sem 2/MYOB/all_drinks.csv",'r') as csvFile:
		f = csv.reader(csvFile)
		print("start")
		for row in f:
			print(type(row))
			print(len(neededColumnIndex))
			for i in neededColumnIndex:
				print(row[i])
			break				
		print("end")
# pickCols()

def fileList():
	with open("D:/Cardo/uc/sem 2/MYOB/all_drinks.csv",'r') as csvFile:
		f = csv.reader(csvFile)
		with open("D:/Cardo/uc/sem 2/MYOB/outputFile.csv","w",newline='') as outputFile:
			w2 = csv.writer(outputFile)
			print("start")
			for row in f:
				rowCols = []
				for i in neededColumnIndex:
					# print(row[i])
					rowCols.append(row[i].lower().strip())
				w2.writerow(rowCols)
		print("end")
# fileList()


# gets a list of all the recipes
# Creates a dictionary with ingridients as keys and cocktail names and volume used as values
def ingredientListFunction():
	print("****")
	ctr = 0
	with open("D:/Cardo/uc/sem 2/MYOB/outputFile.csv",'r') as csvFile:
		r1 = csv.reader(csvFile)
		for rowNum , row in enumerate(r1):
			if rowNum < 1:
				continue
			else:
				for i in range(4,19):
					if ((row[i] not in ingredientList) and (row[i].strip() is not "")) :
						ingredientList.append(row[i])
						ingredientNames[row[i]] = []
						ingredientNames[row[i]].append([row[0],row[i+15]])
					elif ((row[i] in ingredientList) and (row[i].strip() is not "")) :
						ingredientNames[row[i]].append([row[0],row[i+15]])
					else:
						continue
					# print(ingredientNames)
					# time.sleep(1)
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(ingredientList)
		print("****")
		pp.pprint(ingredientNames)
	text = open("D:/Cardo/uc/sem 2/MYOB/ingredientList.csv","w")
	text.write(json.dumps(ingredientList))			
	text = open("D:/Cardo/uc/sem 2/MYOB/ingredientNames.csv","w")
	text.write(json.dumps(ingredientNames))			

			
# ingredientListFunction()

# Gets a dictionary with cocktail name as key and ingridients and volume as values.
def recipeList():
	with open("D:/Cardo/uc/sem 2/MYOB/outputFile.csv",'r') as csvFile:
		r2 = csv.reader(csvFile)
		emptyList = []
		emptyDict = {}
		for rowNum, row in enumerate(r2):
			if rowNum < 1:
				continue
			else:
				emptyDict[row[0]] = []
				for i in range(4,19):
					if(row[i] is not "" and row[i+15] is not ""):
						emptyDict[row[0]].append([row[i],row[i+15]])
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(emptyDict)
		text = open("D:/Cardo/uc/sem 2/MYOB/recipeList.csv","w")
		text.write(json.dumps(emptyDict))

# recipeList()

# tempList = []

# def rectifyVolumes():
# 	with open("D:/Cardo/uc/sem 2/MYOB/outputFile.csv",'r') as csvFile:
# 		r1 = csv.reader(csvFile)
# 		for rownum, row in enumerate(r1):
# 			for j in range(19,34):
# 				if (row[j] not in tempList) and (row[j] is not ""):
# 					tempList.append(row[j])
# 	print(tempList)
# 	print(len(tempList))
# 	text = open("D:/Cardo/uc/sem 2/MYOB/volumeList.csv","w")
# 	for a in tempList:
# 		text.write(a+"\n")			

# rectifyVolumes() 

def selectFinalData():
	d = {}
	d1 = []
	with open("D:/Cardo/uc/sem 2/MYOB/tempDataset.csv") as csvFile:
		f = csv.reader(csvFile)
		for rownum,row in enumerate(f):
			if rownum<1:
				continue
			else:
				d1.append(row[0])
				# d[row[0]] = ""
	l = []
	j = 0
	for values in d1:
		if j%3 == 0:
			l.append(values)
		j = j + 1
		
	print(len(l))
	finalFile = []
	with open("D:/Cardo/uc/sem 2/MYOB/tempDataset.csv") as csvFile:
		f = csv.reader(csvFile)
		for rownum,row in enumerate(f):
			if rownum<1:
				finalFile.append(row)
			else:
				if row[0] in l:
					finalFile.append(row)
	with open("D:/Cardo/uc/sem 2/MYOB/finalDataSet.csv","w",newline='') as csvFile:
		w = csv.writer(csvFile,delimiter = ",")
		for b in finalFile:
			w.writerow(b)	
	
selectFinalData()

def sortFinalDataSet():
	with open("D:/Cardo/uc/sem 2/MYOB/finalDataSet.csv","r") as csvFile:
		r = csv.reader(csvFile,delimiter = "\t")
		with open("D:/Cardo/uc/sem 2/MYOB/finalDataSet3.csv","w", newline = "") as csvFile1:
			w = csv.writer(csvFile1, delimiter = ",", quoting = csv.QUOTE_ALL)
			for row in r:
				print(type(row))
				w.writerow(row)
			
# sortFinalDataSet()
