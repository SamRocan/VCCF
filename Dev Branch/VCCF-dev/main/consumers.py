import json
from random import randint
from channels.generic.websocket import WebsocketConsumer
from django.contrib.sessions.backends.db import SessionStore
from VCCF.tasks import getAPI, extractVariables, twitterImages, companyInfo, graphScraping
from .models import Company

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("----LATEST----")
        company = Company.objects.latest('api')
        slug = company.slug
        apiContent = getAPI(slug)
        print("----API CONTENT----")
        print(apiContent)
        self.send(json.dumps({'message':20}))
        variables = extractVariables(apiContent)
        print("----VARIABLES---")
        print(variables)
        self.send(json.dumps({'message':40}))
        twitterZip = twitterImages('gitlab', variables['TwitterHandles'])
        print("----TWITTER INFO---")
        print(twitterZip)
        self.send(json.dumps({'message':60}))
        print("----WEBSITE DATA---")
        websiteData = companyInfo(variables['results'])
        print(websiteData)
        self.send(json.dumps({'message':80}))
        graphData = graphScraping(variables['topics'])
        print("----GRAPH DATA---")
        print(graphData)
        self.send(json.dumps({'message':100}))

        newComp = Company(slug=slug,
                          api=apiContent,
                          variables=variables,
                          twitterZip=twitterZip,
                          websiteData=websiteData,
                          graphData=graphData)
        newComp.save()
        print("Company Created")


