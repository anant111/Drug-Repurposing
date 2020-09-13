import pandas as pd

df = pd.read_csv('names.csv')

columns = list(df) 


df1 = pd.read_csv('pos_neg.csv')
a = []
for w in df1:
    a.append(w)

df_new = pd.DataFrame()

for i in columns:
	#print()
	b= []
	for j in range(0,35783):
		if  df1[a[0]][j]==i:
			for k in range (431, 485):     #431 to 485 for negs
				 b.append(df1[a[k]][j])
	df_f = pd.DataFrame(b)
	df_new = pd.concat([df_new, df_f], axis=1)

df_new.to_csv('median>1_data_neg.csv')
