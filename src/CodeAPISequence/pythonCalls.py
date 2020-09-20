import os
import subprocess
import operator

def main():
	# inDir = './allExtensionsAfterDiff/adds'
	inDir = '/media/nikos/fourTera1/homeA/javascriptCode'
	callAnalyzeCalled(inDir)
	# CALL THE JAVASCRIPT FILE
	# TO PRODUCE THE API SEQUENCE
	# OR THE HIGH LEVEL AST
	# CHANGE NEXT LINE	
	# inDir = '/media/nikos/fourTera1/homeA/manyCrxFiles/extracted'
	inDir = '/media/nikos/fourTera1/homeA/hashesJS'

	# produceWholeAST(inDir)
	
	inDir = '/media/nikos/fourTera1/homeA/vpcApi'
	outDir = '/media/nikos/fourTera1/homeA/vpcApiOut'
	# apiCount(inDir, outDir)

	# get literally top X from each mouse event catergory + add event listener
	inDir = '/media/nikos/fourTera1/homeA/vpcApi'
	# allApis = getAllApis(inDir)
	inDir = '/media/nikos/fourTera1/homeA/vpcApiOut'
	X = 100
	# getTopXEachMouseEvent(X, inDir, allApis)

def produceWholeAST(inDir):
	counter = 0 
	errorCount = 0
	for each in sorted(os.listdir(inDir)):
		# CHANGE NEXT LINE
		# allFiles1 = walkComplete(inDir + '/' + each)
		# CHANGE NEXT LINE
		# flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
		flat_list1 = [inDir + '/' + each]
		# print(flat_list1)
		for eachJsFile in flat_list1:   
			try:
				# CHANGE NEXT LINE
				# print(eachJsFile)
				fileName = eachJsFile.split('/')
				# CHANGE NEXT LINE				
				# fileNameOut = str(fileName[7]) + '_' + str(fileName[-1])
				fileNameOut = fileName[-1]
				# print(fileNameOut)
				subprocess.call(["node", "analyzeCalled.js", str(eachJsFile), fileNameOut])
			except:
				errorCount += 1
				continue
		counter += 1
		print(counter)
		# print("error per FOLDER = %s" % str(errorCount/counter))


def callAnalyzeCalled(inDir):
	counter = 0
	inDirList = walkComplete(inDir)
	for each in inDirList:
		# eachJSFolder = "/".join(each.split("/")[:-1])
		fileNameOut = each.split("/")[-1]
		# print("eachJSFolder = " + str(eachJSFolder))
		print("fileNameOut = " + fileNameOut)
		subprocess.call(["node", "analyzeCalled.js", each, fileNameOut])
		counter += 1
	# for each in os.listdir(inDir):
	# 	statinfo = os.stat(inDir + '/' + str(each))
	# 	print(str(statinfo.st_size) + '\t\t' + str(each))
	# 	if(statinfo.st_size < 1000000):
	# 		counter += 1
	# 		subprocess.call(["node", "analyzeCalled.js", str(each)])
	print(counter)

def walkComplete(path1):
	returnList = []
	for directory, subdirectories, files in os.walk(path1):
		for file1 in files:
			returnList.append(os.path.join(directory, file1))
	return returnList

def apiCount(inDir, outDir):
	dictionary = {}
	for eachFile in sorted(os.listdir(inDir)):
		with open(inDir + '/' + eachFile, 'r') as file1:
			csvList = file1.read().split(',')
			# print(len(csvList))
			for eachApi in csvList:
				if(len(eachApi) > 2):
					dictionary[eachApi] = 0
	print(len(dictionary))
	# count = 0 
	# for keys in dictionary:
	# 	if(len(keys) == 4):
	# 		print(keys)
	# 		count += 1
	# print(count)
	count = 0 
	# for each add how many of each (SORTED)
	for eachFile in sorted(os.listdir(inDir)):
		tempDictionary = {}
		for keys in dictionary:
			tempDictionary[keys] = 0
		with open(inDir + '/' + eachFile, 'r') as file1:
			csvList = file1.read().split(',')
			# print(eachFile)
			# print(csvList)
			for eachApi in csvList:
				if(len(eachApi) > 2):
					tempDictionary[eachApi] += 1
		# sort dictionary and write to output
		tempDictionary1 = sorted(tempDictionary.items(), key=operator.itemgetter(1), reverse=True)
		with open(outDir + '/' + eachFile, 'w+') as file2:
			for (key,val) in tempDictionary1:
				file2.write(str(key) + "=>" + str(val) + '\n')
		count += 1
		print(count)
		# break

def getAllApis(inDir):
	dictionary = {}
	for eachFile in sorted(os.listdir(inDir)):
		with open(inDir + '/' + eachFile, 'r') as file1:
			csvList = file1.read().split(',')
			# print(len(csvList))
			for eachApi in csvList:
				if(len(eachApi) > 2):
					dictionary[eachApi] = 0
	print(len(dictionary))
	return dictionary

def getTopXEachMouseEvent(X, inDir, allApis):
	# if has mouseevent on it
	# or if it has add event listener
	# add on list (65 in total)
	# for each of the 65 check top 100
	#dir = vpcOUt
	# cluster those 65*100 with everything to find new similarities
	# find new method

	# testFile = 'fffbaf716d73d37ccea7e681e1bc34da2b4ae48805d80cdcdc8232acca4f182c'
	# keepList = []
	# with open(inDir + '/' + testFile, 'r') as inFile:
	# 	lines = inFile.readlines()
	# 	print((lines))
	# 	for line in lines:
	# 		line = line.split('=')[0]
	# 		print(line)
	# 		if 'addEventListener' in line:
	# 			keepList.append(line)
	# 		if 'mouseevent' in line:
	# 			keepList.append(line)
	# print(keepList)
	# print(len(keepList))
	
	keepList = []	
	for line in allApis:
		if 'addeventlistener' in line.lower():
			keepList.append(line)
		if 'mouseevent' in line.lower():
			keepList.append(line)
	streamAllFiles(keepList, inDir)

def streamAllFiles(keepList, inDir):
	# TODO: SORT THE INPUT FILES 
	listOfFiles = []
	count = 0
	keepList = ['addEventListener']
	for apiSelect in keepList:
		top10Temp = []
		for eachFile in sorted(os.listdir(inDir)):
			with open(inDir + '/' + eachFile, 'r') as inFile:
				lines = inFile.readlines()
				for line in lines:
					line = line.split('=>')
					# print(apiSelect)
					# print(line[0])
					if(apiSelect == line[0]):
						top10Temp.append((line[0], line[1].split('\n')[0], eachFile))
			count += 1
			print(count)
		print(top10Temp)
		# top10Sort = top10Temp.sort(key=lambda tup: tup[1], reverse=True)
		top10Sort = sorted(top10Temp, key=lambda tup: tup[1], reverse=True)
		print(top10Sort[:500])
		# break



if __name__ == '__main__':
	main()