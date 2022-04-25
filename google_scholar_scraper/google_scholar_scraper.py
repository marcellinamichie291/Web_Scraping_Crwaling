# Made by hongcana
# ver 1.1 Updates

# fix bugs in get_year, get_author method
# add time.sleep(1) to avoid response[429]
# 한글 논문 검색 지원 추가( Support for searching korean papers )
# 논문 검색 수 입력 가능

import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import urllib

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
    out = ''
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[char-5:char-1]
    if not out.isdigit():
        out = 0
    return int(out)

def get_author(content):
    out = 0
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[:char-1]
            break
    return out


# Update these varibales according to your requirement!
condition = input("한글 논문 검색 = KO / 외국 논문 검색 = EN 입력...")
keyword = input("키워드를 입력하세요...") # 키워드 입력
num_of_results = int(input("추출할 논문 개수 입력..."))
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
    time.sleep(1.01)

    if condition.upper() == 'EN':
        url = 'https://scholar.google.com/scholar?start='+str(n)+'&q='+keyword.replace(' ','+')

    elif condition.upper() == 'KO':
        # parse모듈을 사용해 한글("한글")변수를 유니코드로 치환
        encode = urllib.parse.quote_plus(keyword)
        url = 'https://scholar.google.com/scholar?start='+str(n)+'&q='+encode.replace(' ','+')+'&hl=ko&lr=lang_ko'
    
    else:
        print("오류 : 한글, 영문 논문 여부를 정확히 입력해주세요. (KO 또는 EN 입력!)")
        condition = -1
        break

    page = session.get(url)
    c = page.content
    print(page) # check response

    # Create parser
    soup = BeautifulSoup(c, 'html.parser')
    # Get stuff
    mydivs = soup.findAll("div", {"class": "gs_r gs_or gs_scl"})

    print("Job processing...{}/{}".format(n, num_of_results))
    for div in mydivs:
        try:
            links.append(div.find('h3').find('a').get('href'))
        except: # catch *all* exceptions
            links.append('링크를 찾을 수 없는 항목')

        try:
            title.append(div.find('h3').find('a').text)
        except:
            title.append('제목을 찾을 수 없는 항목')

        citations.append(get_citations(div.select('div.gs_ri > div.gs_fl > a:nth-child(3)')))
        year.append(get_year(div.find('div', {'class' : 'gs_a'}).text))
        author.append(get_author(div.find('div', {'class' : 'gs_a'}).text))
        rank.append(rank[-1]+1)

# Create a dataset and sort by the num of citations

if condition != -1:
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