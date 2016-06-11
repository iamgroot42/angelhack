import telepot,time
from geopy.geocoders import Nominatim

haven_api='2cafa3c4-ef63-463b-bec9-3726c6819e5b'
token='208217948:AAHgpZQ6pQPpl6bSs7IImMqupIi5ZyWwyoU'

bot=telepot.Bot(token)

res=bot.getUpdates()
geolocator = Nominatim()

replies=['Hey there, ', 'Would you like to go somewhere?', 'Please choose your budget:', 'Please provide your location:', 'Specify the group size:', 'Mention your date of departure:', 'Duration of vacation(in number of days):', 'Here\'s what we have planned for you:']
show_keyboard={'keyboard':[['Yes', 'No', 'Maybe']]}
hide_keyboard={'hide_keyboard': True}
budget={'keyboard':[['$0 - $299', '$300 - $599'], ['$600 - $899','$900 - $1199', '$1200+']]}
i=0
n=len(replies)
flag=True
arr=[0,25,50,75,100]
bool_arr=[0,0,0,0,0]
location=''
groupSize=0
numDays=0

def handle(msg):
	global i,flag
	content_type, chat_type, chat_id=telepot.glance(msg)
	if(i==0):
		bot.sendMessage(chat_id, replies[i]+msg['from']['first_name']+'!')
		bot.sendMessage(chat_id, replies[i+1], reply_markup=show_keyboard)
		i+=1
	elif(i==2):
		if(msg['text']!='No'):
			bot.sendMessage(chat_id, replies[i], reply_markup=budget)
		else:
			flag=False
			bot.sendMessage(chat_id, 'Sorry to hear that :/', reply_markup=hide_keyboard)
	elif(i==3 and flag):
		s=str(msg['text'])
		if '299' in s:
			bool_arr[0]=1;
		elif '599' in s:
			bool_arr[1]=1;
		elif '899' in s:
			bool_arr[2]=1;
		elif '1199' in s:
			bool_arr[3]=1;
		else:
			bool_arr[4]=1;
		bot.sendMessage(chat_id, replies[i], reply_markup=hide_keyboard)
	elif(i==4 and flag):
		latitude=str(msg['venue']['location']['latitude'])
		longitude=str(msg['venue']['location']['longitude'])
		location = geolocator.reverse(latitude+" , "+longitude, timeout=None)
		print location
		bot.sendMessage(chat_id, replies[i])
	elif(i==5 and flag):
		s=str(msg['text'])
		l=s.split('![0-9]')
		groupSize=int(l[0])
		i+=1
		bot.sendMessage(chat_id, replies[i])
	elif(i==7 and flag):
		numDays=int(msg['text'])
		print numDays
		bot.sendMessage(chat_id, replies[i])
	i+=1

bot.message_loop(handle)
while 1:
	time.sleep(10)