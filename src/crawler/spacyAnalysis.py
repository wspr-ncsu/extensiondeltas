# import spacy
# import re
# import codecs
# from datetime import datetime, timedelta
# import pandas as pd
# import rpy2
# import numpy as np
# import scipy as sp
# from rpy2.robjects.packages import importr
# import rpy2.robjects as ro
# import rpy2.robjects as robjects
# from rpy2.robjects import r
# from rpy2.robjects.vectors import StrVector
# from rpy2.robjects.lib import grid
# import subprocess
# import locale
# import calendar
# import matplotlib.pyplot as plt
# from math import log
# import webbrowser
# import os
# import ast
# import itertools
from topia.termextract import extract

extractor.filter = extract.permissiveFilter
chrome_path = '/usr/bin/google-chrome %s'
FILESTRING = "./crawled/allReviews"
FILESTRING = "./crawled/concatReviews"
today = "Oct 20, 2018"
locale.setlocale(locale.LC_TIME, locale=None)

def keywordExtraction():
        keywordFile = "./keywordFile.txt"
        alldicts = {}
        keywords = open(keywordFile, 'r').readlines()
        for keyword in keywords:
            keyword = keyword.strip("\n")
            alldicts[keyword] = 0
        # FOR ONE FILE
        filename = "./crawled/concatReviews.txt"
        alldicts = analyzeFile(filename, keywordFile, alldicts)
        # for each in sorted(alldicts):
        #     print(each + '\t' + str(alldicts[each]))

def analyzeFile(filename, keywordFile, alldicts):
    dictionary = {}
    extensionsCountDictionary = {}
    # nlp = spacy.load('en')
    # UNCOMMENT AFTER *******
    # f1 = open(filename, 'r').readlines()
    # UNCOMMENT AFTER *******    
    keywords = open(keywordFile, 'r').readlines()
    for keyword in keywords:
        keyword = keyword.strip("\n")
        dictionary[keyword] = 0
        extensionsCountDictionary[keyword] = 0
    # count keywords in total
    # UNCOMMENT AFTER *******
    # for line in f1:
    #     keywords = open(keywordFile, 'r').readlines()
    #     for keyword in keywords:
    #         keyword = keyword.strip("\n")
    #         #add to dictionary
    #         if keyword.lower() in line.lower():
    #             dictionary[keyword] += 1
    #             alldicts[keyword] += 1
    # UNCOMMENT AFTER *******

    # count extensions for each keyword
    f2 = open(filename, 'r').read()
    blocks = re.split('-{41,}', f2)
    print("Found blocks = " + str(len(blocks)))
    count = 0
    # for block in blocks:  
    #     keywords = open(keywordFile, 'r').readlines()
    #     for keyword in keywords:
    #         keyword = keyword.strip("\n")
    #         #add to dictionary
    #         if keyword.lower() in block.lower():
    #             extensionsCountDictionary[keyword] += 1
    #     count += 1
    keywords = open(keywordFile, 'r').readlines()
    for keyword in keywords:
        keyword = keyword.strip("\n")
        #add to dictionary
        for block in blocks:  
            if keyword.lower() in block.lower():
                extensionsCountDictionary[keyword] += 1
        # print("BLOCKS = " + str(count) + "/" + str(len(blocks)))
    for each in sorted(extensionsCountDictionary):
        print(each + '\t' + str(extensionsCountDictionary[each]))
    return alldicts


def keywordExtractionAverage():
        keywordFile = "./keywordFile.txt"
        alldicts = {}
        keywords = open(keywordFile, 'r').readlines()
        for keyword in keywords:
            keyword = keyword.strip("\n")
            alldicts[keyword] = 0
        # FOR ONE FILE
        revFile = "./crawled/concatReviews.txt"
        scoreFile = "./crawled/concatScores.txt"
        alldicts = keywordAverageScore(revFile, scoreFile, keywordFile, alldicts)
        # for each in sorted(alldicts):
        #     print(each + '\t' + str(alldicts[each]))

def keywordAverageScore(revFile, scoreFile, keywordFile, alldicts):
    dictionary = {}
    extensionsCountDictionary = {}
    # nlp = spacy.load('en')
    # UNCOMMENT AFTER *******
    # f1 = open(filename, 'r').readlines()
    # UNCOMMENT AFTER *******    
    keywords = open(keywordFile, 'r').readlines()
    for keyword in keywords:
        keyword = keyword.strip("\n")
        dictionary[keyword] = 0
        extensionsCountDictionary[keyword] = 0

    countDictionary = {}
    for keyword in keywords:
        keyword = keyword.strip("\n")
        countDictionary[keyword] = 0

    # count extensions for each keyword
    fScore = open(scoreFile, 'r').read()
    fReview = open(revFile, 'r').read()
    scoresBlocks = re.split('\n-{41,}\n', fScore)
    reviewsBlocks = re.split('\n-{41,}\n', fReview)
    scoreCount = 0
    reviewCount = 0
    tempReviewCount = 0
    while scoreCount < len(scoresBlocks) -1:
        tempReviewCount = reviewCount  
        while( (reviewCount < (len(reviewsBlocks) -1) ) & (((scoresBlocks[scoreCount]).split('\n'))[0] != ((reviewsBlocks[reviewCount]).split('\n'))[0]) ):
            reviewCount += 1 
        if ((scoresBlocks[scoreCount]).split('\n'))[0] == ((reviewsBlocks[reviewCount]).split('\n'))[0]:
            for revLine, scoreLine in zip((reviewsBlocks[reviewCount]).split('\n')[1:len((scoresBlocks[scoreCount]).split('\n'))-1], (scoresBlocks[scoreCount]).split('\n')[1:]):
                for keyword in keywords:
                    keyword = keyword.strip("\n")
                    #add to dictionary
                    # print(revLine.lower())
                    if keyword.lower() in revLine.lower():
                        if(int(scoreLine.split('\t')[0]) > 0):
                            extensionsCountDictionary[keyword] += int(scoreLine.split('\t')[0])
                            countDictionary[keyword] += 1
        else:
            if(reviewsBlocks[reviewCount].split('//')[0] != 'https:'):
                reviewCount = 0
            else:
                reviewCount = tempReviewCount
        scoreCount += 1
        print(reviewCount)
        print(str(scoreCount) + '/~150k')
    for each in sorted(extensionsCountDictionary):
        print(each + '\t' + str(extensionsCountDictionary[each]/countDictionary[each]))
    return alldicts

def splitScoresByExtension():
    filename = "./crawled/concatScores.txt"
    allScores = open(filename, 'r').readlines()
    countDash=0
    countHttp=0
    countEmpty=0
    countScore=0
    for line in allScores:
        if ("-----------") in line:
            countDash +=1
        elif("https://chrome.google.com/webstore/detail/") in line:
            countHttp +=1
        elif line in ['\n', '\r\n']:
            countEmpty +=1
        else:
            countScore +=1
    print ("Scores = " + str(countScore) + "\nEmpties = " + str(countEmpty) + "\nHttps = " + str(countHttp) + "\nDashes = " + str(countDash) + '\n')

def splitReviewsByExtension():
    filename = "./crawled/concatReviews.txt"
    allScores = open(filename, 'r').readlines()
    countDash=0
    countHttp=0
    countEmpty=0
    countReview=0
    for line in allScores:
        if ("-----------") in line:
            countDash +=1
        elif("https://chrome.google.com/webstore/detail/") in line:
            countHttp +=1
        elif line in ['\n', '\r\n']:
            countEmpty +=1
        else:
            countReview +=1
    print("Scores = " + str(countReview) + "\nEmpties = " + str(countEmpty) + "\nHttps = " + str(countHttp) + "\nDashes = " + str(countDash) + '\n')

def forEachExtensionScore():
    scoreNamefile = './tempScores.txt'
    dateNamefile = './tempDates.txt'
    combNamefile = './tempComb.txt'
    filename = "./crawled/concatScores.txt"
    allScores = open(filename, 'r').read()
    bigCounter = 0     
    blocks = re.split('-{40,}', allScores)
    bins = np.zeros(7)
    bigBlocks = []
    cnt = 0
    new = 0
    for block in blocks:
        block = block.split('\n')
        if(len(block) > 50):
            bigCounter +=1
            bigBlocks.append(block) 
        #BINS
        if(len(block) < 5):
            bins[0] += 1
        elif(len(block) < 6):
            bins[1] += 1      
        elif(len(block) < 10):
            bins[2] += 1 
        elif(len(block) < 20):
            bins[3] += 1 
        elif(len(block) < 30):
            bins[4] += 1 
        elif(len(block) < 50):
            bins[5] += 1
        else:
            bins[6] += 1   
    print(bigCounter)

    # ******************************************************
    # # START OF PLOT NUMBER OF REVIEWS PER EXTENSION
    # *******************************************************
    # plt.close("all") 
    # bins = bins.astype(int)
    # # for i in range(len(bins)):
    #     # bins[i] = int(bins[i])
    # print(bins)
    # # bins = np.ones(7)
    # # bins.plt.hist()  
    # fig, ax = plt.subplots()
    # # bins = [log(bin,10) for bin in bins]
    # # bins = [log(bin,10) for bin in bins]
    # width = 0.8
    # binss = ['0', '1', '[2-5]', '[6-15]', '[16-25]', '[26-45]', '>45']
    # # binss = ['0', '1', '5', '15', '25', '45', '75']
    # # binss = [1,2,3,4,5,6,7]
    # ax.bar(binss, bins, width=width)
    # x = binss
    # y = bins
    # for a,b in zip(x, y):
    #     ax.text(a, b, str(b))
    # # ind = np.arange(len(bins))
    # # ax.barh(bins, ind, width, color="blue")
    # # plt.hist(np.transpose(bins), bins='auto')
    # # plot()
    # ax.set_yscale('log')
    # ax.set_xlabel('Intervals')
    # ax.set_ylabel('No. Extensions')

    # plt.show()        

    # ******************************************************
    # # END OF PLOT
    # ******************************************************

    #FOR EACH BLOCK
    scores = []
    dates = []
    newDates = []
    rCounter = 0
    for bigblock in bigBlocks:

        for line in bigblock:
            line = line.split("\t")
            if len(line) > 1 :
                scores.append(line[0])
                dates.append(line[1])
        for date in dates:
            if(date == 'None'):
                newDates.append('None')
            elif( ('hour' in str(date)) | ('minute' in str(date)) | ('hours' in str(date)) | ('minutes' in str(date))):
                newDates.append(today)
            elif('day' in date):
                daysBack = int(date.split(' ')[0])
                tday = pd.to_datetime(today)
                realDay = (tday - timedelta(days=daysBack))
            else:
                newDates.append(date)
        filScores = open(scoreNamefile, 'w+')
        filDates = open(dateNamefile, 'w+')
        # filComb = open(combNamefile, 'w+')
        filComb = open('./bigBlockScoresDates/' + str(bigblock[1].split('/')[-1]), 'w+')
        filComb.write('date\tScore\n')
        for score in scores:   
            filScores.write(str(score) + '\n')      
        for date in newDates:
            filDates.write(str(date) + '\n')  
        for (date,score) in zip(newDates,scores):
            date = date.replace(' ', '/')
            date = date.replace(',', '')
            if(len(date.split('/')) > 2):
                if(int(date.split('/')[1]) < 10):
                    date = date.split('/')[0] + '/' + '0' + date.split('/')[1] + '/' + date.split('/')[2]
            date = fixMonthName(date)
            filComb.write(date + '\t' + score + '\n')
        scores = []
        dates = []     
        rCounter += 1

def fixMonthName(date):
    switcher = {
        "Jan":  "01",
        "Feb":  "02",
        "Mar":  "03",
        "Apr":  "04",
        "May":  "05",
        "Jun":  "06",
        "Jul":  "07",
        "Aug":  "08",
        "Sep":  "09",
        "Oct":  "10",
        "Nov":  "11",
        "Dec":  "12" 
    }
    return (switcher[date.split('/')[0]] + '/' + date.split('/')[1] + '/' + date.split('/')[2] )

def date_to_nth_day(date, format='%b %d, %Y'):
    date = pd.to_datetime(date, format=format)
    new_year_day = pd.Timestamp(year=2009, month=1, day=1)
    return (date - new_year_day).days + 365*(date.year - new_year_day.year) + 1

def callRScripts():
    for eachFile in sorted(os.listdir('./bigBlockScoresDates')):
        cmd = "/home/nikos-ubuntu/miniconda2/envs/r-environment/bin/Rscript --vanilla ./MyrScript.r /home/nikos-ubuntu/Documents/PHD/malicious_extensions_fall_18_code/bigBlockScoresDates/" + str(eachFile) + ' ' + str(eachFile)
        p = subprocess.call(cmd, shell=True)

def countAnomaliesSize():
    directories = ["./plots/", "./minus10/", "./minus30/", "./percentMinus10/", "./percentMinus30/", "./percentMinus50/"]
    for directory in directories:
        outfile = open(directory + "output.txt", 'w+')
        a=[]
        for eachFile in sorted(os.listdir(directory)):
            fil = open(directory + str(eachFile)).readlines()
            a.append(len(fil)-1)
        a = sorted(a)
        outfile.write(str(dict((i, a.count(i)) for i in a)))

def allAnomOutput():
    number = "_11_28_18"
    directories = ["./plots/", "./minus10/", "./minus30/", "./percentMinus10/", "./percentMinus30/", "./percentMinus50/"]    
    allAnomOut = open("./anomalies_all_outputs" + number + ".txt", 'w+')
    allAnomOut.write("0\t1\t2-5\t6+\n")
    for directory in directories:
        dictionary = reading(directory + "output.txt")
        summation = sum(dictionary.values())
        sixOrMore = summation - (1 + dictionary[0] + dictionary[1] + dictionary[2] + dictionary[3] + dictionary[4] + dictionary[5] )
        allAnomOut.write(str(dictionary[0]) + "\t" + str(dictionary[1]) + "\t" + str(dictionary[2] + dictionary[3] + dictionary[4] + dictionary[5]) + "\t" + str(sixOrMore))
        allAnomOut.write("\t" + directory)
        allAnomOut.write('\n')


def reading(directory):
    whip = {}
    with open(directory, 'r') as f:
        s = f.read()
        whip = ast.literal_eval(s)
    return whip

def forEachGoogleExtension():
    scoreNamefile = './tempScores.txt'
    dateNamefile = './tempDates.txt'
    combNamefile = './tempComb.txt'
    filename = "./crawled/concatScores.txt"
    googleFile = "./matchingExtensionFiles/allChromeExtensionNames.txt"
    allScores = open(filename, 'r').read()
    googleOut = open("matchingExtensionFiles/googleFound.txt", 'w+')
    googleCounter = 0     
    blocks = re.split('-{40,}', allScores)
    bins = np.zeros(7)
    googleBlocks = []
    cnt = 0
    new = 0
    for block in blocks:
        block = block.split('\n')
        googleNameFile = open(googleFile, 'r').readlines()
        for googleName in googleNameFile:
            if( ( block[1].split('/')[-1] in googleName.split('/')[-1] ) & (len(block[1]) > 0)):
                googleCounter +=1
                googleBlocks.append(block)
                googleOut.write(block[1] + '\n')
        #BINS
        if(len(block) < 5):
            bins[0] += 1
        elif(len(block) < 6):
            bins[1] += 1      
        elif(len(block) < 10):
            bins[2] += 1 
        elif(len(block) < 20):
            bins[3] += 1 
        elif(len(block) < 30):
            bins[4] += 1 
        elif(len(block) < 50):
            bins[5] += 1
        else:
            bins[6] += 1   
    print(googleCounter)

    #FOR EACH BLOCK
    scores = []
    dates = []
    newDates = []
    rCounter = 0
    bigGoogle = 0
    for bigblock in googleBlocks:
        if(len(bigblock) > 40):
            bigGoogle += 1
        # TODO: IF BIGBLOCK IN GOOGLE
        # for line in bigblock:
        #     line = line.split("\t")
        #     if len(line) > 1 :
        #         scores.append(line[0])
        #         dates.append(line[1])
        # for date in dates:
        #     if(date == 'None'):
        #         newDates.append('None')
        #     elif( ('hour' in str(date)) | ('minute' in str(date)) | ('hours' in str(date)) | ('minutes' in str(date))):
        #         newDates.append(today)
        #     elif('day' in date):
        #         daysBack = int(date.split(' ')[0])
        #         tday = pd.to_datetime(today)
        #         realDay = (tday - timedelta(days=daysBack))
        #     else:
        #         newDates.append(date)
        # filScores = open(scoreNamefile, 'w+')
        # filDates = open(dateNamefile, 'w+')
        # # filComb = open(combNamefile, 'w+')
        # filComb = open('./bigBlockScoresDates/' + str(bigblock[1].split('/')[-1]), 'w+')
        # filComb.write('date\tScore\n')
        # for score in scores:   
        #     filScores.write(str(score) + '\n')      
        # for date in newDates:
        #     filDates.write(str(date) + '\n')  
        # for (date,score) in zip(newDates,scores):
        #     date = date.replace(' ', '/')
        #     date = date.replace(',', '')
        #     if(len(date.split('/')) > 2):
        #         if(int(date.split('/')[1]) < 10):
        #             date = date.split('/')[0] + '/' + '0' + date.split('/')[1] + '/' + date.split('/')[2]
        #     date = fixMonthName(date)
        #     filComb.write(date + '\t' + score + '\n')
        # scores = []
        # dates = []     
        # rCounter += 1
    print(bigGoogle)

def compareGoogleAllGoogleFound():
    file1 = open("./matchingExtensionFiles/googleFound.txt", 'r')
    file2 = open("./matchingExtensionFiles/allChromeExtensionNames.txt", "r")
    lines1 = sorted(file1.readlines())
    lines2 = sorted(file2.readlines())
    tempList = []
    for line1 in lines1:
        tempList.append(line1.split('/')[-1])
    for tempp in tempList:
        print(tempp)
    # for (l1, l2) in zip(lines1, lines2):
    #     if(l1 != l2):
    #         print(l1 + "\n" + l2 + '\n----------------------------------')


def checkForDoubles():
    urlFile = open("./crawled/concatScores.txt")
    words = urlFile.read()
    words1 = words.split("https")
    counts = {}
    reviewsNum = 0
    bigReviewsNum = 0
    for wordD in words1:
        word = wordD.split("\n")[0]
        # print(word)
        if word not in counts:
            counts[word] = 0
        counts[word] += 1
        if(counts[word] > 1):
            reviewsNum += len(wordD.split("\n")) -3
            if( ( (len(wordD.split("\n")) -3) > 45)):
                bigReviewsNum += 1

    print(reviewsNum)
    print(bigReviewsNum)
    counter = 0
    for k,v in counts.items() :
        # print (str(k) + " " + str(v) + "\n-----------------")
        if v>1:
            counter += 1
            # print(k)
    print(counter)


def googleAnomaly():
    directories = ["./plots/", "./minus10/", "./minus30/", "./percentMinus10/", "./percentMinus30/", "./percentMinus50/"]    
    googleNames = open("./matchingExtensionFiles/allChromeExtensionNames.txt", "r").readlines()
    temp = []
    for googleName in googleNames:
        temp.append(googleName.split('/')[-1].strip('\n'))
    for directory in directories:
        counterForEachLoop = 0
        allFiles = os.listdir(directory)
        for eachFile in allFiles:
            # TODO: CHECK ALSO FOR FILE SIZE
            if( (eachFile.split('.csv')[0] in temp) & (os.path.getsize(directory + eachFile) > 122 ) ):
                counterForEachLoop += 1
                print(eachFile.split(".csv")[0])
                print(os.path.getsize(directory + eachFile))
        print(str(counterForEachLoop) + " " + directory)

def printAnomalies():
    f = open('listAllAnomaliesMinus10.txt', 'w+')
    for each in os.listdir('./minus10'):
        each = each.split('.csv')[0]
        f.write(each + '\n')

def taggerTest():
    reviews = open("./crawled/concatReviews.txt").read()
    # tagger = tag.Tagger()
    # tagger.initialize()
    # tagger.tokenize(reviews)
    # extract.TermExtractor(tagger)
    # extractor.filter = extract.permissiveFilter
    # # extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=2)
    # extracted = extractor(reviews)
    # printTaggedTerms(extracted)
    extractor = extract.TermExtractor()
    print(extractor(reviews))

if __name__ == '__main__':
    # keywordExtraction()
    # keywordExtractionAverage()
    taggerTest()

    # splitReviewsByExtension()
    # splitScoresByExtension()

    # forEachExtensionScore()
    # callRScripts()

    # for every anomaly, count how big it is
    # countAnomaliesSize()

    # for every anomaly, group depending on size
    # is based on countAnomaliesSize()
    # allAnomOutput()

    # find scores only for google extensions from file
    # forEachGoogleExtension()
    #check if all 65 found (actually 66 found)
    # compareGoogleAllGoogleFound()

    # check if google reviews have anomalies
    
#WE WERE HERE
    # googleAnomaly()

    # printAnomalies()

    # ΟΝ Αll Scores check if reviews were crawled more than once
    # checkForDoubles()