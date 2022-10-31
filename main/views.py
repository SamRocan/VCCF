import os
import time

from django.shortcuts import render,redirect
import requests
import json, itertools
from rest_framework.views import APIView
from rest_framework.response import Response
from selenium import webdriver
from django.contrib.sessions.backends.db import SessionStore

from .LIWC import getExcel, getTweets, tokenize, dic_to_dict, makeTrie, bestMatch, getScore
from scraper.scraper import *
from scraper.GitHub import GitHub
from scraper.SaaSWorthy import SaaSWorthy
from scraper.YCombinator import YCombinator
from scraper.SaasHub import SaasHub
from scraper.Statista import *
import tweepy as tw

# Create your views here.
#To view logs: docker logs vccf_web_1
from django.urls import reverse

from VCCF import settings


def index(request):
    return render(request, 'main/index.html')

def product(request):
    request.session['productSlug'] = request.GET["productSearch"]
    #return redirect('productHome', productSlug=request.GET["productSearch"])
    return redirect('loading')

def loading(request):
    return render(request, 'main/loading.html')

def productHome(request, productSlug):
    #Need to break tasks down into chunks to allow smooth update
    #Need to find way to send context / session from consumers to here
    time.sleep(5)
    print(request.session["testSession"])
    context = {}
    return render(request, 'main/product.html', context)

class ChartData(APIView):

    def get(self, request, format = None):
        data = ["sent data"]

        '''Twitter 5 Factor'''
        extScore = []
        neuScore = []
        agrScore = []
        conScore = []
        opnScore = []
        TwitterHandles = request.session["TwitterHandles"]
        for handle in TwitterHandles:
            userName = handle
            module_dir = os.path.dirname('resources/')
            all_users = os.path.join(module_dir, 'combined_users.xlsx')
            user_scores = os.path.join(module_dir, 'user_scores.xlsx')
            liwc_dic = os.path.join(module_dir, 'LIWC2007_Ammended.dic')
            start_time = time.time()

            data = getExcel(all_users)
            score_data = getExcel(user_scores)
            try:
                twitterContent = getTweets(userName)


                tokenizedTweets = tokenize(twitterContent)

                dictionary = dic_to_dict(liwc_dic)

                trie = makeTrie(dictionary)

                values = []
                for i in tokenizedTweets[0]:
                    value = trie.lookup(i)
                    for i in value:
                        if(isinstance(i, int)):
                            values.append(i)
                try:
                    match = bestMatch(data, values)
                except:
                    message = "Analysis cannot be preformed on this account. This is usually due to the account " \
                              "primarily being in a language other than English, or the Twitter API rate limit being reached." \
                              "Please try another account, or wait and try again later. "
                    return render(request, 'main/noTwitter.html', {'message':message})

                profile = list(match.keys())[0]
                scores = getScore(score_data, profile)

                scoresVar = scores[0]
                catVar = scores[1]
                fiveFactors = ["Extraversion", "Neuroticism", "Agreableness", "Concientiousness", "Openness"]

                extScore.append(scoresVar[0])
                neuScore.append(scoresVar[1])
                agrScore.append(scoresVar[2])
                conScore.append(scoresVar[3])
                opnScore.append(scoresVar[4])
            except:
                extScore.append(0)
                neuScore.append(0)
                agrScore.append(0)
                conScore.append(0)
                opnScore.append(0)
        ext = "Extroversion (" + str(catVar[0]) + ")"
        neu = "Neuroticism (" + str(catVar[1]) + ")"
        agr = "Agreeableness (" + str(catVar[2]) + ")"
        con = "Conscientiousness (" + str(catVar[3]) + ")"
        opn = "Openness (" + str(catVar[4]) + ")"

        '''Statista Scraping'''
        '''Use 'akaunting' to test'''
        allGraphs = request.session['allGraphs']
        print("---ALL Graphs")
        print(allGraphs)
        data = {
            'extScore':extScore,
            'neuScore':neuScore,
            'agrScore':agrScore,
            'conScore':conScore,
            'opnScore':opnScore,
            'ext':ext,
            'neu':neu,
            'agr':agr,
            'con':con,
            'opn':opn,
            'founderName':userName,
            'allGraphs':allGraphs
        }

        return Response(data)