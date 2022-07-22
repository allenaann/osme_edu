# Copyright (C) 2022 OSME Education - All Rights Reserved
# Author: Xiaofeng Fu
# Description: Collect entry requirement for UCL master degree

import re
import requests
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

def writeData(group):
    with open('ucl.csv','a+',encoding='utf-8') as f:
        f.write(group[0]+','+group[1]+','+group[2]+','+group[3]+','+group[4]+'\n')
    print("---------------------------------------")

print("***** OSME Edu Programme Collector *****")
root_url = "https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees?query=&year"
headers = {"Content-Type": "application/json",
                    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                    "Connection": "close"}
urls = []
programmes = []
requirements = []
application_dates = []
study_modes = []
start_dates = []
s = requests.Session()
s.mount('http://',HTTPAdapter(max_retries=5))
s.mount('https://',HTTPAdapter(max_retries=5))
try:
    resp = s.get(root_url, headers=headers)
except requests.exceptions.RequestException as e:
    print("Request Failed!")
    exit()   
resp.encoding = 'utf-8'
content = resp.text

bs = BeautifulSoup(content, 'html.parser')
for programme in bs.select('#programme-data-content a'):
    urls.append(programme['href'])
    group = ['-','-','-','-','-']
    group[0] = programme.text
    programmes.append(group)

for i in range(len(urls)):
    try:
        resp = s.get(urls[i], headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Request Failed!")
        exit()
    resp.encoding = 'utf-8'
    content = resp.text
    group = programmes[i]

    print("No: "+str(i)+" programme: "+ group[0] + "\nProgress: {:.2f}%".format(100*i/len(urls)))

    bs = BeautifulSoup(content, 'html.parser')
    requirement = bs.select('#entry-requirements p')
    if (not isinstance(requirement, list) or requirement == []):
        writeData(group)
        continue
    
    group[1] = requirement[0].text

    tags = bs.find_all('div', class_='prog-key-info__text')
    for tag in tags:
        for child in tag.children:
            if child.text == 'Applications accepted':
                string = tag.contents[3].text.replace('\n', '').replace('\r', '')
                formated_string = '"'+' '.join(string.split())+'"'
                group[2] = formated_string
            if child.text == 'Study mode':
                group[3] = tag.contents[3].text
            if child.text == 'Programme starts':
                group[4] = tag.contents[3].text
    writeData(group)
print("Finish!")
