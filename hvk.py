import requests,json
token='208894872:AAF02gKdVh0ncwhkDvGwy8yRkIu1D36fn8g'
haven_api='2cafa3c4-ef63-463b-bec9-3726c6819e5b'

res=requests.get('https://api.telegram.org/bot'+token+'/getUpdates')
data=json.loads(res.text)
print data
text=[]
for x in data['result']:
	y=x['message']
	if 'text' in y:
		text.append(x['message']['text'])
	else:
		print 'potato'	
print text