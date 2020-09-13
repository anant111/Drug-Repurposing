import pandas as pd # uses pandas python module to view and analyse data
import requests # this is used to access json files

#====================================================================#

# using a list of known targets, find compounds that are active on these targets:

def find_bioactivities_for_targets(targets):

    targets = ",".join(targets) # join the targets into a suitable string to fulfil the search conditions of the ChEMBL api
    assay_type = 'B' # only look for binding assays
    pchembl_value = 5 # xxx specify a minimum threshold of the pCHEMBL activity value. Greater than or equal to 5 (10 microM) is a typical minimum rule of thumb for binding activity between a compound and a protein target
    limit = 100 # limit the number of records pulled back for each url call xxx

    # set up the call to the ChEMBL 'activity' API.
    # Remember that there is a limit to the number of records returned in any one API call (default is 20 records, maximum is 1000 records).
    # So we need to iterate over several pages of results to gather all relevant information together.
    url_stem = "https://www.ebi.ac.uk" #This is the stem of the url
    url_full_string = url_stem + "/chembl/api/data/activity.json?target_chembl_id__in={}&assay_type={}&pchembl_value__gte={}&limit={}".format(targets
, assay_type, pchembl_value, limit) #This is the full url with the specified input parameters
    url_full = requests.get( url_full_string ).json() #This calls the information back from the API using the 'requests' module, and converts it to json format
    url_activities = url_full['activities'] #This is a list of the results for activities

    # This 'while' loop iterates over several pages of records (if required), and collates the list of results
    while url_full['page_meta']['next']:
        url_full = requests.get(url_stem + url_full['page_meta']['next']).json()
        url_activities = url_activities + url_full['activities'] #Add result (as a list) to previous list of results
    

    # Convert the list of results into a Pandas dataframe:
    act_df = pd.DataFrame(url_activities)
    if url_activities ==[]:
        return act_df
    # Print out some useful information:
    print("This is the url string that calls the 'Activities' API with the initial query specification:\n{}".format(url_full_string) )
    print("\nThese are the available columns for the Activities API:\n{}".format(act_df.columns))

    #Specify which columns to keep so that the size of the dataframe becomes more manageable:
    act_df = act_df[[ 'target_chembl_id','target_organism', 'target_pref_name'
                     , 'parent_molecule_chembl_id','molecule_chembl_id','molecule_pref_name'
                     , 'pchembl_value', 'standard_type','standard_relation', 'standard_value', 'standard_units'
                     , 'assay_chembl_id','document_chembl_id','src_id']]

    return act_df

#====================================================================#



def main():

    # using a list of known targets, find compounds that are active on these targets:
    targets = ['CHEMBL1075113',
'CHEMBL1163112',
'CHEMBL1163129',
'CHEMBL1255126',
'CHEMBL1287627',
'CHEMBL1697668',
'CHEMBL1741179',
'CHEMBL1743124',
'CHEMBL1743294',
'CHEMBL1781870',
'CHEMBL1795193',
'CHEMBL1798',
'CHEMBL1844',
'CHEMBL1868',
'CHEMBL1914279',
'CHEMBL1936',
'CHEMBL1938217',
'CHEMBL1971',
'CHEMBL1975',
'CHEMBL2007626',
'CHEMBL2034810',
'CHEMBL2093872',
'CHEMBL2095942',
'CHEMBL3301385',
'CHEMBL3301386',
'CHEMBL2145',
'CHEMBL2146306',
'CHEMBL2146311',
'CHEMBL2148',
'CHEMBL2150844',
'CHEMBL2176777',
'CHEMBL2176778',
'CHEMBL2311230',
'CHEMBL233',
'CHEMBL2331058',
'CHEMBL2362996',
'CHEMBL2363000',
'CHEMBL2363065',
'CHEMBL2364156',
'CHEMBL2364158',
'CHEMBL2364167',
'CHEMBL2364168',
'CHEMBL2399',
'CHEMBL2406895',
'CHEMBL2413',
'CHEMBL2434',
'CHEMBL2494',
'CHEMBL274',
'CHEMBL275',
'CHEMBL278',
'CHEMBL2789',
'CHEMBL2826',
'CHEMBL2889',
'CHEMBL2926',
'CHEMBL2959',
'CHEMBL3038495',
'CHEMBL3045',
'CHEMBL3108643',
'CHEMBL3161',
'CHEMBL3172',
'CHEMBL3217394',
'CHEMBL3217402',
'CHEMBL3240',
'CHEMBL3243',
'CHEMBL3259470',
'CHEMBL3267',
'CHEMBL3301399',
'CHEMBL3308911',
'CHEMBL3407317',
'CHEMBL3414409',
'CHEMBL3421522',
'CHEMBL3514',
'CHEMBL3540',
'CHEMBL3559386',
'CHEMBL3559687',
'CHEMBL3562166',
'CHEMBL3580506',
'CHEMBL3580522',
'CHEMBL3596074',
'CHEMBL3621023',
'CHEMBL3621036',
'CHEMBL3638',
'CHEMBL3712914',
'CHEMBL3712964',
'CHEMBL3714081',
'CHEMBL3736',
'CHEMBL3856162',
'CHEMBL3965',
'CHEMBL4076',
'CHEMBL4105758',
'CHEMBL4105787',
'CHEMBL4105810',
'CHEMBL4105884',
'CHEMBL4105898',
'CHEMBL4163',
'CHEMBL4295690',
'CHEMBL4295829',
'CHEMBL4295895',
'CHEMBL4296103',
'CHEMBL4522',
'CHEMBL4550',
'CHEMBL4679',
'CHEMBL4685',
'CHEMBL4761',
'CHEMBL4789',
'CHEMBL4801',
'CHEMBL4805',
'CHEMBL4843',
'CHEMBL4850',
'CHEMBL4865',
'CHEMBL4941',
'CHEMBL5037',
'CHEMBL5100',
'CHEMBL5215',
'CHEMBL5251',
'CHEMBL5255',
'CHEMBL5335',
'CHEMBL5349',
'CHEMBL5425',
'CHEMBL5433',
'CHEMBL5641',
'CHEMBL5785',
'CHEMBL5811',
'CHEMBL5813',
'CHEMBL5842',
'CHEMBL5876',
'CHEMBL5936',
'CHEMBL5951',
'CHEMBL5953',
'CHEMBL5994',
'CHEMBL6101',
]
    df = pd.DataFrame()
    for i in targets:
        a = []
        a.append(i)
        act_df = find_bioactivities_for_targets(a)
        df = pd.concat([df, act_df])
        print(act_df)
        print("\n")
        df.to_csv('asd.csv')

    #print(act_df)
    #df.to_csv('asd.csv')
    print("FINISHED\n")

#====================================================================#

if __name__=="__main__":
    main()

#====================================================================#


