from flask import Flask
from flask import jsonify
from flask import request
import threading
import grequests
from bs4 import BeautifulSoup
import xml
import json
from urllib2 import *
import requests
from pymongo import MongoClient

app = Flask(__name__, static_url_path='')

users = []
recc = {}
XPTOKEN = 'IZSqdTKn6HAw070SvuOZblBtPYetEEzf'
IBM_USER = '08c030a8-9afd-4ce5-8241-564b39bb5f8c'
IBM_PASS = 'xvUcgeDDyACP'


@app.route("/")
def welcome():
	return "potato"


@app.route("/getCurrentUsers")
def getCurrentUsers():
	global users
	return str(len(users))


@app.route("/checkUsername")
def checkUsername():
	global users
	username = request.args.get('username')
	if username not in users:
		users.append(username)
		return "True"
	return "False"


@app.route("/removeUsername")
def removeUsername():
	global users
	username = request.args.get('username')
	if username in users:
		users.remove(username)
		return "True"
	return "False"


@app.route("/sendMessage")
def sendMessage():
	global users
	username = request.args.get('username')
	message = request.args.get('message')
	if username in users:
		return "Potato is the new tomato :)"
	return "False"


def print_url(r, **kwargs):
    return


def async(url_list):
    sites = []
    for u in url_list:
        rs = grequests.get(u, hooks=dict(response=print_url))
        sites.append(rs)
    return grequests.map(sites)


def stripHtmlTags(htmlTxt):
	return ''.join(BeautifulSoup(htmlTxt,"lxml").findAll(text=True)) 


def get_popular_places():
	continents = ['Asia','Europe','Africa','North America','South America','Australia']
	client = MongoClient()
	# continents = ['Asia']
	db = client['angelhack']
	table = db['places']
	tbp = table.find()
	if tbp.count() > 0:
		for y in tbp:
			recc[y['name']] = y['value']
	else:
		urls = []
		for x in continents:
			urls.append("http://terminal2.expedia.com:80/x/suggestions/flights?query="+x+"&maxresults=2&apikey="+XPTOKEN)
		l =  async(urls)
		for i in l:
			x = i.json()['sr'] 
			for j in x:
				name = stripHtmlTags(j['d']) 
				lat = j['ll']['lat']
				lng = j['ll']['lng']
				recc[name] = places_of_interest(lat,lng)
				table.insert_one({'name':name,'value':recc[name]})
				# print name, recc[name]
	return True


def places_of_interest(latitude, longitude):
	print "chu"
	url = "http://terminal2.expedia.com/x/geo/features?within=15km&lng="\
		+ str(longitude) + "&lat=" + str(latitude)\
		+ "&type=point_of_interest&verbose=3&lcid=1033&apikey=" + XPTOKEN
	print url
	req = Request(url = url)
	data = urlopen(req)
	ex = json.loads(data.read())
	j = 0
	for i in ex:
		pop = i['tags']['score']['popularity']['value']
		if pop >= 0.5:
			j += 1
	return j


def predictions(fromo,start,end,npeople,budget):
	suggest = {}
	print len(recc.keys())
	for i in recc.keys():
		# Duration, Cost, Saving, Places, Hotel Rating
		to = i
		deal = get_deals(fromo, to, start, end, npeople, budget)
		
		if not deal:
			continue
		#Places
		n_places = recc[i]

		#Cost
		cost = float(deal['package']["PackagePrice"]["TotalPrice"]["Value"])

		#Savings
		savings = float(deal['package']["PackagePrice"]["TotalSavings"]["Value"])
		
		#Duration
		from_dur = deal['flight']['FlightItinerary']['FlightLeg'][0]['FlightDuration'][2:]
		hours = int(from_dur.split('H')[0])
		minutes = int(from_dur.split('H')[1][:-1])
		from_dur = 60 * hours + minutes

		to_dur = deal['flight']['FlightItinerary']['FlightLeg'][1]['FlightDuration'][2:]
		hours = int(to_dur.split('H')[0])
		minutes = int(to_dur.split('H')[1][:-1])
		to_dur = 60 * hours + minutes

		duration = max(from_dur, to_dur)

		#Hotel Rating
		hotel_rating = float(deal['hotel']['StarRating'])

		res_dict = {}
		res_dict["places"] = n_places
		res_dict["cost"] = cost
		res_dict["savings"] = savings
		res_dict["duration"] = duration
		res_dict["rating"] = hotel_rating
		res_dict["deal"] = deal
		res_dict["name"] = i

		suggest[i] = res_dict

	# print suggest
	#send suggest to trade-off analytics
	count = 1
	options = []
	mapping = {}
	for x in suggest.keys():
		dat = {}
		mapping[count] = suggest[x]
		potato = suggest[x].copy()
		del potato['deal']
		del potato['name']
		dat['values'] = potato
		dat['description_html'] = "potato"
		dat['app_data'] = {}
		dat['key'] = count
		dat['name'] = x
		options.append(dat)
		print mapping[count].keys()
		count += 1	
	mane = {}
	mane['subject'] = 'exPedia'
	mane['options'] = options
	mane['columns'] = json.loads('[{"key":"places","full_name":"Places","type":"numeric","is_objective":true,"goal":"max"},{"key":"cost","full_name":"Cost","type":"numeric","is_objective":true,"goal":"min"},{"key":"savings","full_name":"Savings","type":"numeric","is_objective":true,"goal":"max"},{"key":"duration","full_name":"Duration","type":"numeric","is_objective":true,"goal":"min"},{"key":"rating","full_name":"Rating","type":"numeric","is_objective":true,"goal":"max"}]')
	# print mane

	headers = {'content-type': 'application/json'}
	url = 'https://gateway.watsonplatform.net/tradeoff-analytics/api/v1/dilemmas?generate_visualization=false'
	faile = json.dumps(mane)
	z = []
	try:
		r = requests.post(url, auth=(IBM_USER, IBM_PASS), headers = headers, data = faile)
		z =  r.json()['resolution']['solutions']
	except:
		pass
	to_hvk = []
	for y in z:
		eye = y['solution_ref']
		zeta = mapping[int(eye)]
		# print zeta.keys()
		weed = {}
		weed['name'] = zeta['name']
		weed['cost'] = zeta['cost']
		weed['savings'] = zeta['savings']
		weed['url'] = zeta['deal']['package']['DetailsUrl']
		to_hvk.append(weed)
	return to_hvk


def get_deals(fromo,to,start,end,npeople, budget):
	try:
		from_val = '%20'.join(str(x) for x in fromo.split())
		url = "http://terminal2.expedia.com/x/suggestions/regions?query=" \
			+  from_val + "&apikey=" + XPTOKEN
		req = Request(url = url)
		data = urlopen(req)
		ex = json.loads(data.read())
		regionId = ex["sr"][0]["id"]
		airportId = ex["sr"][0]["a"]
		print "Done1"

		to_val = '%20'.join(str(x) for x in to.split())
		url = "http://terminal2.expedia.com/x/suggestions/regions?query=" \
			+  to_val + "&apikey=" + XPTOKEN
		req = Request(url = url)
		data = urlopen(req)
		ex = json.loads(data.read())
		airport2Id = ex["sr"][0]["a"]
		print "Done2"

		url = "http://terminal2.expedia.com/x/mhotels/search?regionId=" \
			+ str(regionId) + "&checkInDate=" + str(start) + "&checkOutDate=" \
			+ str(end) + "&room1=2&apikey=" + XPTOKEN
		req = Request(url=url)
		data = urlopen(req)
		ex = json.loads(data.read())
		# print ex
		print "Done3"

		hotels = ex["hotelList"]
		hotelIds = []
		for hotel in hotels:
			if float(hotel["hotelStarRating"]) >= 3.0:
				hotelIds.append(hotel["hotelId"])

		url = "http://terminal2.expedia.com/x/packages?departureDate=" \
			+ start + "&originAirport=" + airportId \
			+ "&destinationAirport=" + airport2Id + "&returnDate=" \
			+ end + "&hotelids=" + ','.join(str(x) for x in hotelIds) \
			+ "&adults=" + npeople + "&limit=20&nonstop=true&apikey=" + XPTOKEN
		# print url

		req = Request(url=url)
		data = urlopen(req)
		ex = json.loads(data.read())
		# print ex
		print "Done4"

		try:
			deals = ex["PackageSearchResultList"]["PackageSearchResult"]
		except:
			return None

		hotels = ex["HotelList"]["Hotel"]
		flights = ex["FlightList"]["Flight"]
		for hotelR in range(5, 2, -1):
			for deal in deals:
				price = deal["PackagePrice"]["TotalPrice"]["Value"]
				if float(price) <= float(budget):
					res_deal = None
					for hotel in hotels:
						hotelid = deal["HotelReferenceIndex"]
						if hotel["HotelIndex"] == hotelid and float(hotel["StarRating"]) >= float(hotelR):
							res_deal = {}
							res_deal['package'] = deal
							flightid = deal["FlightReferenceIndex"]
							if flights["FlightIndex"] == flightid:
								res_deal["flight"] = flights
							res_deal["hotel"] = hotel
							break
					if not res_deal:
						continue
					else:
						return res_deal
		return None
	except:
		return None


@app.route("/getPredictions")
def getPredictions():
	home = request.args.get('home')
	depart = request.args.get('depart')
	arrive = request.args.get('arrive')
	npeople = request.args.get('npeople')
	budget = request.args.get('budget')
	print home
	print depart
	print arrive
	print npeople
	print budget
	ret_obj = predictions(home,depart,arrive,npeople,budget)
	print ret_obj
	return jsonify({"results":ret_obj})


@app.after_request
def apply_caching(response):
	response.headers["Access-Control-Allow-Origin"] = "*"
	return response


if __name__ == "__main__":
	get_popular_places()
	app.run(debug=True,host="0.0.0.0", threaded=True)
