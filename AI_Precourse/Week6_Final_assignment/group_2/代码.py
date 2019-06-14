
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics
from sklearn.grid_search import GridSearchCV

import matplotlib.pylab as plt
from matplotlib.pylab import rcParams

def modelfit(alg, dtrain, dtest, predictors,useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()#赋值最小损失函数下降值
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain[target].values)
        # 构建train除target, IDcol这两个的列的元素+Disbursed的值
        # xgtest = xgb.DMatrix(dtest[predictors].values)
        # 构建test除target, IDcol这两个的列的元素
        cvresult = xgb.cv(xgb_param, xgtrain, 
                          num_boost_round=alg.get_params()['n_estimators'],
                          nfold=cv_folds,metrics='auc', 
                          early_stopping_rounds=early_stopping_rounds)
        # ,show_progress=False
        # 在每一次迭代中使用交叉验证，并返回理想的决策树数量.是否显示目前几颗树额
        
        alg.set_params(n_estimators=cvresult.shape[0])
    
    #Fit the algorithm on the data 将算法放在数据上
    alg.fit(dtrain[predictors], dtrain['Disbursed'],eval_metric='auc')
        
    #Predict training set:  预测训练集：
    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]
        
    #Print model report: 打印模型报告：
    print ("\nModel Report")
    print ("Accuracy : %.4g" % metrics.accuracy_score(dtrain['Disbursed'].values, dtrain_predictions))
    print ("AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['Disbursed'], dtrain_predprob))
     
    #Predict on testing data:  预测测试数据：
    dtest['forecast'] = alg.predict_proba(dtest[predictors])[:,1]
    forecast = dtest[['ID','forecast']]
    forecast.rename(columns={'ID':'userid','forecast':'probability'}, inplace = True)
    forecast.to_csv("forecast_data.csv",index=False,sep=',')
                   
    feat_imp = pd.Series(alg.feature_importances_).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    

rcParams['figure.figsize'] = 12, 4

train  =  pd.read_csv ('train_data.csv')
test = pd.read_csv ('test_data.csv')

target='Disbursed'
IDcol = 'ID'

predictors = [x for x in train.columns if x not in [target, IDcol]]
xgb1 = XGBClassifier(
        learning_rate =0.1,
        n_estimators=500,   #随机森林数的数量
        max_depth=6,         #树的最大深度
        min_child_weight=1,  #决定最小叶子节点样本权重和
        gamma=4,             #指定了节点分裂所需的最小损失函数下降值
        subsample=0.7,       #控制对于每棵树，随机采样的比例
        colsample_bytree=0.8,#控制每棵随机采样的列数的占比
        objective= 'binary:logistic',#二分类的逻辑回归，返回预测的概率
        nthread=4,          #进行多线程控制，应当输入系统的核数
        scale_pos_weight=1, #在样本十分不平衡时，设定为一个正值，可以使算法更快收敛
        seed=27)#,            #随机数的种子
        #booster='gbtree')            
modelfit(xgb1, train, test, predictors)