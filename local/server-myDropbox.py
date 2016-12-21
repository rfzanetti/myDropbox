import os, boto3
from flask import Flask, request

app = Flask(__name__)

fileList = []

def loadControlFile():
	s3 = boto3.resource('s3')
	s3.Bucket('mydropbox.sd').download_file('fileList.ctl', 'fileList.ctl')

	files = [line.rstrip('\n') for line in open('fileList.ctl')]
	for file in files:
		fileList.append(file)

def saveControlFile():
	ctlfile = open('fileList.ctl', 'w')

	fileContent = ''

	for file in fileList:
		fileContent += file
		fileContent += '\n'

	fileContent = fileContent[:-1]

	ctlfile.write(fileContent)

	ctlfile.close()

	s3 = boto3.resource('s3')
	file = open('fileList.ctl', 'r')
	s3.Bucket('mydropbox.sd').put_object(Key='fileList.ctl', Body=file)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/files')
def files():
	filepaths = ''
	for f in fileList:
		if f[-3:] == "txt":
			filepaths += f 
			filepaths += '\n'

	return filepaths

@app.route('/add', methods=['GET', 'POST'])
def addFile():
	fileList.append(request.values["filename"])
	print request.values["filename"]
	saveControlFile()
	return request.values["filename"]

@app.route('/remove', methods=['GET', 'POST'])
def removeFile():
	filename = request.values["filename"]
	if filename in fileList:
		fileList.remove(filename)
	saveControlFile()
	return request.values["filename"]
	
if __name__ == "__main__":
	loadControlFile()
	app.run(port=5000)