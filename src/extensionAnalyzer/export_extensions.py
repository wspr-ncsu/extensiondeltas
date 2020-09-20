# """Export extensions from Hulk.

from docopt import docopt
import analyzer.db.mongo as db
import sys
import os
import glob
import io, zipfile

def main(): 
    # uploadDrive()
    # nameIdMatching(arguments)
    # queriesTesting()
    # searchForHid()
    queryPathSearch()

def queryPathSearch():
	with open('manually_malicious_hid.txt', 'r') as f:
		extensionsID = f.readlines()
	# on mongo db
	# Find by hid:
	# db.queue.find({"hid": "epanfjkfahimkgomnigadpkobaefekcd"})
	for eachID in extensionsID:
		query = db.Queue.objects(hid=eachID)
	print('query is done ' + str(len(query)))
	count = 0
	md5s = {}
	for ext in query:
		if ext.crx is None or ext.md5 in md5s:
			print('none/md5s')
			continue		
		crx = ext.crx.read()
		if crx is None:
			print('none')
			continue
		md5s[ext.md5] = True
		date = str(ext.ts)
		date = date.translate(None, ': ')
		# with open("/home/npantel/data/%s-%s-%s.crx" % (ext.hid, date, ext.md5), "wb") as f:
		# 	print("/home/npantel/data/%s-%s-%s.crx" % (ext.hid, date, ext.md5))
		# 	f.write(crx)
		count += 1
	print count	

def uploadDrive():
	zipList = glob.glob("/home/npantel/data/*.zip")
	for each in zipList:
		crx = each.split('.zip')[0]
		zipID = each.split('-')[0]
		zipID = zipID.split('/')[-1]
		findFolderCommand = 'gdrive list -q \"name = \'' + zipID + '\'\" > tempFile.txt'
		os.system(findFolderCommand)
		folderID = str(open('tempFile.txt', 'r').readlines()[1]).split(' ')[0]
		os.system('gdrive upload --parent ' + str(folderID) + ' ' + each)
		os.system('gdrive upload --parent ' + str(folderID) + ' ' + crx + '.crx')

def queriesTesting():
	nameFile = open('nameFileAll.txt', 'a')	
	query = db.Queue.objects(priority=0)
	count = 0
	nameFound = 0

	for each in query:
		try:
			try:
				archive = zipfile.ZipFile(each.crx, 'r')
			except zipfile.BadZipfile:
				archive.close()
				raise IOError
			manifest = archive.read('manifest.json')
			for line in manifest.split('\n'):				
				string = "\"name\":"
				if string in line:
					nameFound += 1
					line = line.split(':')[1]
					line = line.split(',')[0]
					command = "echo " + str(line) + ',' + str(count) + ' >> nameFileAll.txt'
					os.system(command)	
					command = "echo " + str(each.hid) + ',' + str(count) + ' >> nameFileAll.txt'
					os.system(command)	
					archive.close()
					break	
			archive.close()								 			
		except IOError:
			print("Manifest.json not Found on count = " + str(count))
		count += 1
		print("count NOW = " + str(count) + '\n' + "nameFound on those = " + str(nameFound))
	return 0

def nameIdMatching(arguments):
	with open(arguments["<file>"]) as f:
		extensionsID = f.readlines()
	for eachName in extensionsID:
		query = db.Queue.objects(id_field=eachName)	
		print query		
		return
	count = 0
	md5s = {}
	for ext in query:
		if ext.crx is None or ext.md5 in md5s:
			print('none/md5s')
			continue		
		crx = ext.crx.read()
		if crx is None:
			print('none')
			continue
		md5s[ext.md5] = True

		date = str(ext.ts)
		date = date.translate(None, ': ')
		with open("/home/npantel/data/A%s-%s-%s.crx" % (ext.hid, date, ext.md5), "wb") as f:
			f.write(crx)
		count += 1
	print count	

def searchForHid():
	outFile = open('getHids', 'w+')
	counter = 0
	directory = './minus10/'
	for each in os.listdir(directory):
		if( (os.path.getsize(directory + each) > 122 ) ):
			each = each.split('.csv')[0]
			query = db.Queue.objects(hid=each)
			# print(query)
			# return 0
			if(len(query) > 0):
				counter += 1
				for objects in query:
					outFile.write(str(objects.hid) + '\n')
	print(counter)
	print("out of 1493")


if __name__ == '__main__':
    main()


