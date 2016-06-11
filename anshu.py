import json
import requests
import time
from requests.packages import urllib3
urllib3.disable_warnings()

TOKEN = "EAACEdEose0cBABuDjEPf5XUOfT1qwBzQja17IKJN4bEENcCjP8f6T11xiRFihASBewDZA0rzP8YGS7EaTl1hE2U9ZA7d4ZCovqIHMTkjyGgs04i3zcJuyu1iDm0E0gGoI8ZAvcHIPrSMK7OZADy6S4L4rEys41oLFGeeglcyB6gZDZD"
LIMIT = 1000

fb_id = "me"
url = 'https://graph.facebook.com/v2.5/' + fb_id + '/posts?fields=place&limit=' + str(LIMIT) + '&access_token=' + TOKEN
resp = json.loads(requests.get(url).text) 
count = 0


while resp is not None and count < 50000:
	if 'error' in resp:
		if resp['error']['code'] == 100:
			break

	if 'data' not in resp:
		if 'error' in resp:
			if resp['error']['code'] == 12:
				break
		time.sleep(180)
		resp = json.loads(requests.get(url).text)
		continue

	if len(resp['data']) == 0:
		break

	print len(resp['data'])

	for i in resp['data']:
		try:
			city = i['place']['location']['city']
			country = i['place']['location']['country']
			print city,country
			count += 1
		except:
			continue

	if 'paging' in resp:
		if 'next' in resp['paging']:
			url = resp['paging']['next']
			resp = json.loads(requests.get(url).text)
		else:
			resp = None
	else:
		resp = None	
