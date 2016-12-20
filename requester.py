import requests, json, subprocess
import os
import boto3
import time


def downloadFileFromS3(filename):
	s3 = boto3.resource('s3')
	s3.Bucket('mydropbox.sd').download_file(filename, filename)

def getServerFiles():
	response = requests.get('http://127.0.0.1:5000/files')

	return response.text.split(';')[:-1]

def getNewFiles():
	thisFiles = [f for f in os.listdir('.') if os.path.isfile(f)]
	serverFiles = getServerFiles()

	newFiles = []

	for serverFile in serverFiles:
		if serverFile not in thisFiles:
			if serverFile[-3:] == 'txt':
				newFiles.append(serverFile)

	return newFiles

if __name__ == '__main__':
	while True:
		newFiles = getNewFiles()
		deletedFiles = getDeletedFiles()
		if len(newFiles) > 0:
			for f in newFiles:
				downloadFileFromS3(f)

		time.sleep(5)


