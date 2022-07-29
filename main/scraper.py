from bs4 import BeautifulSoup
import requests

#/akaunting-3-0 --> Good for testing
def searchResults(searchTerm):
    URL = 'https://www.ask.com/web?q='+searchTerm
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = [[],[]]
    for a in soup.find_all("a", {"class": "PartialSearchResults-item-title-link"}):
        results[0].append(a.text)
        #print(a.text)
        #print(a['href'])
        results[1].append(a['href'])
        print('')
    return results

#test - akaunting
def githubResults(companyName):
    print("GitHub Results")
    searchTerm = companyName + ' ' + 'github'
    results = searchResults(searchTerm)
    print(results[0][0])
    val = "0"
    if (companyName.lower() in str(results[0][0]).lower() and '- github' in str(results[0][0]).lower() ):
        print("Yes")
        val = [results[0][0], results[1][0]]
    else:
        val = str(companyName) + ": " + str(results[0][0]).lower()
    print(val)
    return val
#test - akaunting
def crunchBaseResults(companyName):
    query = companyName.replace(' ', '-')
    searchTerm = query + ' ' + 'crunchbase'
    companyName = companyName.lower()
    results = searchResults(searchTerm)
    print(results[0][0])
    val = "0"
    if (companyName in str(results[0][0]).lower() and 'Crunchbase Company Profile & Funding' in str(results[0][0])):
        val = [results[0][0], results[1][0]]
    else:
        val = str(companyName) + ": " + str(results[0][0]).lower()
    print(val)
    return val

def saasWorthyResults(companyName):
    searchTerm = companyName + ' ' + 'Saasworthy'
    searchResults(searchTerm)
    companyName = companyName.lower()
    results = searchResults(searchTerm)
    print(results[0][0])
    val = "0"
    if (companyName in str(results[0][0]).lower() and 'Pricing, Reviews and Features' in str(results[0][0]) and ' SaaSworthy' in str(results[0][0]) ):
        print("Yes")
        val = [results[0][0], results[1][0]]
        print(val)
    elif(companyName not in str(results[0][0]).lower() and 'Pricing, Reviews and Features' not in str(results[0][0]) and ' SaaSworthy' not in str(results[0][0]) ):
        val = str(companyName) + ": " + str(results[0][0]).lower()
    else:
        val = str(companyName) + ": " + str(results[0][0]).lower()


    return val

def linkedInResults(companyName):
    searchTerm = companyName + ' ' + 'LinkedIn'
    searchResults(searchTerm)
    companyName = companyName.lower()
    results = searchResults(searchTerm)
    print(results[0][0])
    val = "0"
    if (companyName in str(results[0][0]).lower() and '- linkedin' in str(results[0][0]).lower()):
        print("Yes")
        val = [results[0][0], results[1][0]]
        print(val)
    elif(companyName not in str(results[0][0]).lower() and '- linkedin' not in str(results[0][0]).lower()):
        print("No")
        val = str(companyName) + ": " + str(results[0][0]).lower()
    else:
        print("No")
        val = str(companyName) + ": " + str(results[0][0]).lower()

    return val

def yCombinatorResults(companyName):
    URL = 'https://www.ycombinator.com/companies/'+companyName.lower()
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('title')
    print(title)
    if('File Not Found' in str(title)):
        print("No Company found")
    else:
        print("company found")
    return ['yCombinator - ' + companyName,URL]

def apolloIOResults(companyName):
    searchTerm = companyName + ' ' + 'Apollo.io'

    results = searchResults(searchTerm)
    print(results[0][0])
    val = "0"
    if (companyName in str(results[0][0]) and '- Apollo.io' in str(results[0][0]) ):
        print("Yes")
        val = [results[0][0], results[1][0]]
        print(val)
    elif(companyName not in str(results[0][0]) and '- Apollo.io' not in str(results[0][0])):
        val = str(companyName) + ": " + str(results[0][0]).lower()
    else:
        val = str(companyName) + ": " + str(results[0][0]).lower()

    return val

def saasHubResults(companyName):
    searchTerm = companyName + ' ' + 'SaasHub'
    results = searchResults(searchTerm)
    print(results[0][0])
    val = "0"
    if (companyName.lower() in str(results[0][0]).lower() and '- SaaSHub' in str(results[0][0]) ):
        print("Yes")
        val = [results[0][0], results[1][0]]
        print(val)
    elif (companyName.lower() in str(results[0][0]).lower() and 'compare differences & reviews' in str(results[0][0]) ):
        print("Yes")
        val = [results[0][0], results[1][0]]
        print(val)
    elif (companyName.lower() in str(results[0][0]).lower() and 'community voted on SaaSHub' in str(results[0][0]) ):
        print("Yes")
        val = [results[0][0], results[1][0]]
        print(val)
    elif(companyName not in str(results[0][0]) and 'Reviews - SaaSHub' not in str(results[0][0])):
        val = str(companyName) + ": " + str(results[0][0]).lower()
    else:
        val = str(companyName) + ": " + str(results[0][0]).lower()

    return val

def capterraResults(companyName):
    searchTerm = companyName + ' ' + 'Capterra'
    results = searchResults(searchTerm)
    print(results[0][0])
    val = "0"
    if (companyName in str(results[0][0]) and 'pricing, cost & reviews - capterra' in str(results[0][0]).lower() ):
        print("Yes")
        val = str(companyName) + ": " + str(results[0][0]).lower() + str(" YES!")
        print(val)
    elif(companyName in str(results[0][0]) and 'pricing, alternatives & more 2022 - capterra' in str(results[0][0]).lower()):
        print("Yes")
        val = str(companyName) + ": " + str(results[0][0]).lower() + str(" YES!")
        print(val)
    else:
        val = str(companyName) + ": " + str(results[0][0]).lower()

    return val

