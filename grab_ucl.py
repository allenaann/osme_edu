# Copyright (C) 2022 OSME Education - All Rights Reserved
# Author: Xiaofeng Fu
# Description: Collect entry requirement for UCL master degree

import re
import requests
import os
from bs4 import BeautifulSoup

root_url = "https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees?query=&year"
urls = []
programmes = []
requirements = []
application_dates = []
study_modes = []
start_dates = []

resp = requests.get(root_url)
resp.encoding = 'utf-8'
content = resp.text
bs = BeautifulSoup(content, 'html.parser')
for programme in bs.select('#programme-data-content a'):
    urls.append(programme['href'])
    programmes.append(programme.text)

for i in range(len(urls)):
    resp = requests.get(urls[i])
    resp.encoding = 'utf-8'
    content = resp.text
    bs = BeautifulSoup(content, 'html.parser')
    requirement = bs.select('#entry-requirements p')[0].text
    # print(requirement)
    requirements.append(requirement)

    tags = bs.find_all('div', class_='prog-key-info__text')
    for tag in tags:
        for child in tag.children:
            if child.text == 'Applications accepted':
                string = tag.contents[3].text.replace('\n', '').replace('\r', '')
                formated_string = ' '.join(string.split())
                application_dates.append(formated_string)
            if child.text == 'Study mode':
                study_modes.append(tag.contents[3].text)
            if child.text == 'Programme starts':
                start_dates.append(tag.contents[3].text)

with open('ucl.txt','w') as f:
    for i in range(len(urls)):
        f.write(programmes[i]+','+requirements[i]+','+application_dates[i]+','+study_modes[i]+','+start_dates[i]+'\n')
