import json
import requests
from pprint import pprint
def find_city_id():
	names=[]
	flag =0
	with open('city.list.json') as f:
	    for line in f:
			#json_data=line
			jdata = json.loads(line)
			location = 'delhi'
			location=location.lower()
			#print location
			jdata['name'] = jdata['name'].lower()
			# print jdata['name']

			if location == jdata['name']:
				city_id = jdata['_id']
				flag = 1
				#print city_id
				return city_id
				#print jdata['name']
				#break

			if location in jdata['name']:
				#print jdata['name']
				name = (jdata['name'])
				city_id = jdata['_id']
				#print city_id

	if flag != 1:
		return jdata['_id']
			#json_data.close()

cityid = find_city_id()

print cityid
def predict():
	response= requests.get("http://api.openweathermap.org/data/2.5/forecast/daily?id="+str(cityid)+"&cnt=3&APPID=59847d23a3f26701b9626e666bc22ecb")
	#print response.json()
	#print response.json()

predict()