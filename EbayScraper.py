import urllib3
from bs4 import BeautifulSoup as soup
import requests


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

productNames.append("nissan+350z")
productNames.append("bmw+z4")
productNames.append("porche+boxter")
productNames.append("lotus+elise")
productNames.append("subaru+impreza")
productNames.append("bmw+m3")
productNames.append("bmw+m5")
productNames.append("focus+rs")
productNames.append("audi+s3")
productNames.append("range+rover")

for product in range(len(productNames)):
    urls.append("https://www.ebay.co.uk/sch/i.html?LH_Complete=1&LH_Sold=0&_from=R40&_sacat=0&_nkw="+ productNames[product] +"&_ipg=100&rt=nc")

completionPercentage = 0

for url in range(len(urls)):
    listings = []

    request = requests.get(urls[url])

    htmlString = str(soup(request.content, 'html5lib'))
    #htmlString = str(request.content)


    increment = 0
    titles = 0

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
    
    listingAvg = listing(productNames[url],str(totalPrice / 100))
    listingsAvg.append(listingAvg)

    completionPercentage += (100 / len(urls))
    print(completionPercentage) 

for i in range(len(listingsAvg)):
    print("Average price of a " + listingsAvg[i].name + " on ebay = £" + listingsAvg[i].price)

print("")
print("program finished")










    

