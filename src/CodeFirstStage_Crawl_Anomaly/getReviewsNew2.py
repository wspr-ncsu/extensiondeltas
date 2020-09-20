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

# PROXY = "127.0.0.1:5566"
PORT = 5666 + int(sys.argv[1]) + 6
PROXY = "127.0.0.1:" + str(PORT)

# PORT = 5666 + int(sys.argv[1])
# PROXY = "127.0.0.1:" + str(PORT)

BASE_URL = 'https://chrome.google.com/webstore/detail/addtoany-share-anywhere/ffpgijchhhkhnokafdeklpllijgnbche'
# BASE_URL = 'http://avi.im/stuff/js-or-no-js.html'
BASE_URL = 'https://chrome.google.com/webstore/detail/grammarly-for-chrome/kbfnbcaeplbcioakkpcpgfkobkghlhen'
# BASE_URL = 'https://chrome.google.com/webstore/detail/google-keep-chrome-extens/lpcaedmchfhocbbapmcbpinfpgnhiddi'
# BASE_URL = 'https://chrome.google.com/webstore/detail/jogos-de-corrida-de-moto/mimlkalllpliaanmkbodacbbedbmaldl'
BASE_URL = "https://steamcommunity.com/id/PapiDimmi"
BASE_UTL = "http://192.168.0.10:5801/"
BASE_URL = "https://chrome.google.com/webstore/detail/grammarly-for-chrome/kbfnbcaeplbcioakkpcpgfkobkghlhen"
BASE_URL = "https://chrome.google.com/webstore/detail/timed/elimnnkcljpjbhoaoeimjjfimhjiekbj"

def main():
 #    text = ""
 #    for i in range(0,100):
 #        r = requests.get("https://chrome.google.com/webstore/sitemap?shard=%s&numshards=100" % (str(i)))
 #        text += r.text
 #    text = f.read()
 #    root = parse(text)
    # # section_url = BASE_URL
    # for each in root:
    #   section_url = each
    #   # testURL(section_url)
    #   testURLselenium(section_url)

    # section_url = BASE_URL
    # testURLselenium(section_url)
    # getAllURLs()
    # print len(sys.argv)
    arg = sys.argv[1]
    # print arg
    # return
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
                    pass
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


def testURL(section_url):
    # # Put the stuff you see when using Inspect Element in a variable called html.
    # html = urlopen(section_url).read()    
    # # Parse the stuff.
    # print html[:100]
    # soup = BeautifulSoup(html, "lxml")    
    # # The next two lines will change depending on what you're looking for. This 
    # # line is looking for <dl class="boccat">.  
    # boccat = soup.find("dl", "ba-Eb-ba")    
    # # This line organizes what is found in the above line into a list of 
    # # hrefs (i.e. links). 
    # print boccat
    # category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("dd")]
    # return category_links

    session = dryscrape.Session(base_url = BASE_URL)
    session.visit(section_url)
    print(type(session))
    response = session.body()
    print(type(response))
    print response
    # soup = BeautifulSoup(response, 'lxml')
    soup = BeautifulSoup(session, 'lxml')
    # results = soup.findAll("div", {"class": "ba-Eb-ba"})
    results = soup.findAll("div", class_="ba-Eb-ba")
    # results = soup.findAll(text='ga:type=\"Comment\"')
    print results
    print len(results)
    # print(soup)
    # print len(soup)
    return 0

def testURLselenium(section_url, textF, scoreF, downloadsF, log):
    # os.system("sudo docker run -d -p 5566:5566 -p 4444:4444 --env tors=25 mattes/rotating-proxy")
    # print( "curl --proxy 127.0.0.1:5566 " + str(section_url) + " > ./htmlTemp.html" )
    # return


    # chrome_options = webdriver.ChromeOptions()
    # # chrome_options.add_argument('--headless')
    # # chrome_options.add_argument('--no-sandbox')
    # # chrome_options.add_argument('--disable-dev-shm-usage')
    # # print str(PROXY)
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # # driver = webdriver.Chrome(executable_path="/home/nikos/Downloads/chromedriver_linux64/chromedriver.exe", options=chrome_options)
    # driver = webdriver.Chrome(r'/home/nikos/Downloads/chromedriver_linux64/chromedriver', options=chrome_options)

    # print PROXY
    chrome_options = ['--proxy=%s' % PROXY]
    driver = webdriver.PhantomJS(service_args=chrome_options)


    # os.system('rm htmlTemp.html')
    # os.system("wget -e <http_proxy>=127.0.0.1:5566 " + str(section_url) + " > ./htmlTemp.html")
    # os.system("curl --proxy 127.0.0.1:5566 " + str(section_url) + " > ./htmlTemp.html")
    # textF = open('textFileReviews.txt', 'w+')
    # scoreF = open('scoreFileReviews.txt', 'w+)
    # os.system('cat ./htmlTemp.html')
    textF = textF
    scoreF = scoreF
    downloadsF = downloadsF
    log = log
    # driver = webdriver.PhantomJS()

    # f = open("")

    # sampleFile = open("/home/nikos/Documents/reviews_scripts/htmlTemp.html", 'r').read()
    # f = open('./htmlTemp.html', 'r').read()
    # f = f.split("<head><title>")[1]
    # f = "<head><title>" + f
    # f = f.split("</html>")[0]
    # print f
    # driver.get(f)
    # print driver


    # driver.get("file:///home/nikos/Documents/reviews_scripts/htmlTemp.html")
    # driver.get("/home/nikos/Documents/reviews_scripts/htmlTemp.html")
    # print (httt)

    # sleep(5)
    sleep(6)

    driver.get(section_url)

    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # print html

    log.write(html.encode('ascii', errors='ignore').strip())

    sleep(6)
    # sleep(1)


    # print httt
    # f2 = open("correctRes.html", 'w+')
    # f2.write(str(html))
    # html = driver.execute_script("return document")
    # html = driver.execute_script(return ALL)
    # pageReviews(html, textF, scoreF)


# COMMENT OUT LATWR
    # print html
    # print len(html)
    # driver.execute("document.innerHTML = " + f)
    # print html
    # ratings1 = driver.find_elements_by_css_selector("div.KnRoYd-N-nd")[0]
    ratings1 = driver.find_elements_by_class_name("KnRoYd-N-nd")[0]
    # ratings1 = driver.find_element_by_xpath("//div[@class='KnRoYd-N-nd']")
    # ratings1 = (ratings1.text).encode('ascii', errors='ignore').strip()
    # ratings1 = driver.find_elements_by_css_selector("span[aria-label]")[0]
    ratings1 = ratings1.get_attribute("aria-label")
    # ratings1 = (ratings1.text).encode('ascii', errors='ignore').strip()
    # print (ratings1)
    # ratings2 = driver.find_elements_by_css_selector("div.KnRoYd-N-Re")[0]
    # downloads = driver.find_elements_by_css_selector("FokDXb.e-f-ih-s")[0]
    # downloads1 = driver.find_elements_by_css_selector("span.e-f-ih")[0]
    # downloads1 = driver.find_element_by_xpath("//div[@class='e-f-ih']")
    try:
        downloads1 = driver.find_elements_by_class_name('e-f-ih')[0]
        # print(downloads1)
        
        ratings1 = ratings1.encode('ascii', errors='ignore').strip()
        downloads1 = (downloads1.text).encode('ascii', errors='ignore').strip()
        # print(str(ratings1))
        # print(str(downloads1))
        downloadsF.write(str(ratings1) + '\n')
        downloadsF.write(str(downloads1) + '\n') 
    except:
        pass    
    # downloads2 = downloads1.getAttribute("title");
    # downloadsF.write(str(ratings1))
    # downloadsF.write(str(downloads))
    # downloadsF.write("ratings1 = " + str(ratings1) + '\n')
    # downloadsF.write("ratings2 = " + str(ratings2) + '\n')
    # print("downloads1 = " + str(downloads1) + '\n')
    # print("ratings1TTT = " + str(ratings1.text) + '\n')
    # print("ratings1TTT = " + str(ratings1.text) + '\n')
    # print("downloads1TTT = " + str(downloads1.text) + '\n')    
    # return
    # downloadsF.write("downloads1 = " + str(downloads1) + '\n')
    # downloadsF.write("downloads2 = " + str(downloads2) + '\n')
    # downloadsF.write("ratings1TTT = " + str(ratings1.text) + '\n')
    # downloadsF.write("ratings2TTT = " + str(ratings2.text) + '\n')
    # downloadsF.write("downloads1TTT = " + str(downloads1.text) + '\n')
    # downloadsF.write("downloads2TTT = " + str(downloads2.text) + '\n')    
    # downloadsF.flush()
# COMMENT OUT LATWR


    # click on Review
    try:
        # print(len(driver.find_elements_by_css_selector("div.e-f-b-L")))
        if(len(driver.find_elements_by_css_selector("div.e-f-b-L")) > 1):
            # print ("review found 1")
            element = driver.find_elements_by_css_selector("div.e-f-b-L")[1].click()
    except NoSuchElementException:
        print("nosososos")
    # click on "user Review" -> maybe fix
    # driver.find_element_by_css_selector("h2.z-J-w").click()
    try:
        # print ("review found 2")
        driver.find_element_by_css_selector("div.z-J").click()
    except:
        pass
    actions = ActionChains(driver) 
    actions = actions.send_keys(u'ue010')
    actions.perform()

    # click Next
    try:
        # print ("review found 3")
        nextButton = driver.find_element_by_xpath("//div[@class='ah-mg-j']/a[2]")
    except:
        pass
    # nextButton = driver.find_element_by_css_selector("a.Aa dc-ce")
    # while(len(nextButton.text) > 0):
    try:
        while(len(nextButton.text) > 0):
            # sleep(0.5)
            # driver.find_element_by_css_selector("a.Aa\ dc-ce").click()        
            # print ("review found")
            driver.find_element_by_xpath("//div[@class='ah-mg-j']/a[2]").click()
            html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            # WRITE HTML TO LOG
            log.write(html.encode('ascii', errors='ignore').strip())
            #CALL TO GET THIS PAGE'S REVIEWS
            pageReviews(html, textF, scoreF)        
            # click on Review
            # element = driver.find_elements_by_css_selector("div.e-f-b-L")[1].click()
            # click on "user Review" -> maybe fix
            driver.find_element_by_css_selector("div.z-J").click()
            actions = ActionChains(driver) 
            actions = actions.send_keys(u'ue010')
            actions.perform()       
            # nextButton = driver.find_element_by_css_selector("a.Aa dc-ce")
            nextButton = driver.find_element_by_xpath("//div[@class='ah-mg-j']/a[2]")
            # print len(nextButton.text)
    except:
        pass
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    pageReviews(html, textF, scoreF)

    # sleep(1)
    # html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # # p_element = driver.find_elements_by_class_name("ba-Eb-ba")
    # # for each in p_element:
    # #     print(each.text)
    # soup = BeautifulSoup(html, 'lxml')
    # results = soup.findAll("div", class_="ba-Eb-ba")
    # # Next button: class="Aa dc-se" , if not empty
    # outF.write(str(results))
    # print results

    

    # html = ((driver.find_element_by_xpath("//*[contains(text(), 'NextLink')]"))[0]).click()
    # print len(html)
    # sleep(2)
    # soup = BeautifulSoup(html, 'lxml')
    # results = soup.findAll("div", class_="ba-Eb-ba")
    # outF.write(str(results))
    # print results


    #CLOSE DRIVERS
    # driver.close()
    # driver.quit()
    return 0

def pageReviews(html, textF, scoreF):
    sleep(3)
    # sleep(1)
    # try:
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
    # to get also answers, just search ba-Eb-ba
    # results = soup.findAll("div", class_='ba-Eb-ba')
    
    # get stars
    stars = soup.findAll("div", class_="rsw-stars")
    #UNCOMMENT HERE
    # print len(results[2:])
    # print len(stars[2:-1])


    # FIND DATES
    dates = []
    counterProg = 0
    # dates = soup.findAll("span", class_="ba-Eb-Nf")
    for each in soup.findAll("div", class_="ba-bc-Xb-K")[4:]:
        if(counterProg > 0):
            counterProg -= 1
        else:
        # print(str(each))
        # return
        # check = each.findChildren("a", class_="z-b-ob-y")
        # print(str(each))
        # return
        # check = each.findAll("div", class_="rsw-stars")
        # # print len(check)
        # print len(check)
        # if(len(check) == 1):
        # if("rsw-stars" in str(each)):
            datee = each.findChildren("span", class_="ba-Eb-Nf")
            if(len(datee) > 1):
                counterProg += len(datee) - 1
            #UNCOMMENT HERE
            # print len(datee)
            # return
            date = datee[0]
            # for date in datee:
            #     pass
                # return
                # print(len(date.findAll("div", class_="rsw-stars")))
                # if("rsw-stars" in str(date)):
            date = date.text
                    # print len(date)
                    # if( (len(str(date)) > 0) & ("rsw-stars" in date)):
                        # date = str(date)
                        # print(len(date))
            date = date.replace("Modified ", '')
                    # date = date.lstrip("Modified ")
                    # date.strip("Modified")
                    # if len(date.split("Timestamp\">")) > 1:
                    # date = date.split("Timestamp\">")[1]
                    # if len(date.split("class=ba-Eb-Nf\">")) > 1:
                    #     date = date.split("class=ba-Eb-Nf\">")[1]
                    # date = date.split("</span>")[0]
            dates.append(date)
        # if( len())
        # for each2 in each.findAll("div", class_="ba-Eb-ba"):
        #     print len(each2)
        #     date = each.findChildren("div", recursive=False)
        #     print "len of this date = " + str(len(date))
        #     if(date != None):
        #         dates.append(each2)
    #UNCOMMENT HERE
    # print ("length of dates  = " + str(len(dates)))
    # print dates[2:]
    # return
    for text,date in itertools.izip_longest(results[2:], dates[0:]):
        textF.write(str(text) + '\t' + str(date) + '\n')
        # print text
    for score,date in itertools.izip_longest(stars[2:-1], dates[0:]):
        score = str(score).split('title=\"')[-1]
        score = score.split(' star')[0]
        if score in {'0','1','2','3','4','5'}:
            scoreF.write(str(score) + '\t' + str(date) + '\n')
            # print score
    # except:
    #     pass
    # for text, score in zip(results[2:],stars[2:-1]):
    #   # score = str(score).split('title=\"')[-1]
    #   score = str(score).split('title=\"')
    #   print len(score)
    #   score = score.split(' star')[0]
    #   outF.write(str(text) + '\n' + str(score) + '\n')
    #   # print (str(text) + '\n' + str(score) + '\n')
    return 0

def getAllURLs():
    # url = 'https://chrome.google.com/webstore/detail'
    # http = httplib2.Http()
    # status, response = http.request(url)

    # counter = 0
    # # for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features='lxml'):
    # #     counter += 1
    # #     # if link.has_attr('href'):
    # #     #   print link['href']
    # # print counter

    # html = urllib.urlopen(url).read()
    # soup = BeautifulSoup(html)
    # for a in soup.findAll('a',{'title':re.compile('.+') }):
    #   counter += 1
    # print counter




    # outF = open("./allURLs.txt", 'w+')
    # text = ""
    # remote = True
    # if remote:
    #     print("if")
    #     for i in range(0,100):
    #         print i
    #         r = requests.get("https://chrome.google.com/webstore/sitemap?shard=%s&numshards=100" % (str(i)))
    #         text += r.text
    #         print len(text)

    #         # return
    # else:
    #     print("else")
    #     with open("sitemap2") as f:
    #         text = f.read()
    # outF.write(text)
    # root = parse(text)

    # log.info("Downloaded %s extensions and submitted to queue %s" % (downloaded, total))
    
    fIn = open("./allURLs.txt", 'r')
    root = parse(fIn.read())



    # xmlDict = {}

    # r = requests.get("https://chrome.google.com/webstore/sitemap?shards=1000.xml")
    # xml = r.text

    # soup = BeautifulSoup(xml)
    # sitemapTags = soup.find_all("sitemap")

    # print "The number of sitemaps are {0}".format(len(sitemapTags))
    # for sitemap in sitemapTags:
    #     xmlDict[sitemap.findNext("loc").text] = sitemap.findNext("lastmod").text

    # print xmlDict    


def parse(text, toFile=False):
    global total
    root = BeautifulSoup(text)
    counter = 0
    subCounter = 0 
    fOut = open("./allURLsCorrect.txt", 'w+')
    # print len(root.findAll("url"))
    # print(root.findAll("url")[0])
    # return
    # for child in root.findAll("url"):
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
    # for child in root.findAll("url"):
    # #     counter += 1
    # # print child 
    # # return child
    #     log.info("%s %s" % (child.loc.text, child.lastmod.text))
    #     ext_id = re.findall("[a-z]{32}", child.loc.text)[0]
    #     ext_name = re.findall("/detail/([^/]*)", child.loc.text)[0]
    #     lastmod = child.lastmod.text
    #     if not already_downloaded(ext_id, lastmod):
    #         subCounter += 1
    #         totalCounter += 1
    #         crx = download_extension(ext_id, "extensions/%s/%s_%s.crx" % (ext_name, ext_id, lastmod))
    #         if toFile:
    #             try:
    #                 os.makedirs("extensions/%s" % ext_name)
    #             except:
    #                 pass
    #             name = "extensions/%s/%s_%s.crx" % (ext_name, ext_id, lastmod)
    #             if os.path.exists(name):
    #                 return
    #             with open(name, "wb") as f:
    #                 f.write(crx)
    #         else:
    #             if add2queue(ext_id, crx):
    #                 total += 1
    #         feed = mongo.Feed(hid=ext_id, lastmod=lastmod)
    #         feed.save()
    #     else:
    #         log.info("%s %s already downloaded" % (ext_id, lastmod))
    #     print subCounter
    #     subCounter = 0
    # print counter
    # return root

def already_downloaded(hid, lastmod):
    if mongo.Feed.objects(hid=hid, lastmod=lastmod).count() == 0:
        return False
    return True

def getAllReviews(arg):
    fIn = open("urlsA" + str(arg) + ".txt", 'r').readlines()
    # fIn = open("allURLsCorrect.txt", 'r')
    fReviews = open('allReviewsA' + str(arg) + '.txt', 'w+')
    fScores = open('allScoresA' + str(arg) + '.txt', 'w+')
    fDownloads = open('allDownloadsA' + str(arg) + '.txt', 'w+')
    # counter = 0
    # proc = []
    # while(True):
    #     while(len(proc) < 6):
    #         each = fIn.readline()
    #         fReviews.write(str(each))
    #         fScores.write(str(each))        
    #         p = Process(target=testURLselenium, args=(each, fReviews, fScores) )
    #         p.start()
    #         proc.append(p)
    #     for p in proc:
    #         p.join()
    #         fReviews.write("-----------------------------------------\n")
    #         fScores.write("-----------------------------------------\n")
    #     # counter +=1
    #     sleep(2)
    #     proc = []
    #     print(len(proc))
    
    # for each in fIn[int(arg)*25092:(int(arg)+1)*25092]:
    # if(int(sys.argv[1]) == 0 ):
    #     continueFrom=0
    # if(int(sys.argv[1]) == 1 ):
    #     continueFrom=25145
    # if(int(sys.argv[1]) == 2 ):
    #     continueFrom=51679
    # if(int(sys.argv[1]) == 3 ):
    #     continueFrom=76707
    # if(int(sys.argv[1]) == 4 ):
    #     continueFrom=103948
    # if(int(sys.argv[1]) == 5 ):
    #     continueFrom=125592
    # for each in fIn[int(continueFrom):]:
    # for each in fIn[25000*(sys.argv[1]):continueFrom]
    # for each in fIn[25000*int(sys.argv[1]):25000*(int(sys.argv[1]) + 1)]:
    for each in reversed(fIn):
        # print each1
        id = each.split('\n')[0]
        id = id.split('/')[-1]

        log = open("./htmlLogs/" + id + '_' + str(datetime.datetime.now()), "a+")


        # each = BASE_URL




        # try:
        #     # print each        
        #     fReviews.write(str(each))
        #     fScores.write(str(each))
        #     testURLselenium(each, fReviews, fScores)
        #     fReviews.write("-----------------------------------------\n")
        #     fScores.write("-----------------------------------------\n")
        #     sleep(10)
        # except:
        #     pass
        fReviews.write(str(each) + '\n')
        fScores.write(str(each) + '\n')
        fDownloads.write(str(each) + '\n')
        # proc = []
        # while(len(proc) < 6):
        #     p = Process(target=testURLselenium, args=(each, fReviews, fScores) )
        #     p.start()
        #     proc.append(p)

        # for p in proc:
        #     p.join()



        try:
            testURLselenium(each, fReviews, fScores, fDownloads, log)
        except:
            pass
        # testURLselenium(each, fReviews, fScores, fDownloads, log)




        # except requests.exceptions.ConnectionError:

        # except socket_error as serr:
        #     if serr.errno == errno.ECONNREFUSED:
        #         print("Connection refused ")
        # except:
            # pass

        # if(counter%6 == 0):
        #     p1 = Process(target=testURLselenium, args=(each, fReviews, fScores) )
        #     p1.start()
        #     p1.join()
        # if(counter%6 == 1):
        #     p2 = Process(target=testURLselenium, args=(each, fReviews, fScores) )
        #     p2.start()
        #     p2.join()
        # if(counter%6 == 2):
        #     p3 = Process(target=testURLselenium, args=(each, fReviews, fScores) )
        #     p3.start()
        #     p3.join()
        # if(counter%6 == 3):
        #     p4 = Process(target=testURLselenium, args=(each, fReviews, fScores) )
        #     p4.start()
        #     p4.join()
        # if(counter%6 == 4):
        #     p5 = Process(target=testURLselenium, args=(each, fReviews, fScores) )
        #     p5.start()
        #     p5.join()
        # if(counter%6 == 5):
        #     p6 = Process(target=testURLselenium, args=(each, fReviews, fScores) )
        #     p6.start()  
        #     p6.join()                      
        fReviews.write("-----------------------------------------\n")
        fScores.write("-----------------------------------------\n")
        fDownloads.write("-----------------------------------------\n")
        # counter +=1
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