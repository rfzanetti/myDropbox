import requests, json, subprocess
import os
import boto3
import time


def downloadFileFromS3(filename):
	s3 = boto3.resource('s3')
	s3.Bucket('mydropbox.sd').download_file(filename, filename)

def deleteFileFromS3(filename):
	cl = boto3.client('s3')
	cl.delete_object(Bucket='mydropbox.sd', Key=filename)

def getServerFiles():
	response = requests.get('http://mydropbox-sd.herokuapp.com/files')

	return response.text.split('\n')

def getNewFiles():
	thisFiles = [f for f in os.listdir('.') if os.path.isfile(f)]
	serverFiles = getServerFiles()

	newFiles = []

	for serverFile in serverFiles:
		if serverFile not in thisFiles:
			if serverFile[-3:] == 'txt':
				newFiles.append(serverFile)

	return newFiles


def getDeletedFiles():
	thisFiles = [f for f in os.listdir('.') if os.path.isfile(f)]
	serverFiles = getServerFiles()

	deletedFiles = []

	for thisFile in thisFiles:
		if thisFile not in serverFiles:
			if thisFile[-3:] == 'txt':
				deletedFiles.append(thisFile)

	return deletedFiles

if __name__ == '__main__':
	while True:
		newFiles = getNewFiles()
		deletedFiles = getDeletedFiles()

		if len(newFiles) > 0:
			for f in newFiles:
				downloadFileFromS3(f)

		if len(deletedFiles) > 0:
			print deletedFiles
			for f in deletedFiles:
				deleteFileFromS3(f)
				os.unlink(f)
		else:
			print "nada"

		time.sleep(10)


