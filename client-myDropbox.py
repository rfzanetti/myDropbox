import time  
import sys
import boto3
import requests
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler

class S3Control():

	def uploadFileToS3(self, filepath):
		s3 = boto3.resource('s3')
		file = open(filepath, 'r')
		s3.Bucket('mydropbox.sd').put_object(Key=filepath, Body=file)

	def deleteFileFromS3(self, filename):
		cl = boto3.client('s3')
		cl.delete_object(Bucket='mydropbox.sd', Key=filename)

class MyHandler(PatternMatchingEventHandler):
	patterns = ["*.txt"]

	S3Controller = S3Control()

	def process(self, event):
		print event.src_path, event.event_type

	def on_modified(self, event):
		self.process(event)
		self.S3Controller.uploadFileToS3(event.src_path[2:])

	def on_created(self, event):
		self.process(event)
		self.S3Controller.uploadFileToS3(event.src_path[2:])

	def on_deleted(self, event):
		self.process(event)
		self.S3Controller.deleteFileFromS3(event.src_path[2:])

if __name__ == '__main__':
	args = sys.argv[1:]
	observer = Observer()
	observer.schedule(MyHandler(), path='.')
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()
