# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 00:37:13 2022

@author: culro
"""

import pandas as pd
import glob
# All files and directories ending with .txt and that don't begin with a dot:
import os
import seaborn as sns
import matplotlib.pyplot as plt
import re
# !pip install tweet-preprocessor
import preprocessor as p

#%%

x = "C:\\Users\culro\OneDrive\Desktop\Fall'21\Data Science for Product Managers\Project Social Media Analysis\\"
# print(glob.glob(x+"*")) 
data = pd.read_excel(x+"Stream (2).xlsx")

print(os.getcwd())
#%%

data2 = data.drop((data.tail(10).index))
#%%


# x = (data2["No. of Followers/Daily Unique Visitors"].loc[data2["No. of Followers/Daily Unique Visitors"]>0].mean())

# for i in data2['Sound Bite Text']:
#     if 'http' in i:
#         print("<------------------------------------->")
#         print(i)

# print(data2['Sound Bite Text'].str.contains('http').value_counts()[True])
        

    
#%%
corpus=[]
data2["clean_soundbite"] = None
for i in range(0, len(data2['Sound Bite Text'])):
     review = data2['Sound Bite Text'][i]
     review = review.encode('ascii', 'ignore').decode() 
     # review = review.split()
     review = re.sub("http*\S+", "", review, flags=re.IGNORECASE)
     review = re.sub("www*\S+", "", review, flags=re.IGNORECASE)
     review = re.sub("\S+@\S+", "", review)
     review = re.sub("\S+\.com", "", review, flags=re.IGNORECASE)
     review = re.sub("\S+\s\.com\S+", "", review, flags=re.IGNORECASE)
     review = re.sub("\S+\s\.com", "", review, flags=re.IGNORECASE)
     review = re.sub(r"[\([{})\]]", "", review)
     corpus.append(review)
     data2['clean_soundbite'][i] = review
     
#%%
# for i in data2.index:
#     if "@" in data2.loc[i]['Sound Bite Text']:
#         print(i)

#%%
# print(corpus[44581])
# print(data2.loc[44581]['Sound Bite Text'])
#%%
# regex = [r'\S+\s\.com\S+', r'\S+\s\.com']
# j = 0
# for i in corpus:
#     for x in regex:
#         matches = re.findall(x, i)
#         if matches != []:
#             print(x)
#             print(j,"---", matches)
#     j+=1
        
#%%
#do not remove hastags--- p.OPT.HASHTAG
def preprocess_tweet(row):
    p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.RESERVED, p.OPT.MENTION, p.OPT.SMILEY)
    text = row['Sound Bite Text']
    text = p.clean(text)
    return text
data2['clean_soundbite'] = data2.apply(preprocess_tweet, axis=1)

#%%
data2[['Sound Bite Text','clean_soundbite']].to_excel("clean_Stream (2).xlsx")  

#%%#%%
# for i in data2.index:
#     if (data2.loc[i]['clean_soundbite'].find(".com")!=-1):
#         print(data2.loc[i]['clean_soundbite'])
#         print("-------")
        
#%%
print(data2.loc[48294]['Sound Bite Text'])
print("-----")
print(data2.loc[48294]['clean_soundbite'])

#%%
data2['clean_soundbite'] = data2['clean_soundbite'].str.lower()
data2['iphone x'] = 0
data2['iphone 8'] = 0
data2['galaxy'] = 0
for i in data2['clean_soundbite'].index:
    if "iphone x" in data2.loc[i]['clean_soundbite']:
        data2['iphone x'][i] = 1
    if "iphone 8" in data2.loc[i]['clean_soundbite']:
        data2['iphone 8'][i] = 1
    if "galaxy" in data2.loc[i]['clean_soundbite']:
        data2['galaxy'][i] = 1
#%%
for i in data2['iphone x'].index:
    if data2.loc[i]['iphone x'] == 1:
        print(data2.loc[i]['iphone x'])
        
#%%

print(data2.groupby(['iphone x'])["clean_soundbite"].count())
print(data2.groupby(['iphone 8'])["clean_soundbite"].count())
print(data2.groupby(['galaxy'])["clean_soundbite"].count())

x = 0 #iphone x only tweets
i8 = 0 #iphone 8 only tweets
g = 0 #galaxy only tweets
for i in data2['clean_soundbite'].index:
    if data2['iphone x'][i] == 1 and data2['iphone 8'][i] == 0 and data2['galaxy'][i] == 0:
        x+=1
    if data2['iphone x'][i] == 0 and data2['iphone 8'][i] == 1 and data2['galaxy'][i] == 0:
        i8+=1
    if data2['iphone x'][i] == 0 and data2['iphone 8'][i] == 0 and data2['galaxy'][i] == 1:
        g+=1
        

print(x, i8, g)


#%%
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()





entities = []
labels = []
position_start = []
position_end = []
for i in data2['clean_soundbite']:
    doc = nlp(i)
    for ent in doc.ents:
        entities.append(ent)
        labels.append(ent.label_)
        position_start.append(ent.start_char)
        position_end.append(ent.end_char)
    
    df = pd.DataFrame({'Entities': entities, 'Labels': labels, 'position_start': position_start, 'Position_end': position_end})
    

print(df)
