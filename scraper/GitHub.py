import requests
from bs4 import BeautifulSoup


class GitHub:
    def __init__(self, url):
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')


    #Github used https://github.com/akaunting/akaunting#readme
    def getCommits(self):
        commits = self.soup.find_all("div", {"class": "js-details-container"})[0].find("strong")
        print(commits.text)

    def getLastUpdate(self):
        last_update = self.soup.findAll("relative-time", {"class": "no-wrap"})
        print(last_update)
        print(last_update[0].text)

    def getBranches(self):
        git_file_info = self.soup.findAll("a", {"data-pjax":"#repo-content-pjax-container"})
        arr = []
        for line in git_file_info:
            if('branches' in str(line)):
                arr.append(line.text.strip())
        branches = int(arr[1][:1])
        print(branches)

    def getLanguages(self):
        languages = self.soup.findAll("a", {"data-ga-click":"Repository, language stats search click, location:repo overview"})
        retVal = []
        for i in languages:
            val = i.text.strip()
            word = ""
            for z in val:
                #split where ord = 10 aka a Line Feed
                if(ord(z)!=10):
                    word+=z
                else:
                    retVal.append(word)
                    word=""

                if(z=='%'):
                    retVal.append(word)
                    word=""
        finalVals = []
        language = []
        for i in range(0, len(retVal)):
            language.append(retVal[i])
            if(len(language)==2):
                finalVals.append(language)
                language=[]
        print(finalVals)

    def stringToNum(str):
        retNum = ''
        multiplier = 1
        for i in str:
            if(i.isnumeric() or i == '.'):
                retNum +=i
            if(i == 'k'):
                multiplier = 1000
        retNum = float(retNum) * multiplier
        return retNum

    def getStats(self):
        about = self.soup.find('div', {'class':'BorderGrid-cell'})
        retVal = []
        for i in about:
            if('<strong>' in str(i)):
                word = i.text.strip()
                for z in word:
                    if(ord(z)==32 or ord(z)!=10):
                        retVal.append(word)
                        word=""
                    else:
                        word+=z
        finList1 = []
        for i in retVal:
            if(i!='' and str(i)!='\n'):
                finList1.append(i)

        finList2 = []
        for i in finList1:
            z = i.replace('\n   ', '')
            finList2.append(z)
        finListFin = []
        for i in finList2:
            z = i.split()
            finListFin.append(z[0])
        print(finList2)
        print(finListFin)
        numList = []
        for i in finListFin:
            numList.append(stringToNum(i))
        return numList

    def getTags(self):
        tags = self.soup.findAll('a', {'data-ga-click':'Topic, repository page'})
        print(len(tags))
        retList = []
        for i in tags:
            retList.append(i.text.strip())
        return retList

    def getReadMe(self):
        readMe = self.soup.find('div', {'data-target':'readme-toc.content'})
        return readMe #add .text to only get text and not html
