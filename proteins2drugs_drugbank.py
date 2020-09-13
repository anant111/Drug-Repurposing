import pandas as pd

dfd = pd.read_csv('proteins3.csv')
dfp = pd.read_csv('gene2protein.csv')
columns_drugs = list(dfd) 
columns_prot = list(dfp)

df_new = pd.DataFrame()
a=0
for j in range(0,26878):
	b = []
	for l in range(0,519):
		if dfd['uniprot_id'][j] == dfp['Entry'][l]:
			b.append(dfd['uniprot_id'][j])
			b.append(dfp['Gene'][l])
			b.append(dfd['drugbank_id'][j])
			b.append(dfd['name'][j])
			b.append(dfd['organism'][j])
			b.append(dfd['category'][j])
			b.append(dfd['groups'][j])
			b.append(dfd['known_action'][j])
			b.append(dfd['actions'][j])
			b.append(dfd['categories'][j])
			a=a+1
	if b != []:
		df_f = pd.DataFrame(b)
		df_f = df_f.transpose()
		df_new = pd.concat([df_new, df_f], axis=0)
		print(a)
		print(j)
		print("\n")
df_new.to_csv('a.csv')		


