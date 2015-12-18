import urllib2, pprint, string
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

mData = ""
mDict = {}
mTag = ""
rightAfterOption = False
aliases = {'Tex.':'Texas', 'St.':'Saint', 'N.C.':'North Carolina', 'S.C.':'South Carolina', 'N.M.':'New Mexico', 'Mt.':'Mount', 'Mo.':'Missouri', 'Minn.':'Minnesota', 'Me.':'Maine',
           'La.':'Louisiana', 'Ga.':'Georgia', 'Frank.':'Franklin', 'Fla.':'Florida', 'Col.':'Colorado', 'Colo.':'Colorado', 'Cal':'California', 'Poly':'Polytechnic', 'BYU':'Bringham Young University'}

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

