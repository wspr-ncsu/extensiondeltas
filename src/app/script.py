#!/usr/bin/env python3
import logging
import os
import random
import sys
import time
from mongoengine import *
import mongoExtensionsAST as mongo
# from my_function import specialLCS
# from extractApisFromDb import *
# from rq import Queue
import rq
import redis
# from redis import Redis

MESSAGE = os.environ.get("MESSAGE", "YOUR_MESSAGE_HERE")

REDIS_HOST = os.environ.get("REDIS_HOST", "npantel-redis-test")
# REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
# REDIS_PORT = int(os.environ.get("REDIS_PORT", "8000"))

QUEUE_NAME = os.environ.get("QUEUE_NAME", "default")


def main(argv):
    # connect("extensionsASTnpantel", host="hulk.csc.ncsu.edu", port=27077)
    disconnect()
    connect("analyzer", host="hulk.csc.ncsu.edu", port=27077)

    # UNCOMMENT NEXT 4 LINES
    # connect("extensionsASTnpantel", username="npantel", host="localhost", port=37017)

    # load data from query
    # queue = readFromDatabase()
    # queuetest = ['a','b','c','d','e','f','g','h','i','j','k','l']
    # put them and run them in the queue
    # specialLCSHandler(queue)
    with rq.Connection(redis.Redis(REDIS_HOST, REDIS_PORT)) as connection:

        # print(job.result)
        w = rq.Worker([QUEUE_NAME])
        w.work()
        # q = rq.Queue(connection=connection)
        # job = q.enqueue(specialLCS, queuetest, queuetest[1:])        
        # dTable = mongo.diffStore(hid1='abc', hid2='abd', commonLength=job.result)
        # dTable.save()

if __name__ == "__main__":
    # log basic info
    logging.basicConfig(level=logging.INFO)
    try:
        main(sys.argv)
    except:
        logging.exception("Something just went terribly wrong--have fun tracking it down!")
        sys.exit(1)

