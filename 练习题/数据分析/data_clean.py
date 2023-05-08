# -*- coding:utf-8 -*-
"""
作者：HET
    数据清洗
日期：2023年05月06日
"""
import pandas as pd

# ==========数据导入===========
data=pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')  # 电信用户流失
# print(data.columns)
data.columns=['用户ID', '性别', '是否老人', '是否有伴侣', '是否有孩子',
       '合同期限', '通话服务', '多线程', '网络服务',
       '在线安全', '在线备份', '设备安全', '技术支持',
       '流媒体电视', '流媒体电影', '期限单位', '电子账单',
       '支付方式', '月消费', '总消费', '是否流失']

# # =======汇总统计========
# print(data.dtypes)  # 数据类型
# print(data.describe())  # 只对数值型数据进行汇总统计
# print(data.describe(include='all'))   # 对所有数据进行汇总统计

# # ===========缺失值查询与处理==========
# print(data.isnull())  # 是缺失值：1/True，不是：0/False
# print(data.isnull().sum())  # 统计各类型数据 缺失值个数

# # ===========重复值查询与处理==========
# print(data.duplicated())  # 按行判断
# print(data.duplicated().sum())
# print(data['是否老人'].duplicated())  # 按指定列判断


'''   用户属性   '''
# # *******整体流失情况：人数、比例、流失率***************
churn=data[data['是否流失']=='Yes']  # 流失子数据
# # print(churn)

# print(data['是否流失'].drop_duplicates())  # drop_duplicates()去重复值
churn0=data[data=='No']['是否流失'].count()  # 非流失人数
churn1=data[data=='Yes']['是否流失'].count()   # 流失人数
# print(churn0,churn1)
churn_per=churn1/len(data)   # 流失率
# print(churn_per)
# # =======性别：人数、比例、流失率========
# print(data['性别'].drop_duplicates())
gender0=data[data=='Female']['性别'].count()  # 女性
gender1=data[data=='Male']['性别'].count()  # 男性
# print(gender0,gender1)
gender0_per=gender0/len(data)  # 女性占比
# print(gender0_per)
g0_churn=len(churn[churn['性别']=='Female'])/gender0  # 女性流失率
# g0_churn=churn[churn['性别']=='Female']['性别'].count()/gender0  # 女性流失率
# # print(g0_churn)
g1_churn=len(churn[churn['性别']=='Male'])/gender1  # 男性流失率
# print(g1_churn)
# # =======老人：人数、比例、流失率========
# print(data['是否老人'].drop_duplicates())
senior0=len(data[data['是否老人']==0])   # 不是老人
senior1=len(data[data['是否老人']==1])   # 是老人
# print(senior0,senior1)
# print(senior1/len(data))   #老年人占比
s0_churn=churn[churn['是否老人']==0]['是否老人'].count()/senior0   # 非老人流失率
s1_churn=len(churn[churn['是否老人']==1]['是否老人'])/senior1   # 老人流失率
# print(s0_churn,s1_churn)
# # =======伴侣：人数、比例、流失率========
# # =======亲属：人数、比例、流失率========
# # =======数据洞察：现象、溯源、建议========
'''
1.性别无特殊性
2.是否老人：老人相对非老人，更容易流失
3.是否伴侣：……
……
'''

'''    产品属性    '''
# 创建通用函数：计算类别数据对应条数、占总数比例、对应流失率
def eda_calculate(column,types):
       """
       计算类别数据对应条数、占总数比例、对应流失率
       :param column: str，列表
       :param types: list，类别数据
       :return:
       """
       print('\n========当前标签：',column,types)
       # 计算类别数据对应的个数
       res_list=[]
       rate_list=[]
       for t in types:
           res=len(data[data[column]==t])
           # 计算类别数据对应的流失率
           rate = len(churn[churn[column] == t]) / res
           res_list.append({t:res})
           rate_list.append({t:rate})
       # 预览各类别数据对应的个数、占总数比列
       print('========数据条数')
       for res in res_list:
           print(res,'占总数比例',list(res.values())[0]/len(data))
       # 预览各类别数据对应流失率、前后者倍数关系
       print('*******类别数据对应流失率********')
       for rate in rate_list:
           before=list(rate.values())[0]
           index=rate_list.index(rate)+1
           print(rate)
           if index<len(rate_list):
              after=list(rate_list[index].values())[0]
              print('前后者倍数关系',before/after)

# 创建通用函数：提取列标签、提取对应类别数据
columns=['通话服务', '多线程', '网络服务', '在线安全', '在线备份',
        '设备安全', '技术支持','流媒体电视', '流媒体电影']
for c in columns:
    types=data[c].drop_duplicates().tolist()   # tolist()转换为列表
    # print(c,types)
    # 函数应用：快速计算特征指标
    eda_calculate(c,types)
# 数据洞察（高流失率的产品属性特征）
'''
1.没有明显相关性的产品服务
    通话服务、多线程：流失率在25%左右
    流媒体电视、电影：流失率在30%左右
2.有明显影响的产品服务：和网络相关的增值服务
    网络安全：光纤用户的流失率41%，是DSL的2倍多
    在线安全：没有选择这项服务的流失率41%+，是选择的用户的2.85倍
    在线备份：没有选择这项服务的流失率41%+，是选择的用户的1.5倍
    设备安全：同上
    技术支持：没有选择这项服务的流失率41%+，是选择的用户的2.74倍
'''
# eda_calculate(column='是否老人',types=[0,1])

