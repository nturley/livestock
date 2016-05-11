
# https://www.ams.usda.gov/mnreports/nw_ls795.txt
import pprint
import requests
pp = pprint.PrettyPrinter(indent=2)

# make a class for sale categories with a tostring method
class Sale:
    def __init__(self,
                 saletype,
                 number,
                 weight_range,
                 weight_average,
                 price_range,
                 price_average):
        self.saletype = saletype
        self.number = number
        self.weight_range = weight_range
        self.weight_average = weight_average
        self.price_range = price_range
        self.price_average = price_average

    def __str__(self):
        return 'CLASS: ' + self.saletype.ljust(35) + \
             '  HD: ' + self.number.rjust(3) + \
             '  WEIGHT: ' + self.weight_average.rjust(10) + \
             '  PRICE: ' + self.price_average.rjust(7)

headerstart = 'Head'
endtable = 'Source:'

res = requests.get('https://www.ams.usda.gov/mnreports/nw_ls795.txt')
res.raise_for_status()
lines = res.text.splitlines()
allrows = []
for line in lines:
	 allrows.append([s.strip() for s in line.split('  ') if len(s.strip())>0])

IGNORE = 0
CONSUME = 1

state = IGNORE
currentType = None

sales = []
for i, row in enumerate(allrows):
	if state is IGNORE and len(row) > 3 and row[0] == headerstart:
		currentType = allrows[i - 1][0]
		state = CONSUME
	elif len(row)>0 and row[0].startswith(endtable):
		break
	elif state is CONSUME and len(row) is 0:
		state = IGNORE
	elif state is CONSUME:
		sale = Sale(saletype=currentType,
			        number=row[0],
			        weight_range=row[1],
			        weight_average=row[2],
			        price_range=row[3],
			        price_average=row[4])
		sales.append(sale)

for sale in sales:
	print str(sale)

