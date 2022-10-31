import json
from random import randint
from channels.generic.websocket import WebsocketConsumer
from django.contrib.sessions.backends.db import SessionStore
from VCCF.tasks import getAPI, extractVariables, twitterImages, companyInfo, graphScraping


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        apiContent = getAPI('gitlab')
        self.send(json.dumps({'message':20}))
        variables = extractVariables(apiContent)
        self.send(json.dumps({'message':40}))
        twitterZip = twitterImages('gitlab', variables[3])
        self.send(json.dumps({'message':60}))
        websiteData = companyInfo(variables[0])
        self.send(json.dumps({'message':80}))
        graphData = graphScraping(variables[1])
        self.send(json.dumps({'message':100}))
        # Maybe consider saving this data into a django model
        self.scope["session"]["testSession"] = 5
        self.scope["session"].save()




