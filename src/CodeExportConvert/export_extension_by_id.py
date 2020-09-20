"""Export extensions from Hulk(findFromHid)
Also DBSCAN results (dbScanTry1)
Usage:
    export_extensions.py -f <file>
    export_extensions.py -n <count>
    export_extensions.py -d <hid>
"""

from docopt import docopt
import mongo
import sys
import os
from mongoengine import *

from mongoengine.queryset.visitor import Q
# import datetime
# import pkgutil
# import numpy as np
# import matplotlib.pyplot as plt
# this is the package we are inspecting 
# import analyzer.db as ammm
# from sklearn.cluster import DBSCAN
# from sklearn import metrics
# from sklearn.datasets.samples_generator import make_blobs
# from sklearn.preprocessing import StandardScaler
# import pandas as pd
# import itertools

def tostring(detection_array):
	s = ""
	for d in detection_array:
		s += "[[%s-%s] %s]" % (d.c, d.did, d.d)
	return s

def main(arguments):
	# how to find HIds by file provided -f 
	findFromHid(arguments)

	#search for closest date by file provided -f
	# searchClosestDate(arguments)

	# query for sum of apis on api_freq
	# sumApis()
	# checkResults1()

	'''
	use sklearn DBSCAN
	'''
	# dbScanTry1()

	'''
	plot average of each of the groups created by DBSCAN
	% runs after dbScanTry1
	'''
	'''
	TODO: write this functions
	'''
	# clusterAverageBarPlot()

	'''
	plot bars of summations of API freqs
	% needs to run from office (because connects to hulk)
	'''
	# sumFreqApiBarPlot()

	'''
	test pairwise function to see bug where there is no direct
	transformation
	'''
	# pairwiseTest()


def findFromHid(arguments):
	try:
		os.makedirs("/tmp/data")
	except:
		pass

	if arguments["-f"]:
		with open(arguments["<file>"]) as f:
			extensions = f.readlines()

		extensions = [x.strip() for x in extensions]
		query = mongo.Queue.objects(hid__in=extensions).order_by("-ts")
	elif arguments["-d"]:
		query = mongo.Queue.objects(hid=arguments["<hid>"]).order_by("-ts")
	else:
		query = mongo.Queue.objects().order_by("-ts")	

	count = 0
	md5s = {}
	print(len(query))
	for ext in query:
		# no extension duplicates
		# if ext.crx is None or ext.md5 in md5s:
		# 	continue
		# if arguments["-f"]:
		# 	if ext.hid not in extensions:
		# 		continue
		crx = ext.crx.read()
		if crx is None:
			continue
		md5s[ext.md5] = True

		# print "%s" % (ext.hid)
		# put the directory here
		dirCustom = 'malicious_131'

		if not os.path.exists("/home/npantel/data/" + str(dirCustom)):
			os.makedirs("/home/npantel/data/" + str(dirCustom))

		with open("/home/npantel/data/" + dirCustom + "/%s-%s-%s.crx" % (ext.hid, ext.ts, ext.md5), "wb") as f:
			f.write(crx)
		count += 1
		if arguments["-n"] and count > int(arguments["<count>"]):
		    break
	# os.system("ssh nikos@152.14.90.84 \"mkdir -p /media/nikos/fourTera1/homeA/" + str(dirCustom) + "\"")
	# put them to office, the whole folder
	os.system("rsync -ru /home/npantel/data/" + str(dirCustom) + " nikos@152.14.90.84:/media/nikos/fourTera1/homeA")


def pairwiseTest():
	inputDir = "/media/nikos/fourTera1/homeA/bhoofappogmodaofmiaihhodalnokbfo/extracted"
	tempOutNameList = sorted(os.listdir(inputDir))
	for version1, version2 in pairwise(tempOutNameList):
		allFiles1 = walkComplete(inputDir + '/' + version1)
		allFiles2 = walkComplete(inputDir + '/' + version2)
		flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
		flat_list2 = [item for item in allFiles2 if item.endswith('.js')]
		maxLength = max(len(flat_list1), len(flat_list2))
		mainPart1 = inputDir + '/' + version1
		mainPart2 = inputDir + '/' + version2
		lastPart1 = ["/".join(n.split('/')[8:]) for n in flat_list1]
		lastPart2 = ["/".join(n.split('/')[8:]) for n in flat_list2]
		flat_list12 = list(set(lastPart1) - set(lastPart2))
		flat_list21 = list(set(lastPart2) - set(lastPart1))
		common12 = list(set(lastPart1) & set(lastPart2))
		parts1 = common12 + flat_list12 + ['None']*len(flat_list21)
		parts2 = common12 + ["None"]*len(flat_list12) + flat_list21
		flat_list1 = [mainPart1 + '/' + parts1Each for parts1Each in parts1]
		flat_list2 = [mainPart2 + '/' + parts2Each for parts2Each in parts2]
		for files1, files2 in itertools.zip_longest(flat_list1, flat_list2):
			print(files1)
			print(files2)
			print("\n")

def walkComplete(path1):
	returnList = []
	for directory, subdirectories, files in os.walk(path1):
		for file1 in files:
			returnList.append(os.path.join(directory, file1))
	return returnList


def pairwise(iterable):
	"s -> (s0,s1), (s1,s2), (s2, s3), ..."
	a, b = itertools.tee(iterable)
	next(b, None)
	return zip(a, b)


def sumFreqApiBarPlot():
	'''
	connect to hulk from office
	'''
	connect("analyzer", username="npantel", host="localhost", port=37017)
	
	query = mongo.apiFreqStorageUpdOrder.objects(sum0__gte=0)

	print(len(query))
	sum0List = []
	for each in query:
		if "None" not in each.name:
			sum0List.append(each.sum0)

	print(len(sum0List))
	myBins = [-1,0,1,2,5,10,15,20,300]
	pdOutput = pd.cut(sum0List, bins=myBins, include_lowest=True)
	# print((pdOutput.categories.values[0].tolist()))
	# return
	ax = pdOutput.value_counts().plot.bar(rot=0, color='r', figsize=(6,4))
	ax.set_xticklabels(zip(myBins[:-1], myBins[1:]))
	# ax.set_xticklabels([c[1:-1].replace(","," to") for c in zip(myBins[:-1], myBins[1:])])
	plt.show()

	'''
	print value counts with sorted categories
	% command:
	out.value_counts().reindex(out.cat.categories)
	'''

def clusterAverageBarPlot():
	pass

def dbScanTry1():
	'''
	connection because you run from office
	'''
	connect("analyzer", username="npantel", host="localhost", port=37017)
	# eps = [1.5, 2, 3, 5,10]
	eps = [0.1]
	# eps = [3]
	# min_samples = [2, 5, 10, 20, 30, 50 , 75, 100]
	min_samples = [2]

	query0 = mongo.apiFreqStorageUpdOrderB.objects(sum0__gte=1)
	# print(type(query0))
	# print(list(query0)[:10])
	# return
	print(len(query0))
	'''
	create new function that takes the query and returns 
	1) only those values that don't have none
	and
	2) those that come from the same versions, merge them
	and return the summation of the values
	'''
	# queryModified = removeNoneAndMerge(query0)
	inputNames = [each.name for each in query0]
	input0List = [each.apiFreqsUpdated for each in query0]
	input0 = np.asarray(input0List)
	# input0 = np.empty
	# for each in query:
	# 	input0 = np.append(input0, each.apiFreqs)
	# input0 = [np.array(each.apiFreqs for each in query)]
	# print(input0[:10])
	'''
	TODO: check if it is None
	TODO: check if it is from the same hid_version
	TODO: check clusters after that
	'''
	'''
	dice distance metric check
	'''
	for eps_ in eps:
		for min_samples_ in min_samples:
			db = DBSCAN(eps=eps_, min_samples=min_samples_).fit(input0)
			core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
			core_samples_mask[db.core_sample_indices_] = True
			labels = db.labels_

			# Number of clusters in labels, ignoring noise if present.
			n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
			n_noise_ = list(labels).count(-1)

			print(' For eps = %d and min_samples = %d' % (eps_, min_samples_))
			print('Estimated number of clusters: %d' % n_clusters_)
			print('Estimated number of noise points: %d' % n_noise_)

			'''
			count unique labels
			'''
			uniqueLabels = []
			for each in list(labels):
				if each not in uniqueLabels:
					uniqueLabels.append(each)
			print(uniqueLabels)
			uL_count = []
			for uL in uniqueLabels:
				uL_count.append(list(labels).count(uL))
			print("unique count = " + str(uL_count))
	print("number of labels = " + str(len(labels)))
	'''
	choose which cluster to show
	'''
	# chooseCluster = 38
	for i in range(39, 100):
		chooseCluster = i
		clusterList = []
		clusterListFreqs = []
		for labelIndex in range(len(labels)):
			if(labels[labelIndex] == chooseCluster):
				# clusterList.append(input0[labelIndex])
				clusterList.append(inputNames[labelIndex])
				clusterListFreqs.append(input0List[labelIndex])
		hidsToPrint = []
		for (eachElement, eachFreq) in zip(clusterList, clusterListFreqs):
			hidsToPrint.append(eachElement.split('_')[0])
		print(unique(hidsToPrint))
		for (eachElement, eachFreq) in zip(clusterList, clusterListFreqs):
			print(eachElement)
		print(eachFreq)
		# print(clusterList[:50])
		print(len(clusterList))

# function to get unique values 
def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    # print list 
    for x in unique_list: 
        print(x,)

def removeNoneAndMerge(query):
	queryWithoutNone = []
	for each in query:
		if 'None' in each.name:
			queryWithoutNone.append(each)
	uniqueComparisons = {}
	for each in queryWithoutNone:
		twoVersions = each.name.split("_")[:10]
		if(twoVersions not in uniqueComparisons):
			uniqueComparisons[twoVersions].append(each.apiFreqs)

	'''
	sumUp all list elements for every key of the dictionary
	'''

def checkResults1():
	# connect("analyzer", username="npantel", host="localhost", port=37017)
	# query = mongo.Queue.objects(hid="mgbaaaipdlpccmepeghoaemnhpebfbnp").order_by("ts")
	query = mongo.apiFreqStorageUpdOrder.objects(sum0__gte=(20)).order_by("ts")
	# for each in query:
		# print(each.ts)
	# return

	unique_hid_list = []
	names = []
	sums = []
	counts = []
	unique_comp_names = []
	print(len(query))
	# return
	for each in query:
		compNameTemp = str(each.name).split("_")[:10]
		if compNameTemp not in unique_comp_names:
			# if("None" not in str(each.name)):
			unique_comp_names.append(compNameTemp)
		# if each.hid not in unique_hid_list:
		# 	unique_hid_list.append(each.hid)
		# 	names.append(each.name)
		# 	sums.append(each.sum0)
		# 	counts.append(each.apiFreqs)

	# print(len(unique_hid_list))
	print(len(unique_comp_names))
	# print(names[:20])
	# print(unique_hid_list[:20])
	# print(sums[:20])
	# print(counts[:20])

def sumApis():
	query = mongo.apiFreqStorage.objects()

	outFile = ("./outFile.txt", "w+")
	print(query[0])
	# return
	for each in query:
		sum = 0
		freqs = each.apiFreqs.read()
		for freq in freqs:
			sum += freq
		outFile.write(sum)
		outFile.write("\n")

def searchClosestDate(arguments):
	# count how many days
	for eachFile in os.listdir('./keywords'):
		try:
		# 	with open('./keywords/' + eachFile, 'r') as f:
		# # with open('./keywords/injects_ads', 'r') as f:
		# 		extensionsID = f.readlines()
		# 	print(f)
		# 	list1 = []
		# 	lastHid = ''
		# 	counter = 0
		# 	for line in extensionsID:
		# 		# print(lastHid)
		# 		hid = line.split('\t')[0]
		# 		hid = hid.split(':')[-1]
		# 		if(str(lastHid) != str(hid)):
		# 			date = line.split('\t')[-1]
		# 			date = date.split('\n')[0]
		# 			date = datetime.datetime.strptime(date, '%b %d, %Y')
		# 			# print(hid)
		# 			# print(date)
		# 			# return
					# query1 = mongo.Queue.objects( Q(hid=hid) & Q(ts__gte=(date)) )
		# 			query2 = mongo.Queue.objects( Q(hid=hid) & Q(ts__lte=(date)) )

		# 			if( (len(query2) > 0) & (len(query1) > 0)):
		# 				min1 = (query2[0].ts - date).days
		# 				if((query1[0].ts - date).days < min1):
		# 					min1 = (query1[0].ts - date).days
		# 				list1.append(min1)
		# 			lastHid = hid
		# 		counter += 1
		# 		# print(str(counter) + '/' + str(len(extensionsID)))


			# print(list1)
			# # plot histogram
			bins = np.zeros(7)
			# for block in list1:
			# 	block = abs(block)
			# 	#BINS
			# 	if((block) <= 1):
			# 		bins[0] += 1
			# 	elif((block) <= 2):
			# 		bins[1] += 1
			# 	elif((block) <= 5):
			# 		bins[2] += 1 
			# 	elif((block) <= 10):
			# 		bins[3] += 1 
			# 	elif((block) <= 20):
			# 		bins[4] += 1 
			# 	elif((block) <= 30):
			# 		bins[5] += 1
			# 	else:
			# 		bins[6] += 1   

			# print(bins)

			# ******************************************************
			# # START OF PLOT NUMBER OF REVIEWS PER EXTENSION
			# *******************************************************
			bins[0] = 370
			bins[1] = 280
			bins[2] = 413
			bins[3] = 404
			bins[4] = 553
			bins[5] = 677
			bins[6] = 1127

			plt.close("all") 
			bins = bins.astype(int)
			# for i in range(len(bins)):
			    # bins[i] = int(bins[i])
			print(bins)
			# bins = np.ones(7)
			# bins.plt.hist()  
			fig, ax = plt.subplots()
			# bins = [log(bin,10) for bin in bins]
			# bins = [log(bin,10) for bin in bins]
			width = 0.8
			binss = ['1', '2', '[3-5]', '[6-10]', '[11-20]', '[21-30]', '>30']
			# binss = ['0', '1', '5', '15', '25', '45', '75']
			# binss = [1,2,3,4,5,6,7]
			ax.bar(binss, bins, width=width)
			x = binss
			y = bins
			for a,b in zip(x, y):
			    ax.text(a, b, str(b))
			# ind = np.arange(len(bins))
			# ax.barh(bins, ind, width, color="blue")
			# plt.hist(np.transpose(bins), bins='auto')
			# plot()
			# ax.set_yscale('log')
			ax.set_xlabel('No Days')
			ax.set_ylabel('No. Extensions')

			plt.show()

			# ******************************************************
			# # END OF PLOT
			# ******************************************************
		except:
			pass

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Export Extensions 1.0')
    main(arguments)
