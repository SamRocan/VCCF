import os
import time

from django.shortcuts import render,redirect
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
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
    print(request.GET["productSearch"])
    return redirect('productHome', productSlug=request.GET["productSearch"])

def productHome(request, productSlug):

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
    if (jsonInfo['data']['post'] == None):
        print("None found")
        return render(request, 'main/productNotFound.html')
    results = {}
    topics =[]
    global Names
    Names = []
    global TwitterHandles
    TwitterHandles = []
    phUrls = []
    profilePics = []

    #Gets specific information requred from jsonInfo
    for i in jsonInfo['data']['post']:
        if(i=='makers'):
            for y in jsonInfo['data']['post']['makers']:
                TwitterHandles.append(y['twitterUsername'])
                Names.append(y['name'])
                phUrls.append(y['username'])
                profilePics.append(y['profileImage'])
        if(i=='media'):
            for y in jsonInfo['data']['post']['media']:
                #print(y['url'])
                pass
        if(i=='productLinks'):
            for y in jsonInfo['data']['post']['productLinks']:
                #print(y['url'])
                pass
        if(i=='thumbnail'):
            logo = str(jsonInfo['data']['post'][i]['url'])
        if(i=='topics'):
            for y in jsonInfo['data']['post']['topics']['edges']:
                topics.append(y['node']['name'])
        results[i] = str(jsonInfo['data']['post'][i])


    '''Twitter Code'''

    socialMediaZip = zip(Names,TwitterHandles, phUrls, profilePics)
    request.session["TwitterHandles"] = TwitterHandles
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

    '''Statista Graph Scraping'''


    topicLinkDic = {}
    #gets list of topic pages, currently for first topic
    for topic in topics:
        topicResults = topicSearch(topic)
        for topicPage in topicResults:
            #gets first topic page
            URL = 'https://www.statista.com' + str(topicPage)
            soup = BeautifulSoup(requests.get(URL).content, 'html.parser')
            linkList = soup.find_all("a", {"class":"list__itemWrap dossierSummary__link text--linkReset"})
            #Gets all non-premium statistics of first topic page
            for link in linkList:
                if('iconSprite--statisticPremium' not in str(link)):
                    print(str(link.text) + " : " + str(link["href"]))
                    topicLinkDic[link.text] = link["href"]
                    print("------")
            print(topicInfo(URL))

    print(topicLinkDic)

    graphNames = list(topicLinkDic.keys())
    graphNames = enumerate(graphNames)
    allGraphs = []
    for graphLink in topicLinkDic.values():
        URL = 'http://statista.com' + graphLink
        statistaGraph = StatistaGraph(URL)
        print(statistaGraph.getGraphData())
        statGraphData = statistaGraph.getGraphData()
        retData = []
        retData.append(list(statGraphData.keys()))
        for key in statGraphData.keys():
            retData.append(statGraphData[key])
        allGraphs.append(retData)

    noOfGraphs = len(allGraphs)

    request.session['allGraphs'] = allGraphs

    context = {
        'results':results,
        'topics':topics,
        'logo':logo,
        'names':Names,
        'socialMediaZip':socialMediaZip,
        'twitterHandles':TwitterHandles,
        'product':productSlug,
        'product_name':product_name,
        'userImages':userImages,
        'twitterZip':twitterZip,
        'githubInfo':githubInfo,
        'git':git,
        'saasWorthy':saasWorthy,
        'saasHub':saasHub,
        'ycombinator':ycombinator,
        'crunchBaseInfo':crunchBaseInfo,
        'saasWorthyInfo':saasWorthyInfo,
        'linkedInInfo':linkedInInfo,
        'yCombinatorInfo':yCombinatorInfo,
        'apolloIOInfo':apolloIOInfo,
        'saasHubInfo':saasHubInfo,
        'noOfGraphs':range(noOfGraphs),
        'graphNames':graphNames,
    }
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