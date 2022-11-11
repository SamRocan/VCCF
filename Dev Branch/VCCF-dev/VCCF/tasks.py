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


    MY_API_TOKEN = "dfEjn2P-eAeNqApqL14eZGOuji8awzEBWmHM1BaA-FM"
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

    socialMedia = [Names,TwitterHandles, phUrls, profilePics]
    retDict = {
                'results':results, 'topics':topics, 'logo':logo,
                'TwitterHandles':TwitterHandles, 'socialMedia':socialMedia
               }
    retJSON = json.dumps(retDict)
    loadedJSON = json.loads(retJSON)
    return loadedJSON

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

    twitterZip = [TwitterHandles, userImages]
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
            gitCommits = git.getCommits()
        except:
            gitCommits = None

        try:
            gitLastUpdate = git.getLastUpdate()
        except:
            gitLastUpdate = None

        try:
            gitBranches = git.getBranches()
        except:
            gitBranches = None

        try:
            gitLanguages = git.getLanguages()
        except:
            gitLanguages = None

        try:
            gitStats = git.getStats()
        except:
            gitStats = None

        try:
            gitTags = git.getTags()
        except:
            gitTags = None

        try:
            gitReadMe = git.getReadMe()
        except:
            gitReadMe = None

        git = [
            gitCommits, gitLastUpdate, gitBranches, gitLanguages,
            gitStats, gitTags, gitReadMe
        ]

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
            ycombinatorOverview = ycombinator.getOverview()
        except:
            ycombinatorOverview = None

        try:
            ycombinatorBadges = ycombinator.getBadges()
        except:
            ycombinatorBadges = None

        try:
            ycombinatorFounders = ycombinator.getFounders()
        except:
            ycombinatorFounders = None

        try:
            ycombinatorJobsHiring = ycombinator.getJobsHiring()
        except:
            ycombinatorJobsHiring = None

        try:
            ycombinatorgetKeyInfo = ycombinator.getKeyInfo()
        except:
            ycombinatorgetKeyInfo = None

        try:
            ycombinatorgetNews = ycombinator.getNews()
        except:
            ycombinatorgetNews = None

        ycombinator = [ycombinatorOverview, ycombinatorBadges, ycombinatorFounders,
                       ycombinatorJobsHiring, ycombinatorgetKeyInfo, ycombinatorgetNews]

    if(len(apolloIOInfo)!=2):
        print("No Apollo.IO Found")
        apolloIOInfo = None

    if(len(saasHubInfo) !=2):
        print("No SaasHubInfo")
        saasHub = None
        print(saasHubInfo)
    else:
        saasHub = SaasHub(saasHubInfo[1])
        try:
            saasHubMentions = saasHub.getMentions()
        except:
            saasHubMentions = None

        try:
            saasHubSources = saasHub.getSources()
        except:
            saasHubSources = None

        saasHub = [saasHubMentions, saasHubSources]

    print("INFO: " + str(saasWorthyInfo))
    if(len(saasWorthyInfo) !=2):
        print("No SassWorthy Found")
        saasWorthy = None
        print(saasWorthyInfo)
    else:
        saasWorthy = SaaSWorthy(saasWorthyInfo[1])
        try:
            saasWorthyScore = saasWorthy.getScore()
        except:
            saasWorthyScore = None

        try:
            saasWorthySubHeading = saasWorthy.getSubHeading()
        except:
            saasWorthySubHeading = None

        try:
            saasWorthyPricingPlans = saasWorthy.getPricingPlans()
        except:
            saasWorthyPricingPlans = None

        try:
            saasWorthyTableInfo = saasWorthy.getTableInfo()
        except:
            saasWorthyTableInfo = None

        try:
            saasWorthyFeatures = saasWorthy.getFeatures()
        except:
            saasWorthyFeatures = None

        try:
            saasWorthyDescription = saasWorthy.getDescription()
        except:
            saasWorthyDescription = None

        try:
            saasWorthySocialMediaCount = saasWorthy.getSocialMediaCount()
        except:
            saasWorthySocialMediaCount = None

        saasWorthy = [  saasWorthyScore,saasWorthySubHeading, saasWorthyPricingPlans,
                        saasWorthyTableInfo, saasWorthyFeatures, saasWorthyDescription,
                        saasWorthySocialMediaCount]
    return [git,crunchBaseInfo,linkedInInfo, ycombinator, apolloIOInfo, saasHub, saasWorthy]

def statistaSearcher(topic, count):
    topicDic = {}
    try:
        topicDic = searchStatista(topic)
    except:
        print("EXCEPTION CAUGHT: TRYING AGAIN")
        count+=1
        if count<5:
            statistaSearcher(topic, count)
        else:
            print("Too many errors, returning as is")
            return topicDic
    return topicDic

    '''Statista Graph Scraping'''
def graphScraping(topics):
    #search statista for topics
    print(topics)
    topicLinkDic = {}
    for topic in topics:
        topicDic = statistaSearcher(topic, 0)
        #topicDic = searchStatista(topic)
        topicDic = dict(itertools.islice(topicDic.items(), 2))
        print(len(topicDic))
        topicLinkDic.update(topicDic)
    print(topicLinkDic)


    graphNames = list(topicLinkDic.keys())
    retGraphName = [[],[]]
    for i in range(len(graphNames)-1):
        retGraphName[0].append(i)
        retGraphName[1].append(graphNames[i])
    #graphNames = enumerate(graphNames)
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

