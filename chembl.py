from chembl_webresource_client.new_client import new_client
import pandas as pd
dfp = pd.read_csv('protein.csv')
df = pd.DataFrame()
target = new_client.target
for l in range(0,519):
	gene_name = dfp['Gene'][l]
	res = target.search(gene_name)
	act_df = pd.DataFrame(res)
	print(act_df)
	if act_df.empty:
		continue

	#act_df = act_df[[ 'target_chembl_id','target_organism', 'target_pref_name'
     #                , 'parent_molecule_chembl_id','molecule_chembl_id','molecule_pref_name'
      #               , 'pchembl_value', 'standard_type','standard_relation', 'standard_value', 'standard_units'
       #              , 'assay_chembl_id','document_chembl_id','src_id']]
	df = pd.concat([df, act_df])
	print(act_df)
	print("\n")
	df.to_csv('asd.csv')
#from chembl_webresource_client import *
#targets = TargetResource()
#t = targets.get(uniprot='Q13936')
#print(t)