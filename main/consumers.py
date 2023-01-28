import json
from random import randint
from channels.generic.websocket import WebsocketConsumer
from VCCF.tasks import getAPI, extractVariables, twitterImages, companyInfo, graphScraping,getNews
from .models import Company

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("----LATEST----")
        print(Company.objects.all())
        company = Company.objects.latest('updated_at')
        slug = str(company.slug)
        apiContent = getAPI(slug)
        print("----API CONTENT----")
        print(apiContent)
        self.send(json.dumps({'title':'Loading Variables','message':20}))
        variables = extractVariables(apiContent)
        print("----VARIABLES---")
        print(variables)
        self.send(json.dumps({'title':'Loading Twitter Data','message':40}))
        twitterZip = twitterImages(slug, variables['TwitterHandles'])
        print("----TWITTER INFO---")
        print(twitterZip)
        self.send(json.dumps({'title':'Loading Website Data','message':60}))
        print("----WEBSITE DATA---")
        websiteData = companyInfo(variables['results'])
        print(websiteData)
        print("----NEWS DATA---")
        news = getNews(variables['results'])
        for article in news:
            print(article['title'])
            print(article['url'])
            print('------------')
        self.send(json.dumps({'title':'Loading Graph Data','message':80}))
        graphData = graphScraping(variables['topics'])
        print("----GRAPH DATA---")
        print(graphData)
        self.send(json.dumps({'title':'Finished!','message':100}))

        newComp = Company(slug=slug,
                          api=apiContent,
                          variables=variables,
                          twitterZip=twitterZip,
                          websiteData=websiteData,
                          graphData=graphData,
                          newsArticles=news)
        newComp.save()
        print("Company Created")


