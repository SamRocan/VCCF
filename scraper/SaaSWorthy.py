import requests
from bs4 import BeautifulSoup


class SaaSWorthy:
    def __init__(self, url):
        self.url = url
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def getSubHeading(self):
        subhead = self.soup.find(class_='h-sub-head').text
        return subhead

    def getScore(self):
        score = self.soup.find(class_='pop_score_d').text
        retval = ''
        for i in score:
            if(i != '%'):
                retval +=i
            else:
                return retval.strip()

    def getDescription(self):
        desc = self.soup.find(class_='sass-desc').findChildren("p", recursive=False)[1].text.strip()
        return desc

    def getSocialMediaCount(self):
        socials = self.soup.findAll(class_='flwrs-row')
        retVal = []
        print(socials)
        for i in range(len(socials)):
            if(i>0):
                if(socials[i].text.strip() !=''):
                    retVal.append(int(socials[i].text.strip().replace(',','')))
                else:
                    retVal.append(0)
        return retVal

    def getFeatures(self):
        features = []
        for i in self.soup.find("div", {"id": "features"}).findAll("li"):
            features.append(i.text)
        return features

    def getTableInfo(self):
        tableDict = {}
        cells = self.soup.find("table", {"class": "tech-det-table"}).findAll("td")
        currentCell = None
        for i in cells:
            if('tech-title' in str(i)):
                if(currentCell!=None):
                    tableDict[currentCell][0].split("\n")
                tableDict[i.text] = []
                currentCell = i.text
            else:
                if('fa fa-check-circle-o' in str(i)):
                    tableDict[currentCell].append('YES')
                elif(currentCell == 'API'):
                    tableDict[currentCell].append('NO')
                else:
                    tableDict[currentCell].append(i.text.strip())
        for i in tableDict:
            tableDict[i] = tableDict[i][0].split("\n")
        return tableDict

    def getPricingPlans(self):
        #Split on:
        #$num after free
        #custom after $num
        plans = self.soup.findAll("div", {"class":"plans-div"})
        plansDict = {}
        for plan in plans:
            #print("-----")
            planName = plan.find("span", {"class":"plan-title"}).text.strip()
            planVals  = plan.find("div", {"class":"pricing"}).text.strip().split("\n")
            planDesc = plan.find("div", {"class":"pln-desc"})
            featList = planDesc.findAll("li")
            featListFinal = []
            for i in featList:
                featListFinal.append(i.text.strip())
            if len(planVals) >= 4:
                plansDict[planName] = [[planVals[0], planVals[2]], [planVals[1], planVals[3]], featListFinal]
            else:
                plansDict[planName] = [planVals, featListFinal]
            print("---")

        return plansDict

