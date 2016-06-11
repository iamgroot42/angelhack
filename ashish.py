from urllib2 import *
import json
from pprint import *
from datetime import *
from flask import Flask

expedia_key = "IZSqdTKn6HAw070SvuOZblBtPYetEEzf"

#Step 1:
# Modify this to get user input through chat bot
city = raw_input()
url = "http://terminal2.expedia.com/x/suggestions/regions?query=" \
	+ city + "&apikey=" + expedia_key
req = Request(url=url)
data = urlopen(req)
regionId = json.loads(data.read())["sr"][0]["id"]
print regionId

#Step 2:
#Modify this to get user input through chat bot
starRatingWanted = 3.0
url = "http://terminal2.expedia.com/x/mhotels/search?regionId=" \
	+ str(regionId) + "&checkInDate=" + str(date.today()) + "&checkOutDate=" \
	+ str(date.today() + timedelta(days=1)) + "&room1=2&apikey=" + expedia_key
req = Request(url=url)
data = urlopen(req)
# print data.read()
hotels = json.loads(data.read())["hotelList"]
hotelIds = []
for hotel in hotels:
	if float(hotel["hotelStarRating"]) >= starRatingWanted:
		hotelIds.append(hotel["hotelId"])
print hotelIds

#Step 3:
#Modify this to get user input through chat bot
departureDate = raw_input()
originAirport = raw_input()
destinationAirport = raw_input()
returnDate = raw_input()
adults = raw_input()
url = "http://terminal2.expedia.com/x/packages?departureDate=" \
	+ departureDate + "&originAirport=" + originAirport \
	+ "&destinationAirport=" + destinationAirport + "&returnDate=" \
	+ returnDate + "&hotelids=" + ','.join(str(x) for x in hotelIds) \
	+ "&adults=" + adults + "&limit=1&nonstop=true&apikey=" + expedia_key
# url = "http://terminal2.expedia.com/x/packages?departureDate=" \
# 	+ departureDate + "&originAirport=" + originAirport \
# 	+ "&destinationAirport=" + destinationAirport + "&returnDate=" \
# 	+ returnDate + "&regionid=" + regionId + "&adults=" \
# 	+ adults + "&limit=1&nonstop=true&apikey=" + expedia_key
print url
req = Request(url=url)
data = urlopen(req)
deals = json.loads(data.read())
print deals