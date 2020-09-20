#!/usr/bin/env python3
'''
Check Jobs
rq info -u redis://localhost:9000
'''

import logging
import os
import random
import sys
import time
from mongoengine import *
import mongoExtensionsAST as mongo
from rq import Queue
from redis import Redis
import operator
import itertools
from extractApisFromDb1 import *

MESSAGE = os.environ.get("MESSAGE", "YOUR_MESSAGE_HERE")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "9000"))

def main(argv):
	emptyQueue()
	enqueueByHid()

def enqueueByHid():
	disconnect()
	connect("analyzer", username="npantel", host="localhost", port=37017)
	# connect("analyzer", username="npantel", host="hulk.csc.ncsu.edu", port=37017)

	q = Queue(connection=Redis(REDIS_HOST, REDIS_PORT))
	hidQueue = open("./uniqueAllHids.txt", 'r').readlines()
	# for 30 APIs only
	combList = open('./thirtyOnlyApis.txt', 'r').read().splitlines()
	# for all APIs
	# combList = open('./combList.txt', 'r').read().splitlines()

	for i, eachHid in enumerate(hidQueue):
		eachHid = eachHid.strip()
		q.enqueue(generalHandler, eachHid, combList)
		print(i)

def emptyQueue():
	q = Queue(connection=Redis(REDIS_HOST, REDIS_PORT))
	q.empty()
	return

if __name__ == "__main__":
	# log basic info
	logging.basicConfig(level=logging.INFO)
	try:
		main(sys.argv)
	except:
		logging.exception("Something just went terribly wrong--have fun tracking it down!")
		sys.exit(1)

