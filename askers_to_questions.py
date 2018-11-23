
# coding: utf-8

# In[5]:


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
import mysql.connectorimport pandas as pd 
import requests


# In[6]:


def request_to_stack(method, url, headers, querystring):
    response = requests.request(method, url, headers=headers, params=querystring)
    return (response.text)


# In[22]:


def fetch_top_askers(tag):
    base_url = "https://api.stackexchange.com/2.2/tags/"+ tag +"/top-askers/month"
    querystring = {"site":"stackoverflow"}
    headers = {'Cache-Control': 'no-cache'}
    method = "GET"
    result = request_to_stack(method, base_url,headers,querystring)
    return result


# In[23]:


def fetch_ques_of_user(user_id):
    base_url = "https://api.stackexchange.com/2.2/users/"+user_id+"/questions"
    querystring = {"site":"stackoverflow","order":"desc"}
    headers = {'Cache-Control': 'no-cache'}
    method = "GET"
    result = request_to_stack(method, base_url,headers,querystring)
    return result    


# In[32]:


askers = fetch_top_askers('php')
data = json.loads(askers)

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="stack_overflow"
)cursor = db.cursor()

for item in data['items']:
    user_id = str(item['user']['user_id'])
    post_count = item['post_count']
    questions = fetch_ques_of_user(user_id)
    ques_data = json.loads(questions)
#     print(ques_data)
    for ques in ques_data['items']:
        ques_title = ques['title']
        ques_id = ques['question_id']
        ques_creation_date = ques['creation_date']
        if ques['is_answered'] == True:
            answer_count = ques['answer_count']
        else:
            answer_count = 0
            if 'accepted_answer_id' in ques:
                accepted_answer_id = ques['accepted_answer_id']
        data = [user_id, ques_id, ques_title, ques_creation_date, answer_count, accepted_answer_id]
        print(data)
        sql = 'insert into top_askers_questions (user_id, ques_id, ques_title, ques_creation_date, answer_count, accepted_ans_id ) values (%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,data)
            db.commit()
        except:
            db.rollback()
            
db.close()
        
                
                
        

