from bs4 import BeautifulSoup, SoupStrainer
from urllib2 import urlopen
import dryscrape
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import xpath_soup
import httplib2
import urllib
import re
import requests
import log
from selenium.common.exceptions import NoSuchElementException        
import os
import itertools
from multiprocessing import Process
import sys
import errno
from socket import error as socket_error
import datetime

PORT = 5666 + int(sys.argv[1])
PROXY = "127.0.0.1:" + str(PORT)

# PORT = 5666 + int(sys.argv[1])
# PROXY = "127.0.0.1:" + str(PORT)

def main():
    arg = sys.argv[1]
    getAllReviews(arg)

def parse(text, toFile=False):
    global total
    root = BeautifulSoup(text)
    for child in root.findAll("url"):
        log.info("%s %s" % (child.loc.text, child.lastmod.text))
        ext_id = re.findall("[a-z]{32}", child.loc.text)[0]
        ext_name = re.findall("/detail/([^/]*)", child.loc.text)[0]
        lastmod = child.lastmod.text
        if not already_downloaded(ext_id, lastmod):
            crx = download_extension(ext_id, "extensions/%s/%s_%s.crx" % (ext_name, ext_id, lastmod))
            if toFile:
                try:
                    os.makedirs("extensions/%s" % ext_name)
                except:
                    print("no directory")
                name = "extensions/%s/%s_%s.crx" % (ext_name, ext_id, lastmod)
                if os.path.exists(name):
                    return
                with open(name, "wb") as f:
                    f.write(crx)
            else:
                if add2queue(ext_id, crx):
                    total += 1
            feed = mongo.Feed(hid=ext_id, lastmod=lastmod)
            feed.save()
        else:
            log.info("%s %s already downloaded" % (ext_id, lastmod))
    return root     

def testURLselenium(section_url, textF, scoreF, downloadsF, usernameFile, log):
    # print PROXY
    chrome_options = ['--proxy=%s' % PROXY]
    driver = webdriver.PhantomJS(service_args=chrome_options)
    textF = textF
    scoreF = scoreF
    downloadsF = downloadsF
    log = log
    sleep(4)
    driver.get(section_url)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # write to log
    # log.write(html.encode('ascii', errors='ignore').strip())
    sleep(4)


    # UNCOMMENT HERE##
    # Get Ratings and Downloads
    # ratings1 = driver.find_elements_by_class_name("KnRoYd-N-nd")[0]
    # ratings1 = ratings1.get_attribute("aria-label")
    # try:
    #     downloads1 = driver.find_elements_by_class_name('e-f-ih')[0]
    #     ratings1 = ratings1.encode('ascii', errors='ignore').strip()
    #     downloads1 = (downloads1.text).encode('ascii', errors='ignore').strip()
    #     downloadsF.write(str(ratings1) + '\n')
    #     downloadsF.write(str(downloads1) + '\n') 
    # except:
    #     print("first page error") 
    # UNCOMMENT HERE##



    # click on Review
    try:
        if(len(driver.find_elements_by_css_selector("div.e-f-b-L")) > 1):
            element = driver.find_elements_by_css_selector("div.e-f-b-L")[1].click()
    except NoSuchElementException:
        print("nosososos")
    try:
        driver.find_element_by_css_selector("div.z-J").click()
    except:
        print("could not click on black area")
    actions = ActionChains(driver) 
    actions = actions.send_keys(u'ue010')
    actions.perform()

    # click Next
    try:
        nextButton = driver.find_element_by_xpath("//div[@class='ah-mg-j']/a[2]")
    except:
        print("could not click next")
    try:
        while(len(nextButton.text) > 0):
            driver.find_element_by_xpath("//div[@class='ah-mg-j']/a[2]").click()
            html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            # WRITE HTML TO LOG
            # log.write(html.encode('ascii', errors='ignore').strip())
            #CALL TO GET THIS PAGE'S REVIEWS
            pageReviews(html, textF, scoreF, usernameFile)        
            driver.find_element_by_css_selector("div.z-J").click()
            actions = ActionChains(driver) 
            actions = actions.send_keys(u'ue010')
            actions.perform()       
            nextButton = driver.find_element_by_xpath("//div[@class='ah-mg-j']/a[2]")
    except:
        print("could not click review")
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    pageReviews(html, textF, scoreF, usernameFile)
    return 0

def pageReviews(html, textF, scoreF, usernameFile):
    sleep(3)
    #parse
    soup = BeautifulSoup(html, 'lxml')
    results = []
    #previous attempt, only original comments, not answers
    for each in soup.findAll("div", class_="ba-bc-Xb-K"):
        result = each.findChildren("div", recursive=False)
        if "ba-Eb-ba" in str(result[1]):
            temp = str(result[1])
            temp = temp.split('\"Comment\">')[1]
            temp = temp.split('</div>')[0]
            results.append(temp)    
    # get stars
    stars = soup.findAll("div", class_="rsw-stars")
    # FIND DATES
    dates = []
    counterProg = 0
    for each in soup.findAll("div", class_="ba-bc-Xb-K")[4:]:
        if(counterProg > 0):
            counterProg -= 1
        else:
            datee = each.findChildren("span", class_="ba-Eb-Nf")
            if(len(datee) > 1):
                counterProg += len(datee) - 1
            date = datee[0]
            date = date.text
            date = date.replace("Modified ", '')
            dates.append(date)
    for text,date in itertools.izip_longest(results[2:], dates[0:]):
        textF.write(str(text) + '\t' + str(date) + '\n')
    for score,date in itertools.izip_longest(stars[2:-1], dates[0:]):
        score = str(score).split('title=\"')[-1]
        score = score.split(' star')[0]
        if score in {'0','1','2','3','4','5'}:
            scoreF.write(str(score) + '\t' + str(date) + '\n')
    print("usernames = "  + str(len(soup.findAll("a", class_="comment-thread-displayname"))))
    for each,date in itertools.izip_longest(soup.findAll("a", class_="comment-thread-displayname"), dates[0:]):
        usernameFile.write(each.text + '\t' + str(date) + '\n')
    return 0

def getAllURLs():
    fIn = open("./allURLs.txt", 'r')
    root = parse(fIn.read())

def parse(text, toFile=False):
    global total
    root = BeautifulSoup(text)
    counter = 0
    subCounter = 0 
    fOut = open("./allURLsCorrect.txt", 'w+')
    counter1 = 0 
    counter2 = 0
    for child in root.findAll("url"):
        counter1 += 1
        temp = str(child).split("<loc>")
        if (len(temp) > 1):
            child = str(child).split("<loc>")[1]
            child = child.split("</loc>")[0]
            fOut.write(child + '\n')
            counter2 += 1
    print counter1 
    print counter2
    return 0 

def already_downloaded(hid, lastmod):
    if mongo.Feed.objects(hid=hid, lastmod=lastmod).count() == 0:
        return False
    return True

def getAllReviews(arg):
    # input folder to read URLs from
    # fIn = open("./urlSplitBeforeWorkerQueue/urlsA" + str(arg) + ".txt", 'r').readlines()
    fIn = open("./unlistedAidan/extensions_uniq_sanitized.txt", 'r').readlines()
    fReviews = open('allReviewsB' + str(arg) + '.txt', 'w+')
    fScores = open('allScoresB' + str(arg) + '.txt', 'w+')
    fDownloads = open('allDownloadsB' + str(arg) + '.txt', 'w+')
    #write usernames
    usernameFile = open('allUsernamesB' + str(arg) + '.txt', 'w+')
    for each in reversed(fIn):
        id = each.split('\n')[0]
        id = id.split('/')[-1]

        # open log to write
        # log = open("./htmlLogs/" + id + '_' + str(datetime.datetime.now()), "a+")
        log = open("deleteLog", "w+")
        fReviews.write(str(each) + '\n')
        fScores.write(str(each) + '\n')
        fDownloads.write(str(each) + '\n')
        usernameFile.write(str(each) + '\n')
        print(each)
        testURLselenium(each, fReviews, fScores, fDownloads, usernameFile, log)
        # try:
        #     testURLselenium(each, fReviews, fScores, fDownloads, usernameFile, log)
        # except:
        #     print("error in the main function")                    
        fReviews.write("-----------------------------------------\n")
        fScores.write("-----------------------------------------\n")
        fDownloads.write("-----------------------------------------\n")
        usernameFile.write("-----------------------------------------\n")
        sleep(5)

    return 0

def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

if __name__ == '__main__':
    main()