import statistics
pl = [1.99, 1.99, 2.99, 2.99, 2.99, 2.99, 10]
# print(pl[0:0])
ap = []
for index,value in enumerate(pl):
	# print(pl[0:index+1])
	temp = pl[0:index+1]
	ap.append(statistics.mean(temp))
	
print(ap)