import time

import requests
from bs4 import BeautifulSoup


class StatistaGraph:
    def __init__(self, URL):
        self.URL = URL
        print(self.URL)
        preConTime = time.time()
        self.soup = BeautifulSoup(requests.get(URL).content, 'html.parser')
        print("conn time: " + str(time.time() - preConTime))
        rows = self.soup.select('#statTableHTML tr')
        heading = self.soup.find("h2", {"class":"sectionHeadline"})
        title = heading.text.strip()
        #4 types expected: bar, line, pie and table
        chartType = self.soup.find("meta", {"id":"gtm_stat_graphType"})
        #print(title)
        chartType = str(chartType['data-page'])
        #print(chartType)
        self.chartType = chartType
        self.chartData = {}

        #Make a multiDepth array of values
        #

        for i in rows:
            if('<th>' in str(i)):
                chartHeadingInfo = i.findAll('th')
                for i in chartHeadingInfo:
                    self.chartData[i.text] = []
            else:
                values = i.findAll('td')
                for index, key in enumerate(self.chartData.keys()) :
                    if(index > 0):
                        value = values[index].text.strip().replace(',','')
                        if('%' in  value):
                            value = float(values[index].text.strip().replace(',','').replace('%',''))
                        if('-'==value):
                            value=None
                        else:

                            value = float(value)
                        self.chartData[key].append(value)

                    else:
                        self.chartData[key].append(values[index].text.strip())
        self.chartData['type'] = chartType
        #print(self.chartData)
        try:
            #print(len(self.chartData['Characteristic']))
            if(chartType == 'line' or len(self.chartData['Characteristic']) > 100):
                for x in range(len(self.chartData.keys())-1):
                    key = list(self.chartData.keys())[x]
                    self.chartData[key].reverse()
        except:
            pass

    def getGraphData(self):
        return self.chartData


def searchStatista(query):
    url = 'https://www.statista.com/search/?q='+query+'&Search=&qKat=search'
    searchSoup = BeautifulSoup(requests.get(url).content, 'html.parser')
    searchlinkList = searchSoup.find_all("li", {"class":"list__item--searchContentTypeTopic"})
    return searchlinkList

def soupToLink(resultSetList):
    links = []
    for i in resultSetList:
        loc1 = str(i).find("href")
        loc2 = str(i).find("title")
        links .append(str(i)[loc1+6:loc2-2])
    return links

def getLinks(linkList):
    premiumStatisticLinks = []
    basicStatisticLinks = []
    topicLinks = []

    for i in range(len(linkList)):
        if("searchContentTypeStatistic" in str(linkList[i])):
            if("iconSprite--statisticPremium" in str(linkList[i])):
                element = linkList[i].find_all('a', href=True)
                premiumStatisticLinks.append(element)
            if("iconSprite--statisticBasis" in str(linkList[i])):
                element = linkList[i].find_all('a', href=True)
                basicStatisticLinks.append(element)

    basicStatPage = soupToLink(basicStatisticLinks)
    premiumStatPage = soupToLink(premiumStatisticLinks)
    topicPage = soupToLink(topicLinks)
    print("Stats")
    print(len(basicStatPage))
    print("Topics")
    print(topicPage)
    print("------")
    return(basicStatPage)


def topicSearch(query):
    links = searchStatista(query)
    topics = []
    #Gets all topics
    for i in links:
        if 'href="/topics/' in str(i):
            print(i.find("a")["href"])
            topics.append(i.find("a")["href"])
    return topics

def topicInfo(link):
    topicInfoRes = {}
    soup = BeautifulSoup(requests.get(link).content, 'html.parser')

    #and key facts on the page
    keyFactsTitles = soup.findAll("div", {"class":"fancyBox__title"})
    keyFactsValues = soup.findAll("div", {"class":"fancyBox__content"})

    for title, value in zip(keyFactsTitles, keyFactsValues):
        topicInfoRes[title.text.strip()] = value.text.strip()
    return topicInfoRes
