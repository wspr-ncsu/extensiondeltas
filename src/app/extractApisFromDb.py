import mongoExtensionsAST as mongo
import difflib
import logging
import sys
import crx_unpack
import os 
import itertools
import subprocess
from Naked.toolshed.shell import execute_js, muterun_js
import re
#sudo python3 tool.py checkout  2fa4ee555b8b5b382d68e1118ab7e6eac293a039

# apiList = ["localStorage.setItem", "localStorage.getItem", "document.createElement",
# "document.write", "tabs.executeScript", "chrome.tabs.executeScript", "xhr", 
# "XMLHttpRequest", "innerHTML", "createElement", "window.location.replace",
# "googleTag.defineSlot.addService", "addEventListener", "window.addEventListener",
# "storage.local.set", "storage.local.get", "storage.sync.set", "storage.sync.get",
# "chrome.storage.local.set", "document.cookie", "cookies.getAll", "history.search",
# "history.getVisits", "bookmarks.getTree", "management.getAll", "downloads.download", 
# "runtime.sendMessage", "tabs.sendMessage", "runtime.onMessage.addListener", 
# "runtime.onConnect.addListener", "runtime.connect"]

lengths = [2, 2, 2, 2, 2, 3, 1, 1, 1, 1, 3, 3, 1, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2]
apiListThird = ["''", "''", "''", "''", "''", 'chrome', "''", "''", "''", "''", 'window', 'googleTag', "''", "''", 'storage', 'storage', 'storage', 'storage', "''", "''", "''", "''", "''", "''", "''", "''", "''", 'runtime', 'runtime', "''"]
apiListSecond = ['localStorage', 'localStorage', 'document', 'document', 'tabs', 'tabs', "''", "''", "''", "''", 'location', 'defineSlot', "''", 'window', 'local', 'local', 'sync', 'sync', 'document', 'cookies', 'history', 'history', 'bookmarks', 'management', 'downloads', 'runtime', 'tabs', 'onMessage', 'onConnect', 'runtime']
apiListFirst = ['setItem', 'getItem', 'createElement', 'write', 'executeScript', 'executeScript', 'xhr', 'XMLHttpRequest', 'innerHTML', 'createElement', 'replace', 'addService', 'addEventListener', 'addEventListener', 'set', 'get', 'set', 'get', 'cookie', 'getAll', 'search', 'getVisits', 'getTree', 'getAll', 'download', 'sendMessage', 'sendMessage', 'addListener', 'addListener', 'connect']


# apiList = ["localStorage", "createElement", "executeScript", "xhr", "XMLHttpRequest",
# "innerHTML", "location", "addService", "addEventListener", "storage", "cookie", 
# "cookies", "history", "bookmarks", "management", "downloads", "download", 
# "SendMessage", "onMessage", "onConnect", "connect"]

def generalHandler(hid):
    # hid = "abocfhfdmbbafpioaijblfooiibicblo"
    # result = removeComments(open("./" + hid + "/initial/test_folder/test_file.js", "r").read())
    # print(result)
    # return
    initialDir = "./" + hid + "/initial"
    bothDir = "./" + hid + "/both"
    addsDir = "./" + hid + "/adds"
    removesDir = "./" + hid + "/removes"
    nodeDir = "./" + hid + "/node"
    nodeAddDir = "./" + hid + "/nodeAdd"
    nodeRemDir = "./" + hid + "/nodeRem"
    # testDir = "/media/nikos/fourTera1/homeA/oneFromCluster9_1/extracted"
    # testDir = "/media/nikos/fourTera1/homeA/testFoldToDel"

    # renameNamesLocalOnly(initialDir)
    createOnlyDirAndEmptyJS(hid)
    tempOutNameList = queryAndUnpack(hid)
    # logging.info("tempoutBaneList = ")
    # logging.info(tempOutNameList)
    # tempOutNameList = [initialDir + "/" + i for i in sorted(os.listdir(initialDir))]
    # print(tempOutNameList)
    # return
    createBothFolder(bothDir, tempOutNameList, hid)
    addRemoveFromBoth(bothDir, addsDir, removesDir)
    callAnalyzeCalled(addsDir, hid, nodeAddDir)
    callAnalyzeCalled(removesDir, hid, nodeRemDir)
    # countApi(nodeDir)
    countApi23Mod(nodeAddDir, nodeRemDir, hid)
    # addList = countApi23Mod(nodeAddDir, hid)
    # remList = countApi23Mod(nodeRemDir, hid)
    deleteDirectory(hid)

def renameNamesLocalOnly(initialDir):
    for ts1 in os.listdir(initialDir):
        ts = ts1.replace("-", '_')
        ts = ts.replace(":", '_')
        ts = ts.replace(" ", '_')
        ts = ts.replace(".", '_')
        os.rename(initialDir + "/" + ts1, initialDir + "/" + ts)

def createOnlyDirAndEmptyJS(hid):
    if not os.path.exists("./" + hid):
        os.makedirs("./" + hid)
    outDirs = ["/initial", "/both", "/adds", "/removes", "/node", "/nodeAdd", "/nodeRem"]
    for outDirectory in outDirs:
        if not os.path.exists("./" + hid + outDirectory):
            os.makedirs("./" + hid + outDirectory)
    f = open("./" + hid + "/both/emptyFile.js", 'w+')
    f.close()

def queryAndUnpack(hid):
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    query = mongo.Queue.objects(hid=hid).order_by("ts")
    # outDir = "/home/npantel/data/"
    outDir = "./" + hid + '/initial/'
    # logging.info("query length = " + str(len(query)))
    tempOutNameList = []
    for ext in query:
        crx = ext.crx.read()
        '''
        to store the file as a crx
        '''
        ts = str(ext.ts).replace("-", '_')
        ts = ts.replace(":", '_')
        ts = ts.replace(" ", '_')
        ts = ts.replace(".", '_')
        crxOutName = outDir + "%s_%s.crx" % (ext.hid, ts)
        # if("encode" in dir(crx)):
        #     crx = crx.encode()
        with open(crxOutName, 'wb') as f:
            f.write(crx)
        '''
        unpack file and get all paths
        '''
        tempOutName = crxOutName.split(".crx")[0]
        crx_unpack.unpack(crxOutName, ext_dir=tempOutName)

        '''
        get all paths of a directory
        '''
        tempOutNameList.append(tempOutName)
        # pathsWalk = walkComplete(tempOutName)
        # logging.info(pathsWalk)
    return tempOutNameList

def createBothFolder(bothDir, tempOutNameList, hid):
    '''
    previous approach
    '''
    # for version1, version2 in pairwise(tempOutNameList):
    #     allFiles1 = walkComplete(version1)
    #     allFiles2 = walkComplete(version2)
    #     flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
    #     flat_list2 = [item for item in allFiles2 if item.endswith('.js')]
    '''
    end of previous approach
    '''
    '''
    new approach
    '''
    # logging.info(tempOutNameList)
    for version1, version2 in pairwise(tempOutNameList):
        allFiles1 = walkComplete(version1)
        allFiles2 = walkComplete(version2)
        flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
        flat_list2 = [item for item in allFiles2 if item.endswith('.js')]
        mainPart1 = version1
        mainPart2 = version2
        lastPart1 = ["/".join(n.split('/')[4:]) for n in flat_list1]
        lastPart2 = ["/".join(n.split('/')[4:]) for n in flat_list2]
        flat_list12 = list(set(lastPart1) - set(lastPart2))
        flat_list21 = list(set(lastPart2) - set(lastPart1))
        common12 = list(set(lastPart1) & set(lastPart2))
        parts1 = common12 + flat_list12 + ['None']*len(flat_list21)
        parts2 = common12 + ["None"]*len(flat_list12) + flat_list21
        flat_list1 = [mainPart1 + '/' + parts1Each for parts1Each in parts1]
        flat_list2 = [mainPart2 + '/' + parts2Each for parts2Each in parts2]
        '''
        end of my new approach
        '''
        # logging.info(flat_list2)
        for files1, files2 in itertools.zip_longest(flat_list1, flat_list2):
            if("None" in files1):
                f1String = 'None'
                files1 = './' + hid + "/both/emptyFile.js"
            else:
                f1String = str(files1.split('/')[-1])
            if("None" in files2):
                f2String = 'None'
                files2 = './' + hid + "/both/emptyFile.js"
            else:
                f2String = str(files2.split('/')[-1])
            filenameString = bothDir + '/' + str(version1.split('/')[-1]) + '_' + str(version2.split('/')[-1]) + '_' + f1String + '_' + f2String + '.js'             
            if len(str(filenameString)) > 272 :
                filenameString = filenameString[:272]
            with open(filenameString, 'w+') as outFile:
                diffExtraction(files1, files2, outFile)

def addRemoveFromBoth(inDir, addsDir, removesDir):
    # logging.info("both folder contains: " + str(len(os.listdir(inDir))))
    for file in sorted(os.listdir(inDir)):
        fOpen = open(inDir + '/' + file, 'r').readlines()
        # print(len(fOpen))
        # logging.info(fOpen)
        if(len(fOpen) > 0):
            # open plus and minus File
            plusFile = open(addsDir + '/' + file, 'w+')
            minusFile = open(removesDir + '/' + file, 'w+')
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
            # statinfo1 = os.stat('./allExtensionsAfterDiff/adds/' + file)
            # if(statinfo1.st_size == 0):
            #     os.system('rm -rf ./allExtensionsAfterDiff/adds/' + file )
            # statinfo2 = os.stat('./allExtensionsAfterDiff/removes/' + file)
            # if(statinfo2.st_size == 0):
            #     os.system('rm -rf ./allExtensionsAfterDiff/removes/' + file )

def callAnalyzeCalled(inDir, hid, outDir):
    # logging.info("on adds folder there are: " + str(len(os.listdir(inDir))))
    inDirList = os.listdir(inDir)
    for each in inDirList:
        # print("File = %s" % each)
        # subprocess.call(["node", "analyzeCalled.js", inDir+'/'+each, each, hid])
        execute_js('analyzeCalled.js ' + inDir+'/'+each + ' ' + each + ' ' + hid + ' ' + outDir)

def countApi(nodeDir):
    d = {key:0 for key in apiList} 
    # logging.info("node folder has: " + str(len(os.listdir(nodeDir))))
    for eachFile in os.listdir(nodeDir):
        apiFreqs = []
        apiSeq = open(nodeDir + '/' + eachFile, 'r').read().split(',')
        for api in apiSeq:
            if api in apiList:
                d[api] += 1
        for key in d:
            apiFreqs.append(d[key])
        dTable = mongo.apiFreqStorage(name = eachFile, apiFreqs = apiFreqs)
        dTable.save()

def countApi23Mod(node1Dir, node2Dir, hid):
    # d = {key:0 for key in apiListFirst}
    d = [0]*len(apiListFirst)
    # logging.info("node folder has: " + str(len(os.listdir(nodeDir))))
    for eachFile in os.listdir(node1Dir):
        if("None" not in eachFile):
            bothApiFreqs = []
            bothSum0 = []
            for nodeDir in [node1Dir, node2Dir]:
                failed = []
                apiFreqs = []
                apiSeq = open(nodeDir + '/' + eachFile, 'r').read().split(',')
                if(len(apiSeq) >= 3):
                    third = apiSeq[0]
                    second = apiSeq[1]
                    for api in apiSeq[2:]:
                        if api in apiListFirst:
                            i = apiListFirst.index(api)
                            if(lengths[i] == 1):
                                d[i] += 1
                            elif(lengths[i] == 2):
                                if(str(second) == str(apiListSecond[i])):
                                    d[i] += 1
                                else:
                                    failed.append(str(second) + "." + str(api))
                            elif(lengths[i] == 3):
                                if(str(second) == str(apiListSecond[i])):
                                    if(str(third) == str(apiListThird[i])):
                                        d[i] += 1
                                else:
                                    failed.append(str(third) + "." + str(second) + "." + str(api))
                        third = second
                        second = api
                else:
                    if(len(apiSeq) == 2):
                        failed = str(apiSeq[0]) + "." + str(apiSeq[1])
                    elif(len(apiSeq) == 1):
                        failed = str(apiSeq[0])
                sum0 = 0
                for each in d:
                    apiFreqs.append(each)
                    sum0 += each
                bothSum0.append(sum0)
                bothApiFreqs.append(apiFreqs)
            sumStore = max(bothSum0[0] - bothSum0[1], bothSum0[1] - bothSum0[0])
            apiFreqsStore = [max(add-rem, rem-add) for add,rem in zip(bothApiFreqs[0], bothApiFreqs[1])]
            apiFreqsStore = [1 if i>0 else 0 for i in apiFreqsStore]
            logging.info(apiFreqsStore)
            dTable = mongo.apiFreqStorageUpdOrderB(hid = hid, name = eachFile, apiFreqsUpdated = apiFreqsStore, apiFreqsNew = [], sum0 = sumStore, failed = failed)
            dTable.save()
        else:
            bothApiFreqs = []
            bothSum0 = []
            # if(eachFile.split("None")[-1] == ".js"):
            #     nodeDirs = node1Dir
            # else:
            #     nodeDirs = node2Dir
            for nodeDir in node1Dir:
                failed = []
                apiFreqs = []
                apiSeq = open(nodeDir + '/' + eachFile, 'r').read().split(',')
                if(len(apiSeq) >= 3):
                    third = apiSeq[0]
                    second = apiSeq[1]
                    for api in apiSeq[2:]:
                        if api in apiListFirst:
                            i = apiListFirst.index(api)
                            if(lengths[i] == 1):
                                d[i] += 1
                            elif(lengths[i] == 2):
                                if(str(second) == str(apiListSecond[i])):
                                    d[i] += 1
                                else:
                                    failed.append(str(second) + "." + str(api))
                            elif(lengths[i] == 3):
                                if(str(second) == str(apiListSecond[i])):
                                    if(str(third) == str(apiListThird[i])):
                                        d[i] += 1
                                else:
                                    failed.append(str(third) + "." + str(second) + "." + str(api))
                        third = second
                        second = api
                else:
                    if(len(apiSeq) == 2):
                        failed = str(apiSeq[0]) + "." + str(apiSeq[1])
                    elif(len(apiSeq) == 1):
                        failed = str(apiSeq[0])
                sum0 = 0
                for each in d:
                    apiFreqs.append(each)
                    sum0 += each
                bothSum0.append(sum0)
                bothApiFreqs.append(apiFreqs)
            sumStore = bothSum0[0]
            apiFreqsStore = bothApiFreqs[0]
            apiFreqsStore = [1 if i>0 else 0 for i in apiFreqsStore]
            dTable = mongo.apiFreqStorageUpdOrderB(hid = hid, name = eachFile, apiFreqsUpdated = [], apiFreqsNew = apiFreqsStore, sum0 = sumStore, failed = failed)
            dTable.save()

def deleteDirectory(hid):
    subprocess.call(["rm", "-rf", "./" + hid])
    
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

def diffExtraction(fromfile, tofile, outFile):
    # with open(fromfile, 'rw', encoding="ISO-8859-1") as f:
    #     fromlines = f.read()
    #     fromlines = removeComments(fromlines)
    #     f.write(fromlines)
    #     # fromlines = f.readlines()
    #     # fromlines = removeComments("\n".join(fromlines)).split("\n")
    # with open(tofile, 'rw', encoding="ISO-8859-1") as f:
    #     tolines = f.read()
    #     tolines = removeComments(tolines)
    #     f.write(tolines)
    # with open(fromfile, 'r', encoding="ISO-8859-1") as f:
    #     fromlines = f.read()
    #     fromlines = removeComments(fromlines)
    # with open(fromfile, 'w', encoding="ISO-8859-1") as f:
    #     f.writelines(fromlines)
    with open(fromfile, 'r', encoding="ISO-8859-1") as f:
        fromlines = f.readlines()        
    # with open(tofile, 'r', encoding="ISO-8859-1") as f:
    #     tolines = f.read()
    #     tolines = removeComments(tolines)
    # with open(tofile, 'w', encoding="ISO-8859-1") as f:
    #     f.writelines(tolines)
    with open(tofile, 'r', encoding="ISO-8859-1") as f:
        tolines = f.readlines()   
        # tolines = f.readlines()
        # tolines = removeComments("\n".join(tolines)).split("\n")
    # logging.info("fromlines = ")
    # logging.info(fromlines)
    # logging.info("tolines = ")
    # logging.info(tolines)    
    # diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate)
    # print(fromfile)
    # print(tofile)
    diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile)
    # diff = removeComments(str(diff))
    # logging.info("diff = ")
    # for line in diff:
    #     logging.info(line)  
    outFile.writelines(diff)

# def removeComments(string):
#     string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurrences streamed comments (/*COMMENT */) from string
#     string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurrence single-line comments (//COMMENT\n ) from string
#     return string

def removeComments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)    
