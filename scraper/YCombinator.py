import requests
from bs4 import BeautifulSoup


class YCombinator:
    def __init__(self, url):
        self.url = url
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def getOverview(self):
        overview = self.soup.find(class_="text-xl")
        return overview.text

    def getBadges(self):
        badges = self.soup.findAll(class_="ycdc-badge")
        for badge in badges:
            if 'Y Combinator Logo' in  badge.text:
                return badge.text.replace('Y Combinator Logo', '')
            else:
                return badge.text

    def getFounders(self):
        res = self.soup.findAll(class_="leading-snug")
        founders = []
        for i in res:
            founder = []
            name = i.find(class_="font-bold")
            name = name.text
            founder.append(name)
            position = i.findAll('div')
            founder.append(position[1].text)
            founders.append(founder)

        return founders

    def getJobsHiring(self):
        jobs = []
        res = self.soup.findAll(class_="flex flex-row justify-between w-full py-4")
        for i in res:
            job = {}
            title = i.find(class_="text-lg font-bold pr-4 ycdc-with-link-color")
            job['positon'] = title.text
            dets = i.findAll(class_="capitalize list-item list-square first:list-none")
            for z in range(len(dets)):
                job['requirements'] = dets[z].text
            jobs.append(job)
        return jobs

    def getKeyInfo(self):
        keyInfo = []
        info = self.soup.findAll(class_="flex flex-row justify-between")
        if('class="prose"' in str(info[0])):
            info.pop(0)
        for i in info:
            keyInfo.append(i.find_all('span')[1].text)
        return keyInfo

    def getNews(self):
        newsInfo = [[],[]]
        news = self.soup.find("div", {"id": "news"})
        articles = news.findAll("a")
        for article in articles:
            print("------")
            newsInfo[0].append(article.text)
            newsInfo[1].append(article['href'])
        return newsInfo