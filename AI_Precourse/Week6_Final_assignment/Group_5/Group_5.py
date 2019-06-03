
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from bs4 import BeautifulSoup
import requests
import json
import logging
import redis
from pprint import pprint
from redis import *
import ast
import numpy as np
import pandas as pd
import os
from keras.models import Sequential
from keras.layers.core import Dense

import tensorflow as tf
#import redis


di = {}

CLI = redis.StrictRedis(host='127.0.0.1', port=6379)

for year in range(15,19):       #year
    for t in range(0,1500):     #场次。第x场
        key = year * 100000 + t
        url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/20' + str(
            year) + '/scores/gamedetail/002' + str(key) + '_gamedetail.json'
        wb_data = requests.get(url)
        allgam_ok = (str(wb_data) == '<Response [404]')
        if allgam_ok :
            break

        wb_data_py = json.loads(wb_data.text)
        stt = wb_data_py["g"]["stt"]
        if stt.endswith("Qtr"):
            logging.warning("%s game is not finished" % key)

        vls = wb_data_py["g"]["vls"]
        hls = wb_data_py["g"]["hls"]
        vs = int(vls["s"])
        hs = int(hls["s"])

        w = 1.0 if hs > vs else 0.0
        di.update({"win": w})

        vsts = vls["tstsg"]
        hsts = hls["tstsg"]

        for k in hsts:
            di.update({k: int(hsts[k]) - int(vsts[k])})

        vn = vls["ta"]
        hn = hls["ta"]
        di.update({"home": hn, "away": vn})

        date = wb_data_py["g"]["gdtutc"]
        di.update({"date": date})

        CLI.hset("gamedetaildiff", key, str(di))
        logging.info("%s save success" % key)
        CLI.hset("gamedetail", key, wb_data.text)

        print(key)


#cli = redis.Redis(host='127.0.0.1', port=6379)
#pprint(data[list(data.keys())[1]])

data = CLI.hgetall("gamedetaildiff")    #读取数据
dict = {}
for key in list(data.keys()):           #x {场次：各个字段数据}
    x = {key.decode() :
             pd.Series(list((eval(data[key].decode())).values()) ,
                       index = list((eval(data[key].decode())).keys()))}
    dict.update(x)      #dict是{str:list}的字典
df = pd.DataFrame(dict)
#print(len(list((eval(data[key].decode())).keys())))

#pd.Series(list((eval(data[key].decode())).values()) , index = list((eval(data[key].decode())).keys()))
#list((eval(data[key].decode())).values())

#print(dict['1500787'])

#df = pd.DataFrame([data[key] for key in list(data.keys())])

df = df.fillna(value=0.0)   # 用 0 填补空白数据
#print(df)
df = df.T       #转置
df['date'] =pd.to_datetime(df.date) #转换格式
df = df.sort_values(['date'])       #排序

dataY = df['win']                   #抽取字段
dataX = df.drop(['win', 'date', 'home', 'away'], axis=1)
#train_x = np.array(dataX)[2460::2] # train set
#train_y = np.array(dataY)[2460::2]
#test_x = np.array(dataX)[2461::2] # test set
#test_y = np.array(dataY)[2461::2]


train_x = np.array(dataX)[2460:3680:1] # train set
train_y = np.array(dataY)[2460:3680:1]
test_x = np.array(dataX)[3680:-50:1] # test set
test_y = np.array(dataY)[3680:-50:1]

#from keras.models import Sequential
#from keras.layers.core import Dense

model = Sequential()
model.add(Dense(60, input_dim=train_x.shape[1], activation='relu'))#添加网络层
model.add(Dense(30, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(train_x,train_y,batch_size=3,epochs=15)
model.evaluate(test_x,test_y)

game_detail_data = CLI.hgetall("gamedetail")
game_detail_json = []
for k in game_detail_data:
    di_v = {}
    di_h = {}
    j = json.loads(game_detail_data[k])

    vls = j["g"]["vls"]
    hls = j["g"]["hls"]
    di_v.update(vls["tstsg"])
    di_v.update({"date": j["g"]["gdtutc"], "name": vls["ta"], "home": 0})
    game_detail_json.append(di_v)
    di_h.update(hls["tstsg"])
    di_h.update({"date": j["g"]["gdtutc"], "name": hls["ta"], "home": 1})
    game_detail_json.append(di_h)
game_detail_df = pd.DataFrame(game_detail_json)
game_detail_df = game_detail_df.fillna(value=0.0)

def predict(home=None, away=None):
    home_data = game_detail_df[(game_detail_df['name']==home) &
                               (game_detail_df['home']==1)].sort_values(by='date', ascending=False)[:5].mean()
    away_data = game_detail_df[(game_detail_df['name']==away) &
                               (game_detail_df['home']==0)].sort_values(by='date', ascending=False)[:5].mean()
    home_data = home_data.drop(['home'])
    away_data = away_data.drop(['home'])
    new_x = np.array(home_data - away_data)
    return model.predict_classes(new_x[np.newaxis,:], verbose=0)[0][0]


sum = 0
yes_sum = 0
for row in range(4139,4189,1):
    sum += 1
    if predict(home=df.ix[row]['home'], away=df.ix[row]['away']) == df.ix[row]['win']:
        yes_sum += 1
print("预测准确率为：")
print(+yes_sum/sum)




'''


teams = [['DET', 'WAS'], #活塞 奇才 1
         ['ORL', 'PHX'],#魔术 太阳 0
         ['ATL', 'IND'],#老鹰 步行者 0
         ['BKN', 'CHA'],#篮网 黄蜂 1
         ['MIA','TOR'],#热火 猛龙 0
         ['CHI', 'MIN'],#公牛 森林狼 0
         ['MEM','CLE'],#灰熊 骑士 1
         ['DAL', 'NOP'],#独行侠 鹈鹕 1
         ['DEN', 'SAS'],#马刺 掘金 1
         ['LAC','SAC'],#快船 国王 1
         ['LAC', 'DEN'],
         ['WAS', 'PHX'],
         ['PHI', 'TOR'],
         ['MIA', 'MIL'],
         ['HOU', 'SAS'],
]

for t in teams:
    p = predict(t[0],t[1])

    if p == 1:
        print("%s( win) vs %s(loss)" % (t[0],t[1]))
    else:
        print("%s(loss) vs %s( win)" % (t[0],t[1]))


'''
