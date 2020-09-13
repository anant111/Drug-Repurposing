import pandas as pd
dfu2c = pd.read_csv('uniprot2chembl.csv')
dfwd = pd.read_csv('without_duplicated.csv')
columns_u2c = list(dfu2c) 
columns_wd = list(dfwd)

df_new = pd.DataFrame()
a=0
for j in range(0,54):
	b = []
	for l in range(0,131):
		if dfwd['chembl_id'][j] == dfu2c['CHEMBL ID'][l]:
			b.append(dfu2c['UNIPROT ID'][l])
			b.append(dfwd['chembl_id'][j])
			a=a+1
	if b != []:
		df_f = pd.DataFrame(b)
		df_f = df_f.transpose()
		df_new = pd.concat([df_new, df_f], axis=0)
		print(a)
		print(j)
		print("\n")
df_new.to_csv('a.csv')	

a=0
df_new1 = pd.DataFrame()
for j in range(0,88):
	b = []
	for l in range(0,131):
		if dfwd['target_chembl_id'][j] == dfu2c['CHEMBL ID'][l]:
			b.append(dfu2c['UNIPROT ID'][l])
			b.append(dfwd['target_chembl_id'][j])
			a=a+1
	if b != []:
		df_f = pd.DataFrame(b)
		df_f = df_f.transpose()
		df_new1 = pd.concat([df_new1, df_f], axis=0)
		print(a)
		print(j)
		print("\n")
df_new1.to_csv('b.csv')