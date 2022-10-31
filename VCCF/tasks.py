import itertools
import json

import requests
from celery import shared_task

#To get sessions from outside of views
from django.contrib.sessions.backends.db import SessionStore

#@shared_task()
from VCCF import settings
from scraper.GitHub import GitHub
from scraper.SaaSWorthy import SaaSWorthy
from scraper.SaasHub import SaasHub
from scraper.Statista import searchStatista, StatistaGraph
from scraper.YCombinator import YCombinator
from scraper.scraper import githubResults, crunchBaseResults, saasWorthyResults, linkedInResults, yCombinatorResults, \
    apolloIOResults, saasHubResults
import tweepy as tw

@shared_task()
def getAPI(productSlug):

    API_URL = "https://api.producthunt.com/v2/api/graphql"

    '''API Code'''


    MY_API_TOKEN = "PbEz8mWhaMzYy1J8WwS-X2-YXi92xhRffQS3YDi3xl4"
    slug = productSlug

    #API Connsumed
    query = {"query":
                 """
                 query FindBySlug {
                 post(slug:"""+ "\""+ slug +"\"" + """){
                        commentsCount
                        comments(first:5){
                            edges{
                                node{
                                    body
                                }
                            }
                        }
                        description
                        makers{
                            name
                            username
                            twitterUsername
                            profileImage                        
                        }
                        media{
                            url
                        }
                        name
                        productLinks{
                            url
                        }
                        slug
                        tagline
                        thumbnail{
                            url
                        }
                        topics(first:5){
                            edges{
                                node{
                                    name
                                }
                            }
                        }
                        website
                    }
                }
            """}

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + MY_API_TOKEN,
        'Host': 'api.producthunt.com'
    }
    #Gets information in form of JSON
    posts = requests.post(API_URL,
                          headers=headers,
                          data=json.dumps(query))

    #Saves Json information to variable
    jsonInfo = posts.json()
    return jsonInfo

def extractVariables(jsonIput):
    if (jsonIput['data']['post'] == None):
        print("None found")
        return "None Found"
    results = {}
    topics =[]
    global Names
    Names = []
    global TwitterHandles
    TwitterHandles = []
    phUrls = []
    profilePics = []

    #Gets specific information requred from jsonInfo
    for i in jsonIput['data']['post']:
        if(i=='makers'):
            for y in jsonIput['data']['post']['makers']:
                TwitterHandles.append(y['twitterUsername'])
                Names.append(y['name'])
                phUrls.append(y['username'])
                profilePics.append(y['profileImage'])
        if(i=='media'):
            for y in jsonIput['data']['post']['media']:
                #print(y['url'])
                pass
        if(i=='productLinks'):
            for y in jsonIput['data']['post']['productLinks']:
                #print(y['url'])
                pass
        if(i=='thumbnail'):
            logo = str(jsonIput['data']['post'][i]['url'])
        if(i=='topics'):
            for y in jsonIput['data']['post']['topics']['edges']:
                topics.append(y['node']['name'])
        results[i] = str(jsonIput['data']['post'][i])

    socialMediaZip = zip(Names,TwitterHandles, phUrls, profilePics)
    return [results, topics, logo, TwitterHandles, socialMediaZip]

def twitterImages(slug, TwitterHandles):
    product_name = slug.capitalize()

    #Get Twitter Image
    userImages = []
    for handle in TwitterHandles:
        auth = tw.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)
        try:
            user = api.get_user(screen_name=handle)
            url = str(user.profile_image_url)
            userImage = url.replace("_normal", "")
        except:
            userImage = 'https://www.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png'
        userImages.append(userImage)
        #print(userImage)

    twitterZip = zip(TwitterHandles, userImages)
    return twitterZip

def companyInfo(results):
    companyName = str(results.get('name'))

    '''Topics sent for use with Statista graphs'''

    '''Scraping Other Websites'''

    githubInfo = githubResults(companyName)
    crunchBaseInfo = crunchBaseResults(companyName)
    saasWorthyInfo = saasWorthyResults(companyName)
    linkedInInfo = linkedInResults(companyName)
    yCombinatorInfo = yCombinatorResults(companyName)
    apolloIOInfo = apolloIOResults(companyName)
    saasHubInfo = saasHubResults(companyName)
    if(len(githubInfo) != 2):
        print("No Github Found")
        git = None
        print(githubInfo)
    else:
        git = GitHub(githubInfo[1])
        try:
            git.getCommits()
        except:
            git = None

    if(len(crunchBaseInfo)!= 2):
        print("No Crunchbase Found")
        crunchBaseInfo = None

    if(len(linkedInInfo)!=2):
        print("No LinkedIn Found")
        linkedInInfo = None

    print(yCombinatorInfo)
    if(len(yCombinatorInfo) != 2):
        print("No YCombinator Found")
        ycombinator = None
        print(yCombinatorInfo)
    else:
        ycombinator = YCombinator(yCombinatorInfo[1])
        try:
            ycombinator.getOverview()
        except:
            ycombinator = None

    if(len(apolloIOInfo)!=2):
        print("No Apollo.IO Found")
        apolloIOInfo = None

    if(len(saasHubInfo) !=2):
        print("No SaasHubInfo")
        saasHub = None
        print(saasHubInfo)
    else:
        saasHub = SaasHub(saasHubInfo[1])


    print("INFO: " + str(saasWorthyInfo))
    if(len(saasWorthyInfo) !=2):
        print("No SassWorthy Found")
        saasWorthy = None
        print(saasWorthyInfo)
    else:
        saasWorthy = SaaSWorthy(saasWorthyInfo[1])
    return [git,crunchBaseInfo,ycombinator, apolloIOInfo, saasHub, saasWorthy]

    '''Statista Graph Scraping'''
def graphScraping(topics):
    #search statista for topics
    print(topics)
    topicLinkDic = {}
    for topic in topics:
        topicDic = searchStatista(topic)
        topicDic = dict(itertools.islice(topicDic.items(), 2))
        print(len(topicDic))
        topicLinkDic.update(topicDic)
    print(topicLinkDic)


    graphNames = list(topicLinkDic.keys())
    graphNames = enumerate(graphNames)
    allGraphs = []
    lastTime = None
    for graphLink in topicLinkDic.values():
        URL = 'http://statista.com' + graphLink
        statistaGraph = StatistaGraph(URL)
        #print(statistaGraph.getGraphData())
        statGraphData = statistaGraph.getGraphData()
        retData = []
        retData.append(list(statGraphData.keys()))
        for key in statGraphData.keys():
            retData.append(statGraphData[key])
        #print(retData)
        allGraphs.append(retData)

    noOfGraphs = len(allGraphs)
    return [graphNames, allGraphs, noOfGraphs]

