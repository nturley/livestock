
# http://billingslivestock.com/Cow_Sales/Past_Sales/01_21_16_MARKET.html

import requests
import bs4

class Sale:
    def __init__(self,
                 classType,
                 number,
                 description,
                 average_weight,
                 price,
                 unit):
        self.classType = classType
        self.number = number
        self.description = description
        self.average_weight = average_weight
        self.price = price
        self.unit = unit
    def __str__(self):
        return 'CLASS: ' + self.classType.ljust(14) + \
             '  HD: ' + self.number.rjust(3) + \
             '  WEIGHT: ' + self.average_weight.rjust(6) + \
             '  PRICE: ' + self.price.rjust(10) + \
             '  PF: ' + self.unit.rjust(3)


res = requests.get('http://billingslivestock.com/Cow_Sales/Past_Sales/01_21_16_MARKET.html')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'lxml')
table2 = soup.select('table')[1]
allRows = []
for row in table2.select('tr'):
    cells = row.select('td')
    if (len(cells) is 1 or cells[1].getText().strip()==''):
        currentClass = cells[0].getText()
        continue

    number = cells[2].getText().strip()
    price = cells[5].getText().strip().split('/')
    allRows.append(Sale(classType=currentClass,
                        number=cells[2].getText().strip(),
                        description=cells[3].getText().strip(),
                        average_weight=cells[4].getText().strip(),
                        price=price[0],
                        unit=price[1]))

for sale in allRows:
    print str(sale)

