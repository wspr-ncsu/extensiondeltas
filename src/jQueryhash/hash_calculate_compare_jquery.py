'''
How to get all jquery versions
svn export https://github.com/cdnjs/cdnjs.git/trunk/ajax/libs/jquery

Results:
matches hashes of query:
33890

not-matched hashes of query:
187228
'''

import os
import hashlib
import mongo
import crx_unpack
import subprocess
import json

dHidsG = {}
dHidsB = {}
dHashesG = {}
dHashesB = {}
dHashNamesG = {}
dHashNamesB = {}

def main():
    hashes = initialHashes()
    # gatherHidsFromAllapib()
    allQueryFiles(hashes)
    # matchToHashes()

def initialHashes():
    allFiles1 = walkComplete('./jquery')
    flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
    returnHashes = []
    for file in flat_list1:
        with open(file, 'r') as fIn:
            hashable = fIn.read().strip(' ').strip('\n').encode()
            result = hashlib.md5(hashable)
        print(result.digest())
        returnHashes.append(result.digest())
    return returnHashes


def walkComplete(path1):
    returnList = []
    for directory, subdirectories, files in os.walk(path1):
        for file1 in files:
            returnList.append(os.path.join(directory, file1))
    return returnList

def gatherHidsFromAllapib():
    query0 = mongo.allapib.objects()
    query1 = [each for each in query0 if 'jquery' in each.name]
    hidList = []
    names = []
    for each in query1:
        if each.hid not in hidList:
            hidList.append(each.hid)
        # check1or2Part(each.name)
        if each.name.split('_')[-2:-1] not in names:
            names.append(each.name.split('_')[-2:-1])
    print(hidList)
    print(names)
    print(len(hidList))
    print(len(names))
    return (hidList, names)

def allQueryFiles(hashes):
    # from hids gathered in function "gatherHidsFromAllapib()"
    # call queryAndUnpack(hid)
    # and hash file after you extract it locally, path found also from "gatherHidsFromAllapib()"
    hids = open('./queryDetected.txt', 'r').readlines()[0].replace('[', '').replace(']', '').replace(' ', '').replace('\'', '').replace('\"', '').replace('\n', '').split(',')
    print(hids)
    cntPos = 0
    cntNeg = 0
    cnt = 0
    for hid in hids:
        print(cnt)
        cnt += 1
        createOnlyDirAndEmptyJS(hid)
        tempOutNameList = queryAndUnpack(hid)
        # print(tempOutNameList)
        # walk directory
        # if any of the files contains 'query' in the filename
        # hash it and match it to the hash table
        # if yes add to yes table
        # if no add to no table
        for path in tempOutNameList:
            allFiles1 = walkComplete(path)
            flat_list1 = [item for item in allFiles1 if item.endswith('.js')]
            for file in flat_list1:
                if 'query' in file:
                    returnHash = calculateHashFromSourceFile(file)
                    returnHashS = str(returnHash)
                    if returnHash in hashes:
                        cntPos += 1
                        dHidsG[hid + '0'] = dHidsG.get(hid + '0', 0) + 1
                        dHashesG[returnHashS] = dHashesG.get(returnHashS, 0) + 1
                        if returnHashS in dHashNamesG.keys():
                            dHashNamesG[returnHashS].append(file)
                        else:
                            dHashNamesG[returnHashS] = [returnHashS]
                    else:
                        # print(returnHash)
                        # print(file)                        
                        cntNeg += 1
                        dHidsB[hid] = dHidsB.get(hid, 0) + 1
                        dHashesB[returnHashS] = dHashesB.get(returnHashS, 0) + 1
                        if returnHashS in dHashNamesB.keys():
                            dHashNamesB[returnHashS].append(file)
                        else:
                            dHashNamesB[returnHashS] = [returnHashS]                        
                            # print("neg = " + str(cntNeg))
        deleteDirectory(hid)
    # with open("dictionariesResults.txt", 'w') as outF:
    #     outF.write()
    print(cntNeg)
    print(cntPos)
    for i, name in enumerate([dHidsG, dHashesG, dHashNamesG]):
        writeJson(name, i, 'g')
    for i, name in enumerate([dHidsB, dHashesB, dHashNamesB]):
        writeJson(name, i, 'b')

def writeJson(name, i, firstLetter):
    json1 = json.dumps(name)
    f = open(firstLetter + str(i) + ".json","w")
    f.write(json1)
    f.close()
    # calculateHashFromSourceFile(file)


def queryAndUnpack(hid):
    query = mongo.Queue.objects(hid=hid).order_by("ts")
    outDir = "./" + hid + '/initial/'
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
        '''
        actually write the file
        '''
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

def deleteDirectory(hid):
    subprocess.call(["rm", "-rf", "./" + hid])

def calculateHashFromSourceFile(file):
    with open(file, 'r') as fIn:
        try:
            hashable = fIn.read().strip(' ').strip('\n').encode()
        except UnicodeDecodeError:
            print(file)
            # error:
            # 'utf-8' codec can't decode byte 0xe1 in position 2977: invalid continuation byte
            hashable = fIn.read().strip(' ').strip('\n').encode("utf-8", "ignore")
        result = hashlib.md5(hashable)
    # print(result.digest())
    return result.digest()

def createOnlyDirAndEmptyJS(hid):
    if not os.path.exists("./" + hid):
        os.makedirs("./" + hid)
    outDirs = ["/initial"]
    for outDirectory in outDirs:
        if not os.path.exists("./" + hid + outDirectory):
            os.makedirs("./" + hid + outDirectory)


if __name__ == '__main__':
    main()