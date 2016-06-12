import requests
import urllib
import json
from datetime import datetime,timedelta
apikey="6bfa149e-00aa-4870-ad89-bb87403a43dc"

replies=['Hey there', 'Would you like to go somewhere?', 'Please enter your budget (in USD)', 'Please provide your location (City,Country)', 'Specify the group size', 'Mention your date of departure', 'Duration of vacation (in days)', 'Here\'s what we have planned for you:']

def filter_text(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])

class TravelInfo:
	def __init__(self):
		self.location = ""
		self.group_size = -1
		self.days = -1
		self.departure = ""
		self.places = []
		self.budget = -1
		self.context_level = -1

	def process(self):
		if self.location == "" or self.group_size == -1 or self.days == -1 or self.departure == "" or self.places == [] or self.budget == -1:
			return "Invalid Process"
		#return Answer

	def getConcept(self,message):
		r = requests.get('https://api.havenondemand.com/1/api/sync/extractconcepts/v1?text='+urllib.quote(message)+'&apikey='+apikey);
		r = json.loads(r._content)
		l = []
		for k in r["concepts"]:
			l.append(k["concept"])
		return l

	def getSentiment(self,message):
		r = requests.get('https://api.havenondemand.com/1/api/sync/analyzesentiment/v1?text='+urllib.quote(message)+'&apikey='+apikey);
		r = json.loads(r._content)

	#def context(self):

	def extractDate(self,message):
		r = requests.get('https://api.havenondemand.com/1/api/sync/extractentities/v2?text='+urllib.quote(message)+'&entity_type=date_eng&show_alternatives=false&apikey=6bfa149e-00aa-4870-ad89-bb87403a43dc')
		r = json.loads(r._content)
		if len(r["entities"]) == 0:
			return "N/A"
		return r["entities"][0]["normalized_date"]

	def handle_context(self,message,i):
		if i == 0:
			return True
		elif i == 1:
			if message[0] == 'y' or message[0] == 'Y':
				return True
			else:
				return False
		elif i == 2:
			if message.isdigit():
				self.budget = int(message)
				return True
			else:
				return False
		elif i == 3:
			#print message.split(',')
			#if len(message.split(',')) == 2:
			self.location = filter_text(message)
			#else:
			return True
		elif i == 4:
			if message.isdigit():
				self.group_size = int(message)
				return True
			else:
				return False
		elif i == 5:
			k = self.extractDate(message)
			if k != 'N/A':
				self.departure = datetime.strptime(k,"%m/%d/%Y")
				self.departure = self.departure.strftime("%Y-%m-%d")
				return True
			else:
				return False
		elif i == 6:
			if message.isdigit():
				self.days = int(message)
				return True
			else:
				return False
		elif i == 7:
			return False
		 
	def context(self,message):
		global replies
		k = True
		if self.context_level > -1:
			k = self.handle_context(message,self.context_level)
		if not k:
			self.context_level = 8
			return "Error! Please start again."
		self.context_level += 1
		if self.context_level == 7:
			pam = {'home':self.location, 'depart':self.departure,'arrive':(datetime.strptime(self.departure,"%Y-%m-%d") + timedelta(days=self.days)).strftime('%Y-%m-%d'),'npeople':self.group_size,'budget':self.budget}
			r = requests.get('http://localhost:5000/getPredictions',params = pam)
			print r.text
			ar = r.json()["results"]
			if ar:
				for a in ar:
					str1 = "Results:"+"\n"
					str1 = str1 + "Name : " + str(a["name"]) + "\n"
					str1 = str1 + "Cost : $" + str(a["cost"]) + "\n"
					str1 = str1 + "Savings : $" + str(a["savings"]) + "\n"
					str1 = str1 + "Click for more details : " + str(a["url"])
					return str1
			else:
				return "Sorry, no packages found in this budget. Try increasing it."
		else:
			return replies[self.context_level]

	#def context_group_size(self,message):
	#def context_group_size(self,message):
	#def context_days(self,message):
	#def context_departures(self,message):
	#def context_places(self,message):
	#def context_budget(self,message):