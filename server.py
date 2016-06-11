from flask import Flask

app = Flask(__name__, static_folder='image_files', static_url_path='')

@app.route("/")
def welcome():
	return "potato"

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
