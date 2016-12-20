import os
from flask import Flask 

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/files')
def files():
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	filepaths = ''
	for f in files:
		if f[-3:] == "txt":
			filepaths += f 
			filepaths += ';'

	return filepaths


if __name__ == "__main__":
	app.run(port=5001)