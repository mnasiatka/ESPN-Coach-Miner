from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time,re, urllib2, pprint, string,sys
from HTMLParser import HTMLParser
import requests, json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

coachLinkDict = {}
payloads = []
index = 0

driver = webdriver.Chrome()
driver.get('http://web1.ncaa.org/stats/StatsSrv/careersearch')

r = requests.post('http://ythogh.com/lrt/get_coaches.php')
coaches = json.loads(r.text)
print str(len(coaches)) + " coaches to search through."
for name in coaches:

    index = index + 1
    if index >= 1000 and index % 100 == 0:
        print 'Searched ' + str(index) + ' so far.'
            # For each coach we have on record
        for name in coachLinkDict:
            # For each sport the coach coaches
            for link in coachLinkDict[name]:
                #print name,',',link
                try:
                    driver.execute_script(link) # Go to the team sport page
                except:
                    continue
                # Get sport he is coaching
                title_text = driver.find_element_by_class_name("titletext")
                mSport = string.split(title_text.text,'\n')[0];
                # Get last 5 years of this coach's record in this sport
                record_history = driver.find_elements_by_xpath("//table")[-1] # separate results by tables, 5 tables with the last as the history
                season_rows = record_history.find_elements_by_xpath(".//tr")[1:] # separate results by rows, each as a season
                #print len(season_rows)
                # Get 5 most recent seasons
                if len(season_rows) > 5:
                    season_rows = season_rows[len(season_rows) - 5:len(season_rows)]
                # Get each season of coach's history
                try:
                    for season in season_rows:
                        splitted = string.split(season.text,' ')[:-2]
                        print name,splitted
                        mSeason = splitted[0]
                        mRecord = splitted[-2]
                        mPercent = splitted[-1]
                        mTeam = splitted[1]
                        for i in range(2,len(splitted)-2):
                            mTeam = mTeam + ' ' + splitted[i]
                        payload = {'coach' : name, 'team' : mTeam, 'season' : mSeason, 'record' : mRecord, 'winpercent' : mPercent, 'sport' : mSport};
                        doAdd = True
                        for item in payload:
                            if payload[item] == '':
                                doAdd = False
                        if doAdd:
                            payloads.append(payload)
                finally:
                    driver.back()

        for payload in payloads:
            r = requests.post('http://ythogh.com/lrt/add_coach_history.php',params=payload)
            if r.status_code != 200:
                print 'Error sending:', payload['coach'], ':', r.url
        coachLinkDict = {}
        payloads = []
    try:
        driver.find_element_by_name('firstName').clear()
        driver.find_element_by_name('lastName').clear()
    except:
        driver.back()

    # Parse coach's name
    splitted = string.split(name, ' ')
    if len(splitted) < 2:
        continue
    firstname = splitted[0]
    lastname = splitted[1]
    firstname = re.sub('[^A-Za-z]','',firstname)
    lastname = re.sub('[^A-Za-z]','',lastname)
    linkname = lastname + ', ' + firstname

    if len(firstname) < 2 or len(lastname) < 2:
        continue

    # Select coach name and submit
    driver.find_element_by_name('firstName').send_keys(firstname)
    driver.find_element_by_name('lastName').send_keys(lastname)
    driver.find_elements_by_name('playerCoach')[1].click()
    driver.find_elements_by_class_name('button')[0].click()

    # Find relevant links
    links = driver.find_elements_by_xpath("//*[@href]") # separate results by links, should be number of entries aka number of sports
    for link in links:
        if similar(link.text, linkname) > .8:
            if not name in coachLinkDict:
                coachLinkDict[name] = [link.get_attribute('href')]
            else:
                coachLinkDict[name].append(link.get_attribute('href'))
