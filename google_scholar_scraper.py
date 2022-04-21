#Made by hongcana
#ver 1.0
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup

# Methods
def get_citations(content):
    words = str(content[0])
    out = 0
    for char in range(0, len(words)):
        if words[char] == '회':
            init = char
            for end in range(init,init-10, -1):
                if words[end] == '>':
                    break
            out = words[end+1:init]
            break
    return(int(out))


def get_year(content):
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[char-5:char-1]
    if not out.isdigit():
        out = 0
    return int(out)

def get_author(content):
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[:char-1]
            break
    return out


# Update these varibales according to your requirement!
keyword = input("키워드를 입력하세요...") # 키워드 입력
num_of_results = 500
save_database = True
# Choose if you would like to save the DB to .csv

# Start new session
session = requests.Session()

# Variables
links = list()
title = list()
citations = list()
year = list()
rank = list()
author = list()
rank.append(0)

# Get content from 1000 URLs
for n in range(0, num_of_results, 10):
    if n % 100 == 0:
        # Time.sleep 빼셔도 됩니다.
        time.sleep(0.2)
        print("Job processing...{}/{}".format(n, num_of_results))

    url = 'https://scholar.google.com/scholar?start='+str(n)+'&q='+keyword.replace(' ','+')
    page = session.get(url)
    c = page.content

    # Create parser
    soup = BeautifulSoup(c, 'html.parser')
    # Get stuff
    mydivs = soup.findAll("div", {"class": "gs_r gs_or gs_scl"})
    
    for div in mydivs:
        try:
            links.append(div.find('h3').find('a').get('href'))
        except: # catch *all* exceptions
            links.append('Look manually at: https://scholar.google.com/scholar?start='+str(n)+'&q=non+intrusive+load+monitoring')

        try:
            title.append(div.find('h3').find('a').text)
        except:
            title.append('Could not catch title')

        citations.append(get_citations(div.select('div.gs_ri > div.gs_fl > a:nth-child(3)')))
        year.append(get_year(div.find('div', {'class' : 'gs_a'}).text))
        author.append(get_author(div.find('div', {'class' : 'gs_a'}).text))
        rank.append(rank[-1]+1)

# Create a dataset and sort by the num of citations
data = pd.DataFrame(zip(author, title, citations, year, links), index = rank[1:],\
    columns = ['Author', 'Title', 'Citations', 'Year', 'Source'])
data.index.name = 'rank'

data_ranked = data.sort_values('Citations', ascending = False)
print(data_ranked)
print(data_ranked.shape)

if save_database:
    timestr = time.strftime("%y%m%d_%H%M%S")
    data_ranked.to_csv(keyword+'_'+timestr+'.csv', encoding='utf-8-sig')
    print('to csv Done!')