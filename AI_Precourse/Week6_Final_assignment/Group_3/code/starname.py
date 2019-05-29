# -*- coding: utf-8 -*-
import os
import time
import json
import requests
def getManyPages(pages,sex,location,path):
    params=[]
    for i in range(0, 12*pages+12, 12):
        params.append({
            'resource_id': 28266,
            'from_mid': 1,
            'format': 'json',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'query': '明星',
            'sort_key': '',
            'sort_type': 1,
            'stat0': sex,
            'stat1': location,
            'stat2': '',
            'stat3': '',
            'pn': i,
            'rn': 12
                  })
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'

    x = 0
    f = open(path, 'w')
    print('\n'+sex+'明星:')
    print()
    for param in params:
        try:
            res = requests.get(url, params=param)
            js = json.loads(res.text)
            results = js.get('data')[0].get('result')
        except AttributeError as e:
            print(e)
            continue
        for result in results:
            img_name = result['ename']
            f.write(img_name+'\n')
 
        if x % 10 == 0:
            print('第%d页......'%x)
        x += 1
    f.close()
 
if __name__ == '__main__':
    pages = 20
    sex = ['男','女']
    path = ['maleStarName.txt','femaleStarName.txt']
    location = '香港'
    for i in range(len(sex)):
        getManyPages(pages,sex[i],location,path[i])