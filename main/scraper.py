from bs4 import BeautifulSoup
import requests

#/akaunting-3-0 --> Good for testing
def searchResults(searchTerm):
    URL = 'https://www.ask.com/web?q='+searchTerm
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = [[],[]]
    for a in soup.find_all("a", {"class": "PartialSearchResults-item-title-link"}):
        if('searchResult' in a['data-analytics']):
            print(a.text)
            print(a['href'])
            print('')


def crunchBaseResults(companyName):
    searchTerm = companyName + ' ' + 'crunchbase'
    searchResults(searchTerm)

def saasWorthyResults(companyName):
    searchTerm = companyName + ' ' + 'Saasworthy'
    searchResults(searchTerm)

def linkedInResults(companyName):
    searchTerm = companyName + ' ' + 'LinkedIn'
    searchResults(searchTerm)

def yCombinatorResults(companyName):
    searchTerm = companyName + ' ' + 'yCombinator'
    searchResults(searchTerm)

def apolloIOResults(companyName):
    searchTerm = companyName + ' ' + 'Apollo.io'
    searchResults(searchTerm)

def SaasHubResults(companyName):
    searchTerm = companyName + ' ' + 'SaasHub'
    searchResults(searchTerm)

def capterraResults(companyName):
    searchTerm = companyName + ' ' + 'Capterra'
    searchResults(searchTerm)

