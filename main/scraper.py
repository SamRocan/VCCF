from bs4 import BeautifulSoup
import requests

#/akaunting-3-0 --> Good for testing
def searchResults(searchTerm):
    URL = 'https://www.ask.com/web?q='+searchTerm
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all("a", {"class": "PartialSearchResults-item-title-link"}):
        if('searchResult' in a['data-analytics']):
            print(a.text)
            print(a['href'])
            print('')