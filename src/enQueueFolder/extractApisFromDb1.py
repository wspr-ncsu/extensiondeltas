'''
here:
    sudo docker build -t astomp3:latest ./astcomparetest1/
    sudo docker tag astomp3 localhost:5000/npantel-astcomp
    sudo docker push localhost:5000/npantel-astcomp

kubernetes:

    for redis:
    kubectl create -f queued-redis-deployment.yaml
    kubectl port-forward service/npantel-redis-test 9000:6379
    (NOT THIS ONE)kubectl create -f queued-redis-service.yaml

for project:
    kubectl apply -f deploy-exitd-demo.yaml
    kubectl get pods (get __NAME__ here)
    kubectl logs __NAME__
'''

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
from string import ascii_lowercase

# apiList = ["localStorage", "createElement", "executeScript", "xhr", "XMLHttpRequest",
# "innerHTML", "location", "addService", "addEventListener", "storage", "cookie", 
# "cookies", "history", "bookmarks", "management", "downloads", "download", 
# "SendMessage", "onMessage", "onConnect", "connect"]


# insert combinedList
def generalHandler(hid, combList):
    initialDir = "./" + hid + "/initial"
    bothDir = "./" + hid + "/both"
    addsDir = "./" + hid + "/adds"
    removesDir = "./" + hid + "/removes"
    nodeDir = "./" + hid + "/node"
    nodeAddDir = "./" + hid + "/nodeAdd"
    nodeRemDir = "./" + hid + "/nodeRem"
    createOnlyDirAndEmptyJS(hid)
    tempOutNameList = queryAndUnpack(hid)
    createBothFolder(bothDir, tempOutNameList, hid)
    addRemoveFromBoth(bothDir, addsDir, removesDir)    
    presentOrNot(addsDir, hid, combList)
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
        with open(crxOutName, 'wb') as f:
            if crx:
                f.write(crx)
            else:
                continue
        '''
        unpack file and get all paths
        '''
        tempOutName = crxOutName.split(".crx")[0]
        crx_unpack.unpack(crxOutName, ext_dir=tempOutName)

        '''
        get all paths of a directory
        '''
        tempOutNameList.append(tempOutName)
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
        # logging.info(fOpen)
        if(len(fOpen) > 0):
            # open plus and minus File
            plusFile = open(addsDir + '/' + file, 'w+')
            minusFile = open(removesDir + '/' + file, 'w+')
            for line in fOpen:
                if(len(line) >= 3):
                    if( (line[0] == '+') & (line[2] != '+') ):
                        plusFile.write(line[1:])
                    elif( (line[0] == '-') & (line[2] != '-')):
                        minusFile.write(line[1:])
            plusFile.close()
            minusFile.close()

def presentOrNot(inDir, hid, combList):
    inDirList = os.listdir(inDir)
    d = [0]*len(combList)
    for eachFile in inDirList:
        with open(inDir + '/' + eachFile) as fp:
            fpRead = fp.readlines()
            for i, api in enumerate(combList):
                d[i] = next((1 for line in fpRead if api in line), 0)
        # TODO: TOCHANGE: ONLY FOR 30 APIS
        dTable = mongo.allapia(hid = hid, name = eachFile, apiFreqsAll = d, sumAll = sum(d))
        # TODO: TOCHANGE: For ALL APIS
        # dTable = mongo.allapib(hid = hid, name = eachFile, apiFreqsAll = d, sumExt = sum(d[:970]), sumOther = sum(d[970:]), sumAll = sum(d))
        dTable.save()

def callAnalyzeCalled(inDir, hid, outDir):
    # logging.info("on adds folder there are: " + str(len(os.listdir(inDir))))
    inDirList = os.listdir(inDir)
    for each in inDirList:
        # print("File = %s" % each)
        # subprocess.call(["node", "analyzeCalled.js", inDir+'/'+each, each, hid])
        execute_js('analyzeCalled.js ' + inDir+'/'+each + ' ' + each + ' ' + hid + ' ' + outDir)

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
    with open(fromfile, 'r', encoding="ISO-8859-1") as f:
        fromlines = f.readlines()        
    with open(tofile, 'r', encoding="ISO-8859-1") as f:
        tolines = f.readlines()   
    diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile)
    outFile.writelines(diff)

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

def unique(list1):
    uniqueList = []
    # uniqueList = [k for k in list1 if k not in uniqueList.append(k)]
    for each in list1:
        if each not in uniqueList:
            uniqueList.append(each)
    return uniqueList

# if __name__=="__main__":
#     main()