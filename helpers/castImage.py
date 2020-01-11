import requests
import json
from bs4 import BeautifulSoup


def getImages(names):

    casts=[]
    for name in names:
        # search at google search
        # print(" ".join(name.split(" ")[-2:]))
        nam = " ".join(name.split(" ")[-2:])
        URL = f'https://www.google.com/search?q={nam} imdb &source=lnms&tbm=isch'
        # get http request of page
        page = requests.get(URL)
        # beautifull soup it
        soup = BeautifulSoup(page.content, 'lxml')
        # for soso in soup.find_all('img'):
        #     print(soso.get('src'))
        casts.append({"name":nam,"src":soup.find_all('img')[4].get('src')})
        # extract the spesific image of imdb
        print(soup.find_all('img')[4].get('src'))

    return  casts