from django.shortcuts import render,redirect
import requests
import json

# Create your views here.
#To view logs: docker logs vccf_web_1
from django.urls import reverse


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
    #Gets information in form of JSONN
    posts = requests.post(API_URL,
                          headers=headers,
                          data=json.dumps(query))

    #Saves Json information to variable
    jsonInfo = posts.json()
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

    product_name = slug.capitalize()
    context = {
        'results':results,
        'topics':topics,
        'logo':logo,
        'names':Names,
        'socialMediaZip':socialMediaZip,
        'twitterHandles':TwitterHandles,
        'product':productSlug,
        'product_name':product_name
    }
    return render(request, 'main/productHome.html', context)
