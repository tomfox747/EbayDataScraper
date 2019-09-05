import urllib3
from bs4 import BeautifulSoup as soup
import requests
from xlrd import open_workbook
import xlsxwriter


class listing:
    def __init__(self, Name, Price):
        self.name = Name
        self.price = Price

def createSubstring(inputString, startPos, subStringLength):
    outputString = ""
    increment = 0
    while(increment < subStringLength):
        outputString += inputString[startPos + increment]
        increment += 1
    return outputString
def extractTitle(input):
    output = ""
    increment = len(input) - 2
    while(increment > 0):
        if input[increment] == ">":
            increment += 1
            while input[increment] != "<":
                output += input[increment]
                increment += 1
            break
        increment -= 1
    
    return output
def extractPrice(input):
    price = ""
    for i in range(0, len(input)):
        if input[i] == "£" or input[i] == "$":
            priceIncrementor = i + 1
            while input[priceIncrementor] != "<":
                price += input[priceIncrementor]
                priceIncrementor += 1
            return price
    return price
def priceStringToInt(inputString):
    outputString = inputString.replace(" ","")
    outputString = outputString.replace(",","")
    return outputString


urls = []
productNames = []
listingsAvg = []
completionPercentage = 0
book = open_workbook('ebayProducts.xlsx')
sheet = book.sheet_by_index(0)

for row in range(sheet.nrows):
    item = str(sheet.cell(row, 0).value)
    item = item.replace(" ","+")
    productNames.append(item)


for product in range(len(productNames)):
    urls.append("https://www.ebay.co.uk/sch/i.html?LH_Complete=1&LH_Sold=1&_from=R40&_sacat=0&_nkw="+ productNames[product] +"&_ipg=100&rt=nc")


for url in range(len(urls)):
    
    increment = 0
    titles = 0
    listings = []
    request = requests.get(urls[url])
    htmlString = str(soup(request.content, 'html5lib'))

    while increment < (len(htmlString) - 10):
        
        substring = createSubstring(htmlString, increment, 7)

        if substring == "lvtitle":
            startOfString = increment
            while(True):
                substring = createSubstring(htmlString, increment, 4)
                if substring == "</a>":
                    endOfString = increment + 4
                    extractionString = ""
                    for i in range(startOfString, endOfString):
                        extractionString += htmlString[i]
                    title = extractTitle(extractionString)
                    L = listing(title,"")
                    listings.append(L)
                    break
                increment += 1
        else: 
            substring = createSubstring(htmlString, increment, 11)
            if substring == "lvprice prc":
                startOfString = increment
                while(True):
                    substring = createSubstring(htmlString, increment, 7)
                    if substring == "</span>":
                        endOfString = increment + 7
                        extractionString = ""
                        for i in range(startOfString, endOfString):
                            extractionString += htmlString[i]
                        price = extractPrice(extractionString)
                        #productPricesList.append(price)
                        listings[len(listings) - 1].price = price
                        break
                    increment += 1
        increment+=1

    
    totalPrice = 0
    for i in range(len(listings)):
        priceFloat = float(priceStringToInt(listings[i].price))
        totalPrice += priceFloat
    
    listingAvg = listing(productNames[url],str(totalPrice / len(listings)))
    listingsAvg.append(listingAvg)

    completionPercentage += (100 / len(urls))
    print(str(completionPercentage) + "% Complete") 


print("")

for i in range(len(listingsAvg)):
    listingsAvg[i].name = listingsAvg[i].name.replace("+"," ")
    print("Average price of a " + listingsAvg[i].name + " on ebay = £" + listingsAvg[i].price)


#Write to spreadsheet
outputWorkbook = xlsxwriter.Workbook('ebayProducts.xlsx')
worksheet = outputWorkbook.add_worksheet()

worksheet.write(0,0, "Product name")
worksheet.write(0,1, "Average Price")

for i in range(0, len(listingsAvg)):
    worksheet.write(i + 1, 0, listingsAvg[i].name)
    worksheet.write(i + 1, 1, listingsAvg[i].price)


outputWorkbook.close()

print("")
print("program finished")










    

