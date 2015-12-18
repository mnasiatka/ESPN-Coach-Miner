from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time,re,string
import sys
import urllib2, pprint, string
from HTMLParser import HTMLParser

mData = ""
mDict = {}
mTag = ""
rightAfterOption = False
aliases = {'Tex.':'Texas', 'St.':'Saint', 'N.C.':'North Carolina', 'S.C.':'South Carolina', 'N.M.':'New Mexico', 'Mt.':'Mount', 'Mo.':'Missouri', 'Minn.':'Minnesota', 'Me.':'Maine',
           'La.':'Louisiana', 'Ga.':'Georgia', 'Frank.':'Franklin', 'Fla.':'Florida', 'Col.':'Colorado', 'Colo.':'Colorado', 'Cal':'California', 'Poly':'Polytechnic', 'BYU':'Bringham Young University'}


driver = webdriver.Chrome()
driver.get('http://web1.ncaa.org/stats/StatsSrv/careersearch');

pId = "-100";
yr = "2015";
sport = "MBA";
div = "1";
org = "5";

showTeamPage = "showTeamPage({0}, {1}, '{2}', {3}, {4})".format(pId,yr,sport,div,org);
print showTeamPage
print driver.execute_script(showTeamPage)


sys.exit()


class Season:
    def __init__(self, years, team, record, winloss):
        self.years = years
        self.team = team
        self.record = record
        self.winloss = winloss

class Coach:
    def __init__(self, name, seasons, team):
        self.name = name
        self.seasons = seasons
        self.team = team

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mData = ""
        self.mDict = {}
        self.mTag = ""
        self.rightAfterOption = False
    def handle_starttag(self, tag, attrs):
        if tag == "select":
            self.mTag = tag
            for attr in attrs:
                if attr[0] == "name":
                    tDict = {}
                    tDict[attr[0]] = attr[1]
                    if mDict[self.mData] == []:
                        mDict[self.mData].append(tDict)
                    elif len(mDict[self.mData]):
                        mDict[self.mData].append(tDict)

        elif tag == "option":
            self.mTag = tag
            for attr in attrs:
                if attr[0] == "value":
                    tDict = {}
                    tDict[attr[0]] = attr[1]
                    if mDict[self.mData] == []:
                        mDict[self.mData].append(tDict)
                    elif len(mDict[self.mData]):
                        mDict[self.mData].append(tDict)
            self.rightAfterOption = True
        else:
            self.mTag = ""
    def handle_data(self, data):
        rightAfterOption = False
        if data == "Sport" or data == "School" or data == "Year" or data == "Division":
            mDict[data] = []
            self.mData = data
        elif self.mTag != "" and self.rightAfterOption and data.isalnum and not "\n" in data and not "\r" in data:
            if 'value' in mDict[self.mData][-1]:
                mDict[self.mData][-1][self.mTag] = string.replace(data, '+', '&')
            else:
                tDict = {}
                tDict[self.mTag] = data
                mDict[self.mData].append(tDict)

response = urllib2.urlopen('http://web1.ncaa.org/stats/StatsSrv/careersearch')
html = response.read()
html = string.replace(html, '&', '+')
parser = MyHTMLParser()
parser.feed(html)
nDict = {}
for item in mDict:
    if item != "Division":
        nDict[item] = mDict[item][2:len(mDict[item])]
pp = pprint.PrettyPrinter(indent=1)
pp.pprint(nDict)


coachArray = []
driver = webdriver.Chrome()
driver.get('http://web1.ncaa.org/stats/StatsSrv/careersearch');

print driver.execute_script('document.title')

sys.exit()
for teamSet in nDict['School']:
    a=0
    teamName = teamSet['option']
    teamValue = teamSet['value']
    teamName = 'Akron'
    teamValue = '5'
    print teamSet
    for yearSet in nDict['Year']:
        if a < 5:
            a = a + 1
            yearRange = yearSet['option']
            yearValue = yearSet['value']
            print yearSet
        else:
            break
        print driver.execute_script('document.title')
        #for team in teamList:
        #    for year in yearList: # last 5 years, maybe graph of win/loss of career?
        """
        teamSelect = Select(driver.find_element_by_name('searchOrg'))
        yearSelect = Select(driver.find_element_by_name('academicYear'))

        teamSelect.select_by_value(teamValue)
        yearSelect.select_by_value(yearValue)

        driver.find_element_by_name('teamSearch').find_elements_by_class_name('button')[0].click() # Search for team on given year
        arr = driver.find_element_by_name('results').find_elements_by_class_name('text') # get all results
        ListlinkerHref = driver.find_elements_by_xpath("//*[@href]") # separate results by links, should be number of entries aka number of sports

        for item in ListlinkerHref:
            if item.text == teamName: # if link is the team we're at in loop
                print 'to team page'
                item.click() # To team page
                # On team page. Need to back up afterward
                # Get page info about selected sport and team
                selectionInfo = driver.find_element_by_class_name('foregroundtitle').text
                infoArray = re.split('\W+', selectionInfo)
                mTeam = infoArray[0]
                mSeason = infoArray[1] + '-20' + infoArray[2]
                mSport = infoArray[3]
                mDivision = infoArray[5]
                print mTeam, mSport, mSeason, mDivision
                # First two links are Team website and Coach career page, respectively
                ListlinkerHref3 = driver.find_elements_by_xpath('//td[@width="*"]')
                teamLink = ListlinkerHref3[0]
                coachLink = ListlinkerHref3[1]
                coachName = coachLink.text
                print coachName
        """
driver.quit()
