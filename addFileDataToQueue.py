import hashlib 
import json
import csv

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    print(hash_md5.hexdigest())

# md5("D:/Cardo/uc/sem 2/MYOB/inputFiles/invoices/1.txt")

def readFileAsJson(fn):
    with open(fn,"r") as f:
    	data = csv.reader(f)
    	s = " "
    	for line in data:
    		for word in line:
    			temp = str(word)
    			s = s + temp
    		s = s + ","
    	print(s)
    	# newdata = json.loads(s)
    	# print(newdata)

# readFileAsJson("D:/Cardo/uc/sem 2/MYOB/inputFiles/invoices/1.txt")



