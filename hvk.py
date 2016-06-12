import telepot,time
from geopy.geocoders import Nominatim
import requests
from datetime import datetime, timedelta



haven_api='2cafa3c4-ef63-463b-bec9-3726c6819e5b'
token='208217948:AAHgpZQ6pQPpl6bSs7IImMqupIi5ZyWwyoU'

bot=telepot.Bot(token)

res=bot.getUpdates()
geolocator = Nominatim()

replies=['Hey there, ', 'Would you like to go somewhere?', 'Please choose your budget:', 'Please provide your location:', 'Specify the group size:', 'Mention your date of departure(YYYY-MM-DD):', 'Duration of vacation(in number of days):', 'Here\'s what we have planned for you:']
show_keyboard={'keyboard':[['Yes', 'No', 'Maybe']]}
hide_keyboard={'hide_keyboard': True}
budget=0
i=1
n=len(replies)
flag=True
flag1=False
location=''
groupSize=0
numDays=0
departureDate=''
city=''
country=''

def handle(msg):
	global i,flag,flag1,location,numDays,groupSize,departureDate,budget,city,country
	content_type, chat_type, chat_id=telepot.glance(msg)
	if(i==1):
		bot.sendMessage(chat_id, replies[i - 1]+msg['from']['first_name']+'!')
		bot.sendMessage(chat_id, replies[i], reply_markup=show_keyboard)
		i+=1
	elif(i==2):
		if flag1:
			bot.sendMessage(chat_id, replies[i])
			i = 7
		elif(msg['text']!='No'):
			bot.sendMessage(chat_id, replies[i], reply_markup=hide_keyboard)
			i += 1
		else:
			flag=False
			bot.sendMessage(chat_id, 'Sorry to hear that :/', reply_markup=hide_keyboard)
			i = 8
	elif(i==3 and flag):
		budget=float(msg['text'])
		bot.sendMessage(chat_id, replies[i], reply_markup=hide_keyboard)
		i += 1
	elif(i==4 and flag):
		latitude=str(msg['venue']['location']['latitude'])
		longitude=str(msg['venue']['location']['longitude'])
		location = geolocator.reverse(latitude+" , "+longitude, timeout=None)
		print type(location)
		l=str(location).split(', ')
		city=l[-3]
		country=l[-1]
		print city, country
		bot.sendMessage(chat_id, replies[i])
		i += 1
	elif(i==5 and flag):
		s=str(msg['text'])
		l=s.split('![0-9]')
		groupSize=int(l[0])
		bot.sendMessage(chat_id, replies[i])
		i += 1
	elif(i==6 and flag):
		departureDate=msg['text']
		print departureDate
		bot.sendMessage(chat_id, replies[i])
		i += 1
	elif(i==7 and flag):
		if not flag1:
			numDays=int(msg['text'])
			print numDays
		else:
			budget=float(msg['text'])
		flag1 = True
		arrive = datetime.strptime(departureDate, '%Y-%m-%d')
		arrive = arrive + timedelta(days = numDays)
		arrive = str(arrive.strftime("%Y-%m-%d"))
		pam = {'home':city + ", " + country, 'depart':departureDate,'arrive':arrive,'npeople':groupSize,'budget':budget}
		r = requests.get('http://0.0.0.0:5000/getPredictions',params = pam)
		print r.text
		ar = r.json()["results"]
		if ar:
			bot.sendMessage(chat_id, replies[i])
			for a in ar:
				str1 = ""
				str1 = str1 + "Name : " + str(a["name"]) + "\n"
				str1 = str1 + "Cost : $" + str(a["cost"]) + "\n"
				str1 = str1 + "Savings : $" + str(a["savings"]) + "\n"
				str1 = str1 + "Click for more details : " + str(a["url"])
				bot.sendMessage(chat_id, str1)
			i = 9
		else:
			i = 2
			bot.sendMessage(chat_id, "Sorry, no packages found in this budget. Try increasing it.")
	elif i == 8:
		i = 1
		flag1 = False
		flag = True
	elif i == 9:
		bot.sendMessage(chat_id, "Enjoy your travel. Please use me again.")
		i = 1
		flag = True
		flag1 = False
bot.message_loop(handle)
while 1:
	time.sleep(10)