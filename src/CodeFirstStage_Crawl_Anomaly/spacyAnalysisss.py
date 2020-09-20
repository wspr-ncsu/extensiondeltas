import spacy
import re
import codecs
from datetime import datetime, timedelta
import pandas as pd
# import timedelta

import rpy2
# print(rpy2.__version__)
from numpy import *
import scipy as sp
from pandas import *
# from rpy2.robjects.packages import importr
# import rpy2.robjects as ro
# import rpy2.robjects as robjects
# import rpy2.robjects.packages as rpackages
# from rpy2.robjects.vectors import StrVector

FILESTRING = "./backup3/allReviews"
FILESTRING = "./backup4/concatReviews"
# today = str(datetime.today().strftime('%b %d, %Y'))
today = "Oct 20, 2018"

def main():
        keywordFile = "./keywordFile.txt"
        alldicts = {}
        keywords = open(keywordFile, 'r').readlines()
        for keyword in keywords:
                keyword = keyword.strip("\n")
                alldicts[keyword] = 0
        # WHEN THEY WERE 6 FILES
        # for i in range(0,6):
        #         filename = "./backup3/allReviews" + str(i) + ".txt"
        #         alldicts = analyzeFile(filename, keywordFile, alldicts)
        #         # alldicts.append(partDict)
        # FOR ONE FILE
        filename = "./backup5/concatReviews.txt"
        alldicts = analyzeFile(filename, keywordFile, alldicts)
        print(alldicts)
        for each in sorted(alldicts):
                print(each + '\t' + str(alldicts[each]))


def analyzeFile(filename, keywordFile, alldicts):
        dictionary = {}
        nlp = spacy.load('en')
        f1 = open(filename, 'r').readlines()
        keywords = open(keywordFile, 'r').readlines()
        for keyword in keywords:
                keyword = keyword.strip("\n")
                dictionary[keyword] = 0
        for line in f1:
                keywords = open(keywordFile, 'r').readlines()
                for keyword in keywords:
                        keyword = keyword.strip("\n")
                        #add to dictionary
                        if keyword in line:
                                dictionary[keyword] += 1
                                alldicts[keyword] += 1
        # print dictionary
        return alldicts
        # for instance in dictionary:
        #       print( str(dictionary) + "has : " + str(dictionary[instance]) +'\n')
        # f = codecs.open(filename, encoding='utf-8').read()
        # doc = nlp(f[:99999])
        # for entity in doc.ents:
        #     print(entity.text, entity.label_)

def splitScoresByExtension():
    filename = "./backup5/concatScores.txt"
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
    # allScores = allScores.strip('-------')
    # print allScores[:1000]
    print ("Scores = " + str(countScore) + "\nEmpties = " + str(countEmpty) + "\nHttps = " + str(countHttp) + "\nDashes = " + str(countDash) + '\n')

    # for line in allScore:

def splitReviewsByExtension():
    filename = "./backup6/concatReviews.txt"
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
    # allScores = allScores.strip('-------')
    # print allScores[:1000]
    print("Scores = " + str(countReview) + "\nEmpties = " + str(countEmpty) + "\nHttps = " + str(countHttp) + "\nDashes = " + str(countDash) + '\n')

def forEachExtensionScore():
    scoreNamefile = './tempScores.txt'
    dateNamefile = './tempDates.txt'
    combNamefile = './tempComb.txt'    
    filename = "./backup8/concatScores.txt"
    allScores = open(filename, 'r').read()
    bigCounter = 0     
    blocks = re.split('-{40,}', allScores)
    print(len(blocks))
    bigBlocks = []
    for block in blocks:
        block = block.split('\n')
        if(len(block) > 30):
            bigCounter +=1
            bigBlocks.append(block)
        # print len(block)
        # for line in block:
        #     print (line)
        # print len(block)
        # print block
        # break
    #     if len(block > 20):
    #         countScore +=1
    # print countScore
    print(bigCounter)
    return
    #FOR EACH BLOCK
    scores = []
    dates = []
    newDates = []
    for bigblock in bigBlocks:
        for line in bigblock:
            line = line.split("\t")
            if len(line) > 1 :
                scores.append(line[0])
                dates.append(line[1])
        # print("DATES TRANSFORMMMMM")                
        for date in dates:
            if(date == 'None'):
                # print('None')
                newDates.append('None')
                # pass
            elif( ('hour' in str(date)) | ('minute' in str(date)) ):
                # print(date_to_nth_day(today))
                newDates.append(today)
                # pass
            elif('day' in date):
                daysBack = int(date.split(' ')[0])
                realDay = datetime.today() - timedelta(days=daysBack)
                realDay = str(realDay.strftime('%b %d, %Y'))
                newDates.append(realDay)
                # print(date_to_nth_day(realDay))
            else:
                # print(date_to_nth_day(date))
                newDates.append(date)
                # pass
        # print("----------------")
        # print "SCORES = " + str(scores)
        # print "DATES = " + str(dates)            
        filScores = open(scoreNamefile, 'w+')
        filDates = open(dateNamefile, 'w+')
        filComb = open(combNamefile, 'w+')
        # filComb.write('\tScore\n')
        filComb.write('date,Score\n')
        for score in scores:   
            filScores.write(str(score) + '\n')      
        for date in newDates:
            filDates.write(str(date) + '\n')  
        for (date,score) in zip(newDates,scores):
            # print(date)
            date = date.replace(' ', '-')
            date = date.replace(',', '')
            if(len(date.split('-')) > 2):
                # print (date.split('-')[1])
                if(int(date.split('-')[1]) < 10):
                    date = date.split('-')[0] + '-' + '0' + date.split('-')[1] + '-' + date.split('-')[2]
            # date = datetime.strptime(date,'%b-%d-%Y').strftime('%d-%m-%Y')
            # date = date.strftime('%d-%m-%Y')
            # print(part)
            # break
            # filComb.write(date + '\t' + score + '\n')    
            filComb.write(date + ',' + score + '\n')   
        scores = []
        dates = []
    # install.packages('anomalize')
    # utils = importr('utils')
    # #DONE
    # utils.install_packages('anomalize')   

    # packageNames = ('afex', 'emmeans')
    # utils = rpackages.importr('utils')
    # utils.chooseCRANmirror(ind=1)

    # packnames_to_install = [x for x in packageNames if not rpackages.isinstalled(x)]

    # if len(packnames_to_install) > 0:
    #     utils.install_packages(StrVector(packnames_to_install))
# import pandas.rpy2.common as com    
    #---------
    
    # #install.packages('devtools') 
    # devtools::install_github("business-science/anomalize")
    # library(anomalize) #tidy anomaly detectiom
    # library(tidyverse) #tidyverse packages like dplyr, ggplot, tidyr
    # library(coindeskr) #bitcoin price extraction from coindesk
    # btc <- get_historic_price(start = "2017-01-01")
    # btc_ts <- btc %>% rownames_to_column() %>% as.tibble() %>% 
    # mutate(date = as.Date(rowname)) %>% select(-one_of('rowname')) 
    # head(btc_ts)   
    # btc_ts %>% 
    # time_decompose(Price, method = "stl", frequency = "auto", trend = "auto") %>%
    # anomalize(remainder, method = "gesd", alpha = 0.05, max_anoms = 0.2) %>%
    # plot_anomaly_decomposition()

    # btc_ts %>% 
    # time_decompose(Price) %>%
    # anomalize(remainder) %>%
    # time_recompose() %>%
    # plot_anomalies(time_recomposed = TRUE, ncol = 3, alpha_dots = 0.5)
    # btc_ts %>% 
    # time_decompose(Price) %>%
    # anomalize(remainder) %>%
    # time_recompose() %>%
    # filter(anomaly == 'Yes') 

# def date_to_nth_day(date, format='%Y%m%d'):
#     date = datetime.strptime(date, format=format)
#     new_year_day = datetime(year=date.year, month=1, day=1)
#     return (date - new_year_day).days + 1

def date_to_nth_day(date, format='%b %d, %Y'):
    date = pd.to_datetime(date, format=format)
    # new_year_day = pd.Timestamp(year=date.year, month=1, day=1)
    new_year_day = pd.Timestamp(year=2009, month=1, day=1)
    return (date - new_year_day).days + 365*(date.year - new_year_day.year) + 1

if __name__ == '__main__':
    # main()
    # splitReviewsByExtension()
    # splitScoresByExtension()

    forEachExtensionScore()
