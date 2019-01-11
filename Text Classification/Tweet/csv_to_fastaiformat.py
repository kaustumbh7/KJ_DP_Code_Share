import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Tweets.csv')

X = df.iloc[:, [1,10]].values
l=len(X)
#print(l)
#print(X)

pos=[]
neg=[]
neutral=[]
for i in range(len(X)):
	if X[i][0]=="positive":
		pos.append(X[i][1])
	if X[i][0]=="negative":
		neg.append(X[i][1])
	if X[i][0]=="neutral":
		neutral.append(X[i][1])

for i in range(len(pos)):
	with open(str(i)+'.txt','w+',encoding='utf-8') as fd:
		fd.write(pos[i])

for i in range(len(neg)):
	with open(str(i)+'.txt','w+',encoding='utf-8') as fd:
		fd.write(neg[i])

for i in range(len(neutral)):
	with open(str(i)+'.txt','w+',encoding='utf-8') as fd:
		fd.write(neutral[i])