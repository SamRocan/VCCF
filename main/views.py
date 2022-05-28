import os
import time

from django.shortcuts import render,redirect
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .LIWC import getExcel, getTweets, tokenize, dic_to_dict, makeTrie, bestMatch, getScore
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
                print(y['twitterUsername'])
                print(str(y['twitterUsername']) + ": " + str(y['name']))
        if(i=='media'):
            print("Media")
            for y in jsonInfo['data']['post']['media']:
                print(y['url'])
        if(i=='productLinks'):
            print("Product Links")
            for y in jsonInfo['data']['post']['productLinks']:
                print(y['url'])
        if(i=='thumbnail'):
            print("Thumbnail")
            logo = str(jsonInfo['data']['post'][i]['url'])
        if(i=='topics'):
            print("Topics")
            for y in jsonInfo['data']['post']['topics']['edges']:
                topics.append(y['node']['name'])
        results[i] = str(jsonInfo['data']['post'][i])
    print(results.get('tagline'))

    """Parsing Other Websites"""
    companyName = str(results.get('name'))

    socialMediaZip = zip(Names,TwitterHandles, phUrls, profilePics)
    request.session["TwitterHandles"] = TwitterHandles
    product_name = slug.capitalize()

    #Get Twitter Image
    userImages = []
    for handle in TwitterHandles:
        auth = tw.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        api = tw.API(auth, wait_on_rate_limit=True)

        user = api.get_user(screen_name=handle)
        url = str(user.profile_image_url)
        userImage = url.replace("_normal", "")
        userImages.append(userImage)
        print(userImage)
    twitterZip = zip(TwitterHandles, userImages)
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
        'twitterZip':twitterZip
    }
    return render(request, 'main/product.html', context)

class ChartData(APIView):

    def get(self, request, format = None):
        data = ["sent data"]
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
            print(userName)
            print("Getting Tweets for " + str(userName))
            try:
                twitterContent = getTweets(userName)
            except:
                message = "No Twitter account found for that username, please try another account or check your spelling."
                return render(request, 'Main/noTwitter.html', {'message':message})
            print("Getting Tweets took ", time.time() - start_time, " to run")


            print("Tokenizing Tweets")
            tokenizedTweets = tokenize(twitterContent)
            print(tokenizedTweets)
            print("Tokenizing Tweets took ", time.time() - start_time, " to run")

            print("turning to dictionary")
            dictionary = dic_to_dict(liwc_dic)

            print("turning into trie")
            trie = makeTrie(dictionary)

            print("Trie took ", time.time() - start_time, " to run")


            print("Categorizing tokens")
            values = []
            for i in tokenizedTweets[0]:
                value = trie.lookup(i)
                for i in value:
                    if(isinstance(i, int)):
                        values.append(i)
            print("Categorizing tokens took ", time.time() - start_time, " to run")

            print("Getting Best Match")
            try:
                match = bestMatch(data, values)
            except:
                message = "Analysis cannot be preformed on this account. This is usually due to the account " \
                          "primarily being in a language other than English, or the Twitter API rate limit being reached." \
                          "Please try another account, or wait and try again later. "
                return render(request, 'Main/noTwitter.html', {'message':message})
            print("Best Match took ", time.time() - start_time, " to run")

            profile = list(match.keys())[0]
            print("Getting Scores")
            scores = getScore(score_data, profile)
            print("Scores took ", time.time() - start_time, " to run")

            scoresVar = scores[0]
            catVar = scores[1]
            fiveFactors = ["Extraversion", "Neuroticism", "Agreableness", "Concientiousness", "Openness"]

            print("My program took ", time.time() - start_time, " to run")
            extScore.append(scoresVar[0])
            neuScore.append(scoresVar[1])
            agrScore.append(scoresVar[2])
            conScore.append(scoresVar[3])
            opnScore.append(scoresVar[4])
        ext = "Extroversion (" + str(catVar[0]) + ")"
        neu = "Neuroticism (" + str(catVar[1]) + ")"
        agr = "Agreeableness (" + str(catVar[2]) + ")"
        con = "Conscientiousness (" + str(catVar[3]) + ")"
        opn = "Openness (" + str(catVar[4]) + ")"

        print("My program took ", time.time() - start_time, " to run")


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
        }

        return Response(data)