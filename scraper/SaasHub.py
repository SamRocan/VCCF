import requests
from bs4 import BeautifulSoup


class SaasHub:
    def __init__(self, url):
        self.url = url
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def getMentions(self):
        QA = {}
        mentions = self.soup.findAll(class_='mention')
        for i in mentions:
            Q = str(i.find('strong').text).strip()
            val = str(i.find('blockquote').text)
            end = val.find('- Source:')
            A = val[:end].strip()
            QA[Q] = A
        return QA

    def getSources(self):
        SL = {}
        sources = self.soup.findAll(class_='column is-half-desktop is-full-tablet space-y-2')
        for i in sources:
            #print(i.find('strong').text)
            print(i.find('a')['href'])
            print(i.find('a').text)
            print(i.find(class_='description text-sm').text)
            print("----")
            SL[i.find('a').text] = 'https://www.saashub.com'+i.find('a')['href']
        return SL