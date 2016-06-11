from flask import Flask
from flask import request

app = Flask(__name__, static_folder='image_files', static_url_path='')

users = []

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


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
