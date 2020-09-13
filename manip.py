#import pandas as pd

#df = pd.read_csv('day0_12.csv')
#columns = list(df) 

#for i in columns:
#	for j in range(0,56637):
#		if df[i][j]==0:
#			df[i][j]=1

#df.to_csv('day0_12_all_positives.csv')

import pandas as pd 
import math
import numpy as np
data = pd.read_csv("day0_12_all_positives.csv") 

a=[]
i=1

for columns in data:
    a.append(columns)

df = pd.DataFrame()
for i in range(1,len(a),2):
	df_l = pd.DataFrame(np.log2(data[a[i]].div(data[a[i+1]])))
	df = pd.concat([df, df_l], axis=1)

df.to_csv('log_score.csv')
	
