import telepot,time

haven_api='2cafa3c4-ef63-463b-bec9-3726c6819e5b'
token='208217948:AAHgpZQ6pQPpl6bSs7IImMqupIi5ZyWwyoU'

bot=telepot.Bot(token)

res=bot.getUpdates()

replies=['Hey there, ', 'Would you like to go somewhere?', 'Please choose your budget:', 'Please provide your location:', 'dsuifhfiusd']
show_keyboard={'keyboard':[['Yes', 'No', 'Maybe']]}
hide_keyboard={'hide_keyboard': True}
budget={'keyboard':[['Rs 0 - Rs 24999', 'Rs 25000 - Rs 49999'], ['Rs 50000 - Rs 74999','Rs 75000 - Rs 99999', 'Rs 100000+']]}
i=0
n=len(replies)
flag=True
arr=[0,25,50,75,100]
location=[]

def handle(msg):
	global i
	content_type, chat_type, chat_id=telepot.glance(msg)
	if(i==0):
		bot.sendMessage(chat_id, replies[i]+msg['from']['first_name']+'!')
	elif(i==1):
		bot.sendMessage(chat_id, replies[i], reply_markup=show_keyboard)
	elif(i==2):
		if(msg['text']!='No'):
			bot.sendMessage(chat_id, replies[i], reply_markup=budget)
		else:
			flag=False
			bot.sendMessage(chat_id, 'Sorry to hear that :/', reply_markup=hide_keyboard)
	elif(i==3):
		s=str(msg['text'])
		print s
		bot.sendMessage(chat_id, replies[i], reply_markup=hide_keyboard)
	elif(i==4):
		print msg
	i+=1
if flag==True:
	bot.message_loop(handle)
while 1:
	time.sleep(10)