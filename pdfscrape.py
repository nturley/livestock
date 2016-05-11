from PyPDF2 import PdfFileReader as reader
import pprint
import requests

pp = pprint.PrettyPrinter(indent=2)

# download pdf
res = requests.get('http://stocklandlivestock.com/wp-content/uploads/2015/02/05.02.16.pdf')
res.raise_for_status()
f = open('current.pdf', 'wb')
for chunk in res.iter_content(100000):
    f.write(chunk)
f.close()

# make a class for sale categories with a tostring method
class SaleCategory:
    def __init__(self,
                 saletype,
                 number,
                 weight,
                 price_range,
                 price_average,
                 price_unit):
        self.saletype = saletype
        self.number = number
        self.weight = weight
        self.price_range = price_range
        self.price_average = price_average
        self.price_unit = price_unit

    def __str__(self):
        return 'CLASS: ' + self.saletype.ljust(14) + \
             '  HD: ' + self.number.rjust(3) + \
             '  WEIGHT: ' + self.weight.rjust(10) + \
             '  PRICE: ' + self.price_average.rjust(7) + \
             '  PF: ' + self.price_unit.rjust(3)

# each sale has a class
classtypes = ['BABY CALF',
              'BULL CALF',
              'COW/CALF PAIR',
              'BRED COW',
              'BULL',
              'COW',
              'HEIFER',
              'STEER']
# each sale is listed per head or by weight
pftypes = ['HD','WT']

# store our table of data here
currentRow = []
allRows = []

# possible states
IGNORE = 0
FIRST_COL = 1
DEFAULT = 2

# state variable, start out ignoring cells
state = IGNORE

# extract all of the text from the pdf, store in s
f = open('current.pdf','rb')
r = reader(f)
p = r.getPage(0)
s = p.extractText()
f.close()

#parse through each of the cells
for cell in s.split('\n'):
    cell = cell.strip().upper()
    # ignore until we see a class type
    if (state is IGNORE and cell in classtypes):
        state = DEFAULT
        currentRow.append(cell)
    # consume cells
    elif (state is DEFAULT and not cell in pftypes):
        currentRow.append(cell)
    # consume cells until the pftype and then go to FIRST_COL
    elif (state is DEFAULT and cell in pftypes):
        currentRow.append(cell)
        allRows.append(SaleCategory(currentRow[0],
                                    currentRow[1],
                                    currentRow[2],
                                    currentRow[3],
                                    currentRow[4],
                                    currentRow[5]))
        currentRow = []
        state = FIRST_COL
    # throw away all cells on total rows
    elif (state is FIRST_COL and 'TOTAL' in cell):
        state = IGNORE
    # start a new row with a new class type
    elif (state is FIRST_COL and cell in classtypes):
        currentRow.append(cell)
        state = DEFAULT
    # start a new row with the same class type
    elif (state is FIRST_COL):
        currentRow.append(allRows[-1].saletype)
        currentRow.append(cell)
        state = DEFAULT
for row in allRows:
    print str(row)