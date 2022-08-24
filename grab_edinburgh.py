# Copyright (C) 2022 OSME Education - All Rights Reserved
# Author: Xiaofeng Fu
# Description: Collect entry requirement for Edinburgh master degree

import re
import requests
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin

def writeData(group):
    with open('edinburgh.csv','a+',encoding='utf-8') as f:
        f.write(group[0]+','+group[1]+','+group[2]+','+group[3]+','+group[4]+'\n')
    print("---------------------------------------")

print("***** OSME Edu Programme Collector *****")
root_url = "https://www.ed.ac.uk/studying/postgraduate/degrees/index.php&edition=2022?r=site%2Fsearch&pgSearch=&yt0=&moa=a"
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
    resp = s.request("GET",url=root_url, headers=headers)
except requests.exceptions.RequestException as e:
    print(e)
resp.encoding = 'utf-8'
content = resp.text

bs = BeautifulSoup(content, 'html.parser')
for programme in bs.select('div[class*="list-group"] a'):
    urls.append(urljoin(root_url, programme['href']))
    group = ['-','-','-','-','-']
    group[0] = programme.text
    programmes.append(group)

for i in range(len(urls)):
    try:
        resp = s.request("GET",url=urls[i], headers=headers, timeout=(30,60))
    except requests.exceptions.RequestException as e:
        print(e)
    resp.encoding = 'utf-8'
    content = resp.text
    group = programmes[i]

    print("No: "+str(i)+" programme: "+ group[0] + "\nProgress: {:.2f}%".format(100*i/len(urls)))

    bs = BeautifulSoup(content, 'html.parser')
    # requirement_section = bs.select('div[id*="course-profile-content"] div dd[class*="how-to-apply"]')

    requirement = bs.select('#proxy_collapseentry_req div p')
    if (not isinstance(requirement, list) or requirement == []):
        writeData(group)
        continue
    requirement_section = '"'
    for re in requirement:
        requirement_section += re.text + '\n'
    requirement_section += '"'
    group[1] = requirement_section

    applying_info = bs.select('#proxy_applicationLinks div h5')
    if applying_info != []:
        apply_section = '"'
        for ap in applying_info:
            apply_section += ap.text + '\n'
        apply_section += '"'  
    else:
        apply_section = '"'
        applying_info = bs.select('#proxy_applicationLinks div p')
        if (not isinstance(applying_info, list) or applying_info == []):
            writeData(group)
            continue
        for ap in applying_info:
            apply_section += ap.text + '\n'
        apply_section += '"'
    group[2] = apply_section
    writeData(group)
print("Finish!")
