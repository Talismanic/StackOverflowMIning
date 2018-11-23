
# coding: utf-8

# In[1]:


import json
import datetime
import csv
import time
from urllib.request import urlopen
import urllib
import json
import numpy as np
import os
import time
import math
import requests
#import pymysql
import mysql.connector

# import pandas as pd 
# import nltk
# # nltk.download()
# from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.ensemble import RandomForestClassifier

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="stack_overflow"
)


# In[3]:


def request_to_stack(method, url, headers, querystring):
    response = requests.request(method, url, headers=headers, params=querystring)
    return (response.text)


# In[4]:


def fetch_tags():
    base_url = "https://api.stackexchange.com/2.2/tags"
    querystring = {"order":"desc","sort":"popular","site":"stackoverflow"}
    headers = {'Cache-Control': 'no-cache'}
    method = "GET"
    result = request_to_stack(method, base_url,headers,querystring)
    return result



# In[5]:


def fetch_top_answerers(tag):
    base_url = "https://api.stackexchange.com/2.2/tags/"+ tag +"/top-answerers/month"
    querystring = {"site":"stackoverflow"}
    headers = {'Cache-Control': 'no-cache'}
    method = "GET"
    result = request_to_stack(method, base_url,headers,querystring)
    return result


# In[6]:


def fetch_top_askers(tag):
    base_url = "https://api.stackexchange.com/2.2/tags/"+ tag +"/top-askers/month"
    querystring = {"site":"stackoverflow"}
    headers = {'Cache-Control': 'no-cache'}
    method = "GET"
    result = request_to_stack(method, base_url,headers,querystring)
    return result


# In[7]:


def fetch_top_questions(tag, from_time, to_time, sort):
    base_url = "https://api.stackexchange.com/2.2/questions"
    querystring = {"fromdate":from_time, "todate":to_time, "order":"desc","sort":sort,"tagged":tag,"site":"stackoverflow","pagesize":20}
    headers = {"Cahce-Control": "no-cache"}
    method = "GET"
    result = request_to_stack(method, base_url, headers, querystring)
    return result


# In[33]:


to_time = math.floor(time.time())
from_time = to_time - 86400000
# print(to_time)
# print(from_time)
sort = 'votes'
tag ='php'

ques = fetch_top_questions(tag, from_time, to_time, sort)
data = json.loads(ques)
#db = pymysql.connect("localhost","root","","stack_overflow", charset='utf8' )
cursor = db.cursor()


for item in data['items']:
#     print(item['owner']['user_id'])
    user_id = item['owner']['user_id']
    question_id = item['question_id']
    question_title = item['title']
    is_answered = item['is_answered']
    answer_count = item['answer_count']
    created_at = item['creation_date']
    updated_at = item['last_activity_date']
    accepted_answer_id = 0
    #if is_answered == True:
	    #accepted_answer_id = item ['accepted_answer_id']
    #else:
	#accepted_answer_id = 0
    
    data = [user_id, question_id, question_title, is_answered, answer_count, accepted_answer_id, created_at,updated_at]
    sql = 'insert into questions (user_id, question_id, question_title, is_answered, answer_count, accepted_answer_id, created_at,updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update '
    try:
        cursor.execute(sql,data)
        db.commit()
    except:
        db.rollback()
 
db.close()