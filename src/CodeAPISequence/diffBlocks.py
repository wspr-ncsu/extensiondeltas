""" Command line interface to difflib.py providing diffs in four formats:

* ndiff:    lists every line and highlights interline changes.
* context:  highlights clusters of changes in a before/after format.
* unified:  highlights clusters of changes in an inline format.
* html:     generates side by side comparison with change highlights.

"""

import sys, os, time, difflib, optparse
import itertools
from pprint import pprint
import csv
import re

def main():
    # for every extension, for every version, for every file, extract both adds and removes
    # inDir = './allExtensionsBeforeDiff'
    inDir = '/media/nikos/fourTera1/homeA/manyCrxFiles/extracted'
    # extractHashes(inDir)

    # rename all files, replacing spaces with underscores
    # inDir = '/media/nikos/fourTera1/homeA/bfbameneiokkgbdmiekhjnmfkcnldhhm/extracted'    
    # renameDir(inDir)
    # extract all hash1 
    # eachExtractHid(inDir)


    inDir = '/media/nikos/fourTera1/homeA/manyCrxFiles/extracted'
    # createBothFolder(inDir)
    # TODO: distinguish from both to adds and removes
    # ADDREMOVE FUNCTION
    inDir = './allExtensionsAfterDiff/both'
    # addRemove(inDir)
    
    # test default diff
    # defaultDiff()

    # defaultDiff2()

    # how to compare each hash with all other extensions
    hashesInputCsvFile = './allExtensionsAfterDiff/hash1/hash1File.csv'
    # compareHashes1(hashesInputCsvFile)

    # TODO: remove comments sections
    # TODO: check html for unsafe-inline script
    # check which types of script injection exist

    # injectInputFile = open('./scriptTypes.txt', 'r').readlines()
    inDir = './allExtensionsAfterDiff/SequenceAPI'
    # injectScriptTypes(injectInputFile, inDir)


    # LCS in APIs
    inDir = './allExtensionsAfterDiff/SequenceAPI'
    # specialLCSHandler(inDir)
    inDir = './allExtensionsAfterDiff/SequenceAPI'
    outDir = './allExtensionsAfterDiff/SequenceAPIUnobfuscated'
    eliminateObfuscation(inDir, outDir)

def eliminateObfuscation(inDir, outDir):
    counter = 0
    for each in os.listdir(inDir):
        listToBeWritten = []
        with open(inDir + '/' + str(each), 'r') as inFile:
            for eachApi in inFile.read().split(','):
                # print(eachApi)
                if(re.match(r'^[a-zA-Z]{1,2}$', eachApi)):
                    # print(eachApi)
                    listToBeWritten.append('a')
                else:
                    listToBeWritten.append(eachApi)
        with open(outDir + '/' + str(each), 'w+') as outFile:
            for listPart in listToBeWritten:
                outFile.write(listPart + ',')
        counter += 1
        print(str(counter) + "out of 315k")
        
def specialLCSHandler(inDir):
    LcsDir = {}
    lengths = []
    counter = 0 
    # create queue

    for each1 in os.listdir(inDir):
        statinfo1 = os.stat(inDir + '/' + str(each1))
        if(statinfo1.st_size < 1000000):        
            for each2 in os.listdir(inDir):
                statinfo2 = os.stat(inDir + '/' + str(each2))
                if(statinfo2.st_size < 1000000): 
                    if(each1 != each2):
                        newLength = specialLCS(each1, each2)
                        lengths.append(newLength)
                counter += 1 
                print(str(counter) + "out of 90000000000")
    print(len(length))

    # higher level abstraction
    # sgeneralLCS()


def injectScriptTypes(inFile, inputDir):
    injectTypeDict = {}
    for each in inFile:
        each = each.split('\n')[0]
        injectTypeDict[each] = 0
    print(injectTypeDict)
    injectTypes = inFile
    # print(len(injectTypes))
    counter = 0
    for file in sorted(os.listdir(inputDir)):
        eachFile = open(inputDir + '/' + file, 'r').read()
        eachApi = eachFile.split(',')
        # print(len(eachApi))
        for eachApi1 in eachApi:
            for eachInject in injectTypes:
                eachInject = eachInject.split('\n')[0]
                # print(eachApi1)
                if(eachInject == eachApi1) & (len(eachInject) > 0):
                    print("type = " + str(eachInject) + " and file = " + str(file))
                    injectTypeDict[eachInject] += 1
    print(injectTypeDict)

def createBothFolder(inputDir):
    rootDirectoriesList = []
    for rootDirectories in sorted(os.listdir(inputDir)):
        rootDirectoriesList.append(rootDirectories)

    rootDirectoriesHids = deduplicate(rootDirectoriesList)

    newList = [[x for x in rootDirectoriesList if (str(x).split('-')[0] == str(hid))] for hid in rootDirectoriesHids]


    # INITIALIZE HASH FILE
    # allhashes1FileString = './allExtensionsAfterDiff/hash1/hash1File.csv'

    # for every extension, for every version, for every file
    # get counter to see progress
    length = len(newList)
    counter = 0
    for extension in newList:
        for version1, version2 in pairwise(extension):
            # try:
            # print(version1 + '\t' + version2)
            allFiles1 = walkComplete(inputDir + '/' + version1)
            allFiles2 = walkComplete(inputDir + '/' + version2)
            flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
            flat_list2 = [item for item in allFiles2 if item.endswith('.js')]
            for files1, files2 in itertools.zip_longest(flat_list1, flat_list2):
                if(files1 is None):
                    f1String = 'None'
                    files1 = './emptyFile.js'
                else:
                    f1String = str(files1.split('/')[-1])
                if(files2 is None):
                    f2String = 'None'
                    files2 = './emptyFile.js'
                else:
                    f2String = str(files2.split('/')[-1])
                # TODO: CHANGE HERE FROM CODE DIFF TO AST DIFF
                filenameString = './allExtensionsAfterDiff/both/' + str(version1) + '_' + str(version2) + '_' + f1String + '_' + f2String + '.js'             
                # print(len(str(filenameString)))
                if len(str(filenameString)) > 272 :
                    filenameString = filenameString[:272]
                with open(filenameString, 'w+') as outFile:
                    diffExtraction(files1, files2, outFile)
            # except UnicodeDecodeError:
            #     print('Unicode Error\n')
        counter += 1
        print(str(counter) + "/" + str(length))


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

def eachExtractHid(inputDir):
    allhashes1FileString = './allExtensionsAfterDiff/hash1/hash1File.csv'

    for extension in sorted(os.listdir(inputDir)):
        # print(inputDir + '/' + extension)
        # return
        # traverse each directory to find all ".js" files
        allFiles1 = walkComplete(inputDir + '/' + extension)
        flat_list1 = [item for item in allFiles1 if item.endswith('.js')]

        # print(flat_list1[0:3])
        # return
        for files1 in flat_list1:
            # print(files1)
            # WRITE HID
            allhashes1File = open(allhashes1FileString, 'a')
            #get HID function
            myHid = getHid(inputDir + '/' + extension)
            allhashes1File.write(myHid)
            allhashes1File.write('\t')
            
            # os.system('node analyze.js ' + files2 + ' >> ' + outFile2)
            # WRITE NEWLINE
            # allhashes1File.write('\n')
            # os.system('echo \'\n\' >> ' + allhashes1FileString)
            allhashes1File.close()            
            os.system('node analyze.js ' + files1 + ' >> ' + allhashes1FileString)               
            # os.system('echo \'\t\' >> ' + allhashes1FileString)


        # # REPEAT FOR VERSION2
        # # WRITE HASH
        # os.system('node analyze.js ' + files1 + ' >> ' + allhashes1FileString)                
        # os.system('echo -e \'\t\' >> ' + allhashes1FileString)
        # # WRITE HID
        # allhashes1File = open(allhashes1FileString, 'a')
        # #get HID function
        # myHid = getHid(version2)
        # allhashes1File.write(myHid)
        # allhashes1File.close()
        # # WRITE NEWLINE
        # os.system('echo \n >> ' + allhashes1FileString)


def extractHashes(inputDir):    
    rootDirectoriesList = []
    for rootDirectories in sorted(os.listdir(inputDir)):
        rootDirectoriesList.append(rootDirectories)

    rootDirectoriesHids = deduplicate(rootDirectoriesList)

    newList = [[x for x in rootDirectoriesList if (str(x).split('-')[0] == str(hid))] for hid in rootDirectoriesHids]


    # INITIALIZE HASH FILE
    allhashes1FileString = './allExtensionsAfterDiff/hash1/hash1File.csv'

    # for every extension, for every version, for every file
    for extension in newList:
        for version1, version2 in pairwise(extension):
            print(version1 + '\t' + version2)
            allFiles1 = walkComplete(inputDir + '/' + version1)
            allFiles2 = walkComplete(inputDir + '/' + version2)
            flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
            flat_list2 = [item for item in allFiles2 if item.endswith('.js')]
            for files1, files2 in itertools.zip_longest(flat_list1, flat_list2):
                if(files1 is None):
                    f1String = 'None'
                    files1 = './emptyFile.js'
                else:
                    f1String = str(files1.split('/')[-1])
                if(files2 is None):
                    f2String = 'None'
                    files2 = './emptyFile.js'
                else:
                    f2String = str(files2.split('/')[-1])
                # TODO: CHANGE HERE FROM CODE DIFF TO AST DIFF                  
                # outFile = open('./allExtensionsAfterDiff/both/' + str(version1) + '_' + str(version2) + '_' + f1String + '_' + f2String + '.js', 'w+')             
                # diffExtraction(files1, files2, outFile)
                outFile1 = './allExtensionsAfterDiff/ast/' + str(version1) + '_' + f1String + '.ast'
                outFile2 = './allExtensionsAfterDiff/ast/' + str(version2) + '_' + f2String + '.ast'

                # DO FOR VERSION 1
                # WRITE HASH                
                # os.system('node analyze.js ' + files1 + ' >> ' + outFile1)
                os.system('node analyze.js ' + files1 + ' >> ' + allhashes1FileString)               
                os.system('echo -e \'\t\' >> ' + allhashes1FileString)
                # WRITE HID
                allhashes1File = open(allhashes1FileString, 'a')
                #get HID function
                myHid = getHid(version1)
                allhashes1File.write(myHid)
                allhashes1File.close()
                # os.system('node analyze.js ' + files2 + ' >> ' + outFile2)
                # WRITE NEWLINE
                os.system('echo \n >> ' + allhashes1FileString)

                # REPEAT FOR VERSION2
                # WRITE HASH
                os.system('node analyze.js ' + files1 + ' >> ' + allhashes1FileString)                
                os.system('echo -e \'\t\' >> ' + allhashes1FileString)
                # WRITE HID
                allhashes1File = open(allhashes1FileString, 'a')
                #get HID function
                myHid = getHid(version2)
                allhashes1File.write(myHid)
                allhashes1File.close()
                # WRITE NEWLINE
                os.system('echo \n >> ' + allhashes1FileString)

def walkComplete(path1):
    returnList = []
    for directory, subdirectories, files in os.walk(path1):
        for file1 in files:
            returnList.append(os.path.join(directory, file1))
    return returnList

def diffExtraction(fromfile, tofile, outFile):

    fromdate = time.ctime(os.stat(fromfile).st_mtime)
    todate = time.ctime(os.stat(tofile).st_mtime)
    with open(fromfile, 'r', encoding="ISO-8859-1") as f:
        fromlines = f.readlines()
    with open(tofile, 'r', encoding="ISO-8859-1") as f:
        tolines = f.readlines()

    # diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate)
    print(fromfile)
    print(tofile)
    diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile)   
    outFile.writelines(diff)

def deduplicate(iterable):
    seen = set()
    for element in iterable:
        element1 = str(element).split('-')[0]
        if element1 not in seen:
            seen.add(element1)
    return sorted(seen)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def addRemove(inDir):
    # TODO: maybe remove sorted from here
    # count = 0
    # TODO: remove comments!
    # TODO: Does esprima remove comments?
    for file in sorted(os.listdir(inDir)):
        fOpen = open(inDir + '/' + file, 'r').readlines()
        # print(len(fOpen))
        if(len(fOpen) > 0):
            # open plus and minus File
            plusFile = open('./allExtensionsAfterDiff/adds/' + file, 'w+')
            minusFile = open('./allExtensionsAfterDiff/removes/' + file, 'w+')
            # plus = False
            # minus = False        
            # for line in fOpen[2:]:
            # print(fOpen[1])
            # print(file)
            for line in fOpen:
                if(len(line) >= 3):
                    if( (line[0] == '+') & (line[2] != '+') ):
                        plusFile.write(line[1:])
                        # plusFile.write('\n')
                        # plus = True
                        # minus = False
                    elif( (line[0] == '-') & (line[2] != '-')):
                        minusFile.write(line[1:])
                        # minusFile.write('\n')
                        # minus = True
                        # plus = False
                    # elif(plus):
                    #     plusFile.write(line)
                    # else:
                    #     minusFile.write(line)
            plusFile.close()
            minusFile.close()
            statinfo1 = os.stat('./allExtensionsAfterDiff/adds/' + file)
            if(statinfo1.st_size == 0):
                os.system('rm -rf ./allExtensionsAfterDiff/adds/' + file )
            statinfo2 = os.stat('./allExtensionsAfterDiff/removes/' + file)
            if(statinfo2.st_size == 0):
                os.system('rm -rf ./allExtensionsAfterDiff/removes/' + file )
    # print(count)


def defaultDiff():
     # Configure the option parser
    usage = "usage: %prog [options] fromfile tofile"
    parser = optparse.OptionParser(usage)
    parser.add_option("-c", action="store_true", default=False,
                      help='Produce a context format diff (default)')
    parser.add_option("-u", action="store_true", default=False,
                      help='Produce a unified format diff')
    hlp = 'Produce HTML side by side diff (can use -c and -l in conjunction)'
    parser.add_option("-m", action="store_true", default=False, help=hlp)
    parser.add_option("-n", action="store_true", default=False,
                      help='Produce a ndiff format diff')
    parser.add_option("-l", "--lines", type="int", default=3,
                      help='Set number of context lines (default 3)')
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)
    if len(args) != 2:
        parser.error("need to specify both a fromfile and tofile")

    n = options.lines
    fromfile, tofile = args # as specified in the usage string

    # we're passing these as arguments to the diff function
    fromdate = time.ctime(os.stat(fromfile).st_mtime)
    todate = time.ctime(os.stat(tofile).st_mtime)
    with open(fromfile, 'U') as f:
        fromlines = f.readlines()
    with open(tofile, 'U') as f:
        tolines = f.readlines()

    if options.u:
        diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile,
                                    fromdate, todate, n=n)
    elif options.n:
        diff = difflib.ndiff(fromlines, tolines)
    elif options.m:
        diff = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile,
                                            tofile, context=options.c,
                                            numlines=n)
    else:
        diff = difflib.context_diff(fromlines, tolines, fromfile, tofile,
                                    fromdate, todate, n=n)

    # we're using writelines because diff is a generator
    sys.stdout.writelines(diff)

def defaultDiff2():
    # text1 = open('./allExtensionsBeforeDiff/bccjjihdmolcgblhjmkdddnlcmbmjleh-2018-05-05/js/controller.js', 'r').read().splitlines(0)
    # text2 = open('./allExtensionsBeforeDiff/bccjjihdmolcgblhjmkdddnlcmbmjleh-2018-05-17/js/controller.js', 'r').read().splitlines(0)
    # text1 = open('./allExtensionsBeforeDiff/bccjjihdmolcgblhjmkdddnlcmbmjleh-2018-05-05/js/controller.js', 'r').readlines()
    text1 = open('/media/nikos/fourTera1/homeA/unlistedMine/extracted/controller1.js', 'r').readlines()
    # text2 = open('./allExtensionsBeforeDiff/bccjjihdmolcgblhjmkdddnlcmbmjleh-2018-05-17/js/controller.js', 'r').readlines()
    text2 = open('/media/nikos/fourTera1/homeA/unlistedMine/extracted/controller2.js', 'r').readlines()
    # d = difflib.Differ()
    # result = list(d.compare(text1, text2))
    # pprint(result)
    s = difflib.SequenceMatcher(None, text1, text2)
    # blocks = s.get_matching_blocks()
    # for block in blocks:
    #     pprint(text1[block])
    #     pprint('\n\n\n')
    #     pprint(text2[block])
    # pprint(blocks)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if(tag == 'replace'):
            print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, text1[i1:i2], text2[j1:j2]))        

def getHid(string):
    s1 = string.split('/')[-1]
    s2 = s1.split('-')[0]
    # print("Hid = " + str(s2))
    return s2

def compareHashes1(hashesInputCsvFile):
    # open files
    csvFile = open(hashesInputCsvFile, 'r')
    # read csv
    readCSV = csv.reader(csvFile, delimiter='\t')
    # initialize counters

    hashCnt = 0
    totalCnt = 0
    # countArray = [0 for i in range(sum(1 for row in readCSV))]
    print("len = " + str(range(sum(1 for row in readCSV))))
    csvFile.close()

    with open(hashesInputCsvFile, 'r') as csvFile:
        # read csv
        readCSV = csv.reader(csvFile, delimiter='\t')
        for one, two in itertools.combinations(readCSV, 2):
        # for one in readCSV:
        #     print(one)
        #     for two in readCSV:
            # print("l1 = ")
            # print(one[0])
            # print(" \n l2 = ")
            # print(two[0])
            # print("\n\n\n")
            if(str(one[0]) != str(two[0])):
                isEqual = compare(one[1], two[1])
                if(isEqual):
                    # print(hashCnt)
                    # countArray[hashCnt] += 1
                    totalCnt += 1
            hashCnt += 1
        # print(countArray)
        print(totalCnt)

def compare(l1, l2):
    if(str(l1) == str(l2)):
        return True
    else:
        return False


if __name__ == '__main__':
    main()
