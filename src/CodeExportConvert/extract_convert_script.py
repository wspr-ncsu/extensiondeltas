# import crx_unpack
import os, errno
from filecmp import dircmp
import jsbeautifier
import zipfile

def main():
	# zipsBeautifier('/home/nikos/Desktop/temp/test2')
	# return
	# initialize directories
	# 1) CHANGE NEXT LINE FOR HID
	# startswithString = "manyCrxFiles"
	# startswithStringList = ['bhoofappogmodaofmiaihhodalnokbfo', 'ceiljlhenjgjmffkmfccjoehdpppcgfg', 'hompjdfbfmmmgflfjdlnkohcplmboaeo', 'emeokgokialpjadjaoeiplmnkjoaegng', 'gidlfommnbibbmegmgajdbikelkdcmcl', 'gfenjblodoldnbiddmggcbkcapiolbig']
	startswithStringList = ['malicious_131']
	for startswithString in startswithStringList:
		# 2) CHANGE NEXT 2 LINES IF IN MANYCRXFILES
		# extraDir = "manyCrxFiles"
		# crxDirectory = "./" + startswithString + "/"	
		crxDirectory = "/media/nikos/fourTera1/homeA/" + str(startswithString) + "/"

		# crxDirectory = "/home/nikos-ubuntu/Documents/PHD/malicious_extensions_fall_18_code/" + str(startswithString) + "/"
		beautifyDirectory = "/media/nikos/fourTera1/homeA/" + startswithString + "/extracted/"
		# beautifyDirectory = "/home/nikos-ubuntu/Documents/PHD/malicious_extensions_fall_18_code/" + str(startswithString) + "/extracted/"


		# unzip from crx to directory they are + /extracted
		crxToZipToUnzip(crxDirectory, startswithString)
		# beautify all javascript in file

		# renameDir(beautifyDirectory)

		# print(beautifyDirectory)
		# beautifyDirectory = '/media/nikos/fourTera1/homeA/manyCrxFiles/extracted/aeeajafchghccbnppaimjhhfpejabole-2016-09-03_00:10:51.385000-cc9e5cd4e99747696f4f43971f922beb/scripts/js'
		zipsBeautifier(beautifyDirectory)

		# beautify the json files
		# jsonBeautify(beautifyDirectory)

		# single beautify ".js" file
		# beautifyFile = "/media/nikos/fourTera1/homeA/unlistedMine/extracted/controller2.js"
		# beautifySingleFile(beautifyFile)

		# extractAllHidsFromDirectory()
		# dcmp = dircmp('./epanfjkfahimkgomnigadpkobaefekcd2', 'epanfjkfahimkgomnigadpkobaefekcd3')
		# counter = 0
		# counter = countDiffs(dcmp, counter)
		# print(counter)

def crxToZipToUnzip(crxDirectory, startswithString):
	# outDirectory = crxDirectory + "extracted/"
	outDirectory = "/media/nikos/fourTera1/homeA/" + startswithString + "/extracted/"
	# outDirectory = "/home/nikos-ubuntu/Documents/PHD/malicious_extensions_fall_18_code/" + str(startswithString) + "/extracted/"

	# create out directory if doesn't exist
	if not os.path.exists(outDirectory):
		os.makedirs(outDirectory)

	counter = 0
	# create output directory if doesn't exist
	try:
		os.makedirs(outDirectory)
	except FileExistsError:
		pass
	for each in os.listdir(crxDirectory):
		print(str(crxDirectory) + str(each) )
		fEach = crxDirectory + each
		# 3) CHANGE NEXT LINE IF IN MANYCRXFILES DIRECTORY
		# if(str(each).endswith(".crx") & str(each).startswith("fngmhnnpilhplaeedifhccceomclgfbg")):
		# TODO: second attempt
		if not os.stat(fEach).st_size:
			continue
		if(str(each).endswith(".crx")):
			tempDir = each.split(".crx")[0]		
			z = zipfile.ZipFile(fEach, mode='r')
			z.extractall(outDirectory + tempDir)
			counter += 1
		elif os.path.isfile(outDirectory + each):
			z = zipfile.ZipFile(fEach, mode='r')
			z.extractall(outDirectory + each)
			counter += 1			
		# return
		# TODO: first attempt
		# if(str(each).endswith(".crx")):
		# 	# print(open(fEach, encoding = "ISO-8859-1").read())
		# 	try:
		# 		# tempDir = each.split(" ")[0]
		# 		tempDir = each.split(".crx")[0]
		# 		print(tempDir)
		# 		crx_unpack.unpack(crxDirectory+each, ext_dir=outDirectory + tempDir, encoding = "ISO-8859-1")
		# 		counter += 1
		# 	except :
		# 		continue
	print(counter)

def zipsBeautifier(beautifyDirectory):
	errorCount = 0
	progressCounter = 0
	length = len(os.listdir(beautifyDirectory))
	for directory, subdirectories, files in os.walk(beautifyDirectory):
		for file1 in files:
			if(file1.endswith(".js")):
				try:
					# print(os.path.join(directory, file1))
					res = jsbeautifier.beautify_file( os.path.join(directory, file1) )
					with open(os.path.join(directory, file1), "w+") as f1:
						f1.write(res)
				except ValueError:
					print("ValueError")
					errorCount += 1
				except IndexError:
					print("IndexError")
					errorCount += 1					
		progressCounter += 1
		print(" Progress " + str(progressCounter) + "out of " + str(length))
	print("ErrorCount from ERRORs = " + str(errorCount))


def jsonBeautify(jsonDirectory):
	for directory, subdirectories, files in os.walk(jsonDirectory):
			for file1 in files:
					if(file1.endswith(".json")):
							f1 = os.path.join(directory, file1)
							os.system("python -mjson.tool " + str(os.path.join(directory, file1)) + ' >> ' + str(f1))


def renameDir(inputDir):
    for folder in os.listdir(inputDir):
        if( (not (folder.endswith('.zip'))) & (len(str(folder).split(' ')) > 1 )   ):
            afterSpace = str(folder).split(' ')[1]
            first = afterSpace.split(':')[0]
            second = afterSpace.split(':')[1]
            third = afterSpace.split(':')[2]
            oldString = inputDir + '/' + str(folder).split(' ')[0] + '\ ' + first + '\:' + second + '\:' + third
            newString = inputDir + '/' + str(folder).replace(' ', '_')
            print("oldstring = " + str(oldString))
            print("newstring = " + str(newString))
            command = "mv " + str(oldString) + " " + str(newString)
            print(command)
            os.system(command)


def beautifySingleFile(beautifyFile):
	opts = jsbeautifier.default_options()
	opts.brace_style = "expand"
	res = jsbeautifier.beautify_file(beautifyFile, opts)
	f1 = open(beautifyFile, "w+")
	f1.write(res)	

def countDiffs(dcmp, counter):
	for name in dcmp.diff_files:
		counter += 1
	for sub_dcmp in dcmp.subdirs.values():
		counter += countDiffs(sub_dcmp, counter)
	print(counter)
	return counter

def extractAllHidsFromDirectory():
	inputDir = "scoreByExtensionHid1OutputNegativeOnly"
	outFile = open("./hulkFIles/allHidsToExtract.txt", "w+")
	for each in os.listdir(inputDir):
		outFile.write(each.split(".crx")[0] + '\n')

if __name__ == '__main__':
	main()
