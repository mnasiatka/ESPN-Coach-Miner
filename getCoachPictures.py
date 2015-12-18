from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
driver.get('http://images.google.com')

r = requests.post('http://ythogh.com/lrt/get_coaches.php')
coaches = json.loads(r.text)
print str(len(coaches)) + " coaches to search through."
query = ""
wait_time = .25

for name in coaches:
    try:
        school = coaches[name][0].replace(" ", "+")
        school = school.replace("(","")
        school = school.replace(")","")
        sport = coaches[name][1].replace(" ", "+")
        new_name = name.replace(" ", "+")
        query = new_name + "+" + school + "+" + sport
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys(query)
        driver.find_element_by_name("q").send_keys(Keys.ENTER);
        time.sleep(wait_time)

        photo = driver.find_element_by_xpath("//div[@data-ri='0']").find_element_by_tag_name("img").get_attribute("src")
        print name, '=>', photo

    except:
        print 'Failed on ' + name + '. Retrying.'
        try:
            time.sleep(4*wait_time)
            photo = driver.find_element_by_xpath("//div[@data-ri='0']").find_element_by_tag_name("img").get_attribute("src")
            print name, '=>', photo
        except:
            print 'Failed on ' + name + '. Continuing.'
        continue