#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: scrapy.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: 2018年08月09日 星期四 13时58分10秒

#########################################################################
import sys

import requests
import ast
from bs4 import BeautifulSoup
import json as js
import re


def getNumFromStr(data):

    return re.findall(r"\d+\.?\d*",data)[0]

def xPathHtml(data):

    soup = BeautifulSoup(data,"html5lib")


    #get goods title
    goods_title =  soup.find('span',class_ = 'g-n-goods-title')
    print(goods_title.string)

    #get sold num
    goods_sold_num = soup.find('span',class_='g-sales false')
    goods_sold_num = re.sub("\D","",goods_sold_num.string)
    print(goods_sold_num)

    #get goods price
    tmp = soup.find_all('script')
    goods_info = tmp[0]
    for child in tmp:
        
        if 'window.rawData' in str(child):
            goods_info = child.string
            goods_info = goods_info.split("=")[1]
            goods_info = goods_info.strip().strip(";")

    goods_info = js.loads(goods_info,encoding = "utf-8")
    
    f= open("log1","w")
    for item in goods_info:
        
        f.write(str(item)+","+str(goods_info[item])+"\n")
        #print (item,goods_info[item])
    f.close()

    #get mall name &id
    mall_id = goods_info['mall']['mallID']
    mall_name = goods_info['mall']['mallName']
    mall_sold_quant = getNumFromStr(goods_info['mall']['salesTip']) 
    print(mall_sold_quant)
    mall_goods_num = goods_info['mall']['goodsNum']

    #get goods price & num
    print(goods_info['goods']['groupPrice'])

if __name__ == "__main__":

    ua = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',     
        'Upgrade-Insecure-Requests':'1',
        'Connection':'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cookie': 'api_uid=rBUGYFtNe32oZ2UvCOqWAg==; rec_list_mall_bottom=rec_list_mall_bottom_NMOmL3; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F68.0.3440.106%20Safari%2F537.36; webp=1; spike=spike_36Phxj; mall_main=mall_main_CDfZNP; msec=1800000; rec_list_catgoods=rec_list_catgoods_mHh5Zm; rec_list_index=rec_list_index_PF09q6; rec_list=rec_list_mReqZ7',
        'Host': 'mobile.yangkeduo.com'
       }
    
    url = 'http://mobile.yangkeduo.com/goods.html?goods_id=141911322'

    data = requests.get(url,headers = ua)

    f = open('data.html',"w")
    f.write(data.text)
    f.close()

    xPathHtml(data.text)
