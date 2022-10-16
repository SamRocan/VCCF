import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class StatistaGraph:
    def __init__(self, URL):

        self.URL = URL
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
                for index, key in enumerate(self.chartData.keys()):
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
    query = str(query).replace(' ','+')
    url = 'https://www.statista.com/search/?q='+query+'&Search=&qKat=search&newSearch=true&p=1&sortMethod=popularity'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(url)
    page_source = driver.page_source.encode("utf-8")
    searchSoup = BeautifulSoup(page_source, 'html.parser')
    regex = re.compile('.*searchItem--.*')
    searchlinkList = searchSoup.find_all("a", {"data-gtm":regex})
    print(query)
    print(len(searchlinkList))
    print('-----------')
    finalLinkList = {}
    topicList = []
    for i in searchlinkList:
        if "statisticBasis" in str(i):
            print(i.find("div",{"class":"itemContent__subline"}).text.strip())
            element = i['href']
            finalLinkList[i.find("div",{"class":"itemContent__subline"}).text.strip()] = element
        if "/topics/" in str(i):
            topicList.append(i)
    driver.quit()
    return finalLinkList

