import os, boto3
from flask import Flask, request

app = Flask(__name__)

def getFileList():
	fileList = []
	s3 = boto3.resource('s3')
	s3.Bucket('mydropbox.sd').download_file('fileList.ctl', 'fileList.ctl')

	files = [line.rstrip('\n') for line in open('fileList.ctl')]
	for file in files:
		fileList.append(file)

	return fileList

def saveFileList(fileList):
	print "\n\nENTREI SAVEFILE\n\n"
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
	fileList = getFileList()

	fileList.append("warriors.txt")

	saveFileList(fileList)

	f = getFileList()

	return str(f)

@app.route('/files')
def files():
	fileList = getFileList()

	filepaths = ''
	for f in fileList:
		if f[-3:] == "txt":
			filepaths += f 
			filepaths += '\n'

	return filepaths

@app.route('/add', methods=['GET', 'POST'])
def addFile():
	print "\n\nENTREI ADD\n\n"
	fileList = getFileList()

	fileList.append(request.values["filename"])

	print fileList
	saveFileList(fileList)

	return request.values["filename"]

@app.route('/remove', methods=['GET', 'POST'])
def removeFile():
	fileList = getFileList()

	filename = request.values["filename"]

	if filename in fileList:
		fileList.remove(filename)

	saveFileList(fileList)

	return request.values["filename"]
	
if __name__ == "__main__":
	app.run()
