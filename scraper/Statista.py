import requests
from bs4 import BeautifulSoup


class StatistaGraph:
    def __init__(self, URL):
        self.URL = URL
        print(self.URL)
        self.soup = BeautifulSoup(requests.get(URL).content, 'html.parser')
        rows = self.soup.select('#statTableHTML tr')
        heading = self.soup.find("h2", {"class":"sectionHeadline"})
        title = heading.text.strip()
        #4 types expected: bar, line, pie and table
        chartType = self.soup.find("meta", {"id":"gtm_stat_graphType"})
        print(title)
        chartType = str(chartType['data-page'])
        print(chartType)
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
        print(self.chartData)
        try:
            print(len(self.chartData['Characteristic']))
            if(chartType == 'line' or len(self.chartData['Characteristic']) > 100):
                for x in range(len(self.chartData.keys())-1):
                    key = list(self.chartData.keys())[x]
                    self.chartData[key].reverse()
        except:
            pass

    def getGraphData(self):
        return self.chartData