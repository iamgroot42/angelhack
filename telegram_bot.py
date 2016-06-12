import telepot, time, requests, urllib
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime, timedelta

haven_api = '2cafa3c4-ef63-463b-bec9-3726c6819e5b'
token = '208217948:AAHgpZQ6pQPpl6bSs7IImMqupIi5ZyWwyoU'

bot = telepot.Bot(token)
geolocator = Nominatim()
replies = ['Hey there, ', 'Would you like to go somewhere?',\
	'Please choose your budget (in $):', 'Please provide your location:',\
	'Specify the group size:', 'Mention your date of departure(YYYY-MM-DD):',\
	'Duration of vacation(in number of days):', 'Here\'s what we have planned for you:']
show_keyboard = {'keyboard':[['Yes', 'No', 'Maybe']]}
hide_keyboard = {'hide_keyboard': True}


dict_states = {'interested' : 0, 'location' : 1, 'sz' : 2, 'depart' : 3, 'duration' : 4, 'budget' : 5}

start = True
step = -1
home = None
sz = -1
st_date = None
duration = -1
budget = -1
chat_id = None

def handle(msg):
	global start, step, home, sz, st_date, duration, budget, chat_id
	content_type, chat_type, chat_id = telepot.glance(msg)
	if start == True:
		start = False
		msg_str = replies[0] + msg['from']['first_name'] + '!'
		bot.sendMessage(chat_id, msg_str)
		bot.sendMessage(chat_id, replies[1], reply_markup=show_keyboard)
		step = 0
	elif step == dict_states['interested']:
		msg_str = str(msg['text'])
		if msg_str == 'No':
			start = True
			bot.sendMessage(chat_id, "Thank you for using Angel. Have a nice day :)", reply_markup=hide_keyboard)
		else:
			step = 1
			bot.sendMessage(chat_id, replies[3], reply_markup=hide_keyboard)
	elif step == dict_states['location']:
		if 'venue' in msg.keys():
			latitude = str(msg['venue']['location']['latitude'])
			longitude = str(msg['venue']['location']['longitude'])
		else:
			latitude = str(msg['location']['latitude'])
			longitude = str(msg['location']['longitude'])
		try:
			# print latitude,longitude
			location = geolocator.reverse(latitude + " , " + longitude, timeout = None)
		except GeocoderTimedOut as e:
			print("Error: geocode failed on input %s with message %s" % (latitude + " , " + longitude, e.msg))
		city = str(location).encode('utf-8').split(', ')[-3]
		country = str(location).encode('utf-8').split(', ')[-1]
		home = city + ', ' + country
		step = 2
		bot.sendMessage(chat_id, replies[4])
	elif step == dict_states['sz']:
		sz = int(str(msg['text']))
		step = 3
		bot.sendMessage(chat_id, replies[5])
	elif step == dict_states['depart']:
		st_date = str(msg['text'])
		step = 4
		bot.sendMessage(chat_id, replies[6])
	elif step == dict_states['duration']:
		duration = int(str(msg['text']))
		step = 5
		bot.sendMessage(chat_id, replies[2])
	elif step == dict_states['budget']:
		budget = float(str(msg['text']))
		arrive = datetime.strptime(st_date, '%Y-%m-%d')
		arrive = arrive + timedelta(days = duration)
		arrive = str(arrive.strftime("%Y-%m-%d"))
		home = urllib.unquote(home)
		pam = {'home' : home, 'depart' : st_date, 'arrive' : arrive, 'npeople' : sz, 'budget' : budget}
		r = requests.get('http://0.0.0.0:5000/getPredictions', params = pam)
		ar = r.json()["results"]
		if ar:
			bot.sendMessage(chat_id, replies[7])
			for a in ar:
				str1 = ""
				str1 = str1 + "Name : " + str(a["name"]) + "\n"
				str1 = str1 + "Cost : $" + str(a["cost"]) + "\n"
				str1 = str1 + "Savings : $" + str(a["savings"]) + "\n"
				str1 = "["+str1+"]("+a["url"]+")"
				bot.sendMessage(chat_id, str1, parse_mode = 'Markdown')
			start = True
			bot.sendMessage(chat_id, "Thanks for using Angel.")
		else:
			step = 5
			bot.sendMessage(chat_id, "No matches found. Please try to increase your budget.")
			bot.sendMessage(chat_id, replies[2])

bot.message_loop(handle, timeout = 20, run_forever = False)
while 1:
	time.sleep(10)