from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time,re, urllib2, pprint, string,sys
from HTMLParser import HTMLParser
import requests

mData = ""
mDict = {}
mTag = ""
rightAfterOption = False
aliases = {'Tex.':'Texas', 'St.':'Saint', 'N.C.':'North Carolina', 'S.C.':'South Carolina', 'N.M.':'New Mexico', 'Mt.':'Mount', 'Mo.':'Missouri', 'Minn.':'Minnesota', 'Me.':'Maine',
           'La.':'Louisiana', 'Ga.':'Georgia', 'Frank.':'Franklin', 'Fla.':'Florida', 'Col.':'Colorado', 'Colo.':'Colorado', 'Cal':'California', 'Poly':'Polytechnic', 'BYU':'Bringham Young University'}


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
#pp = pprint.PrettyPrinter(indent=1)
#pp.pprint(nDict)

it = 0
sIndx = 0
coachArray = []
driver = webdriver.Chrome()
driver.get('http://web1.ncaa.org/stats/StatsSrv/careersearch');

for teamSet in nDict['School']:
    if sIndx < 1230:
        sIndx = sIndx + 1
        continue
    sIndx = sIndx + 1
    a=0
    teamName = teamSet['option']
    teamValue = teamSet['value']
    #print teamSet
    for yearSet in nDict['Year']:
        payloads = []
        if a < 5:
            a = a + 1
            yearRange = yearSet['option']
            yearValue = yearSet['value']
            #print yearSet
        else:
            continue

        #for team in teamList:
        #    for year in yearList: # last 5 years, maybe graph of win/loss of career?
        teamSelect = Select(driver.find_element_by_name('searchOrg'))
        teamSelect.select_by_value(teamValue)
        yearSelect = Select(driver.find_element_by_name('academicYear'))
        yearSelect.select_by_value(yearValue)
        # Search for team on given year
        driver.find_element_by_name('teamSearch').find_elements_by_class_name('button')[0].click()

        functionsForThisSearch = []

        # Get all results on page before proceeding
        ListlinkerHref = driver.find_elements_by_xpath("//*[@href]") # separate results by links, should be number of entries aka number of sports
        for item in ListlinkerHref:
            if item.text == teamName: # if link is the team we're at in loop
                #print item.text
                #print item.get_attribute('href')
                functionsForThisSearch.append(item.get_attribute('href'))

        for function in functionsForThisSearch:
            try:
                driver.execute_script(function)
            except:
                driver.back()
                print 'couldnt execute script'
                continue
            try:
                selectionInfo = driver.find_element_by_class_name('foregroundtitle').text
            except:
                driver.back()
                print 'couldnt get foreground title'
                continue
            infoArray = re.split('\n', selectionInfo)
            mTeam = infoArray[0]
            mSeason = infoArray[1][0:7]
            mSport = infoArray[1][8:]
            mDivision = infoArray[2]
            ListlinkerHref3 = driver.find_elements_by_xpath('//td[@width="*"]')
            try:
                teamLink = ListlinkerHref3[0]
            except:
                teamLink = ''
            try:
                coachLink = ListlinkerHref3[1]
                coachName = coachLink.text
            except:
                coachName = "Unknown"
            #print mTeam,',',mSport,',',mSeason,',',mDivision,':',coachName
            payload = {'team':mTeam, 'sport':mSport, 'year':mSeason,'coach':coachName,'division':mDivision}
            payloads.append(payload)
            driver.back()
            it = it + 1
        errors = 0
        for payload in payloads:
            r = requests.post('http://ythogh.com/lrt/add_team.php',params=payload)
            #print r.url
            if r.status_code != 200:
                errors = errors + 1
                print 'Error sending:', r.url
            #print r.url
        print len(payloads), 'entries added from', teamName ,'with ',errors,'errors.'
    print 'School',teamName,'at index',sIndx,'finished.'
print '***************************************************************'
print 'Crawling has finished after ',it, 'pages!'
print '***************************************************************'
driver.quit()
