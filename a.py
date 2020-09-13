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
    url_full = requests.get( url_full_string ).json() #This calls the information back from the API using the 'requests' module, and converts it to j
son format
    url_activities = url_full['activities'] #This is a list of the results for activities

    # This 'while' loop iterates over several pages of records (if required), and collates the list of results
    while url_full['page_meta']['next']:
        url_full = requests.get(url_stem + url_full['page_meta']['next']).json()
        url_activities = url_activities + url_full['activities'] #Add result (as a list) to previous list of results

    # Convert the list of results into a Pandas dataframe:
    act_df = pd.DataFrame(url_activities)

    # Print out some useful information:
    print("This is the url string that calls the 'Activities' API with the initial query specification:\n{}".format(url_full_string) )
    print("\nThese are the available columns for the Activities API:\n{}".format(act_df.columns))

    #Specify which columns to keep so that the size of the dataframe becomes more manageable:
    act_df = act_df[[  'target_chembl_id','target_organism', 'target_pref_name'
                     , 'parent_molecule_chembl_id','molecule_chembl_id','molecule_pref_name'
                     , 'pchembl_value', 'standard_type','standard_relation', 'standard_value', 'standard_units'
                     , 'assay_chembl_id','document_chembl_id','src_id']]

    return act_df

#====================================================================#

# Extract the list of compounds from the previous dataframe ('act_df'), and call the 'molecule' API to find their molecular properties etc, so that this list can be refined

def find_properties_of_compounds(act_df):

    #First find the list of compounds that are within the act_df dataframe:
    
    cmpd_chembl_ids = list(set(act_df['molecule_chembl_id']))
    print("There are {} compounds initially identified as active on the known targets. e.g.".format(len(cmpd_chembl_ids)))
    print(cmpd_chembl_ids[0:2])

    #For the identified compounds, extract their molecular properties and other information from the 'molecule' ChEMBL API
    #Specify the input parameters:
    cmpd_chembl_ids = ",".join(cmpd_chembl_ids[0:]) #Amend the format of the text string of compounds so that it is suitable for the API call
    limit = 100 #Limit the number of records pulled back for each url call

    # Set up the call to the ChEMBL 'molecule' API
    # Remember that there is a limit to the number of records returned in any one API call (default is 20 records, maximum is 1000 records)
    # So need to iterate over several pages of records to gather all relevant information together!
    url_stem = "https://www.ebi.ac.uk" #This is the stem of the url
    url_full_string = url_stem + "/chembl/api/data/molecule.json?molecule_chembl_id__in={}&limit={}".format(cmpd_chembl_ids, limit) #This is the full
 url with the specified input parameters
    url_full = requests.get( url_full_string ).json() #This calls the information back from the API using the 'requests' module, and converts it to j
son format
    url_molecules = url_full['molecules'] #This is a list of the results for activities

    # This 'while' loop iterates over several pages of records (if required), and collates the list of results
    while url_full['page_meta']['next']:
        url_full = requests.get(url_stem + url_full['page_meta']['next']).json()
        url_molecules = url_molecules + url_full['molecules'] #Add result (as a list) to previous list of results

    #Convert the list of results into a Pandas dataframe:
    mol_df = pd.DataFrame(url_molecules)

    #Print out some useful information:
    print("This is the url string that calls the 'Molecule' API with the specified query\n{}".format(url_full_string) )
    print("\nThese are the available columns for the Molecule API:\n{}".format(mol_df.columns))

    # Select only relevant columns:
    mol_df = mol_df[[ 'molecule_chembl_id','pref_name', 'molecule_hierarchy'
                         , 'molecule_properties', 'max_phase']]

    # And convert cells containing a dictionary to individual columns in the dataframe so that is it easier to filter!
    # Molecule hierarchy:
    mol_df['parent_chembl_id'] = mol_df['molecule_hierarchy'].apply(lambda x: x['parent_chembl_id'])

    #Physicochemical properties (only report if cells are not null)
    mol_df['acd_logd'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['acd_logd'])
    mol_df['acd_logp'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['acd_logp'])
    mol_df['acd_most_apka'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['acd_most_apka'])
    mol_df['acd_most_bpka'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['acd_most_bpka'])
    mol_df['alogp'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['alogp'])
    mol_df['hba'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['hba'])
    mol_df['hbd'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['hbd'])
    mol_df['mw_freebase'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['mw_freebase']) #This is th
e mwt of the parent compound
    mol_df['full_mwt'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['full_mwt']) #This is the mwt
of the full compound including any salt
    mol_df['num_ro5_violations'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['num_ro5_violations'
])
    mol_df['psa'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['psa'])
    mol_df['heavy_atoms'] = mol_df.loc[ mol_df['molecule_properties'].notnull(), 'molecule_properties'].apply(lambda x: x['heavy_atoms'])

    print(mol_df)

    return mol_df

#====================================================================#

# Filter the compound list based on relevant information

def filter_list_of_compounds(mol_df):

    # Filter the compounds based on their molecular properties, or max_phase, for example:

    # Now keep only molecules with max_phase = 4 (ie approved drugs), for example:
    res = mol_df[ mol_df['max_phase'] == 4 ]

    #Now keep only molecules with max_phase = 4 (ie approved drugs), for example:
    res = mol_df[ mol_df['max_phase'] == 4 ]

    # # OR keep only molecules with less than 400 amu, for example:
    # # but first need to convert strings to float for 'full_mwt':
    # mol_df['full_mwt'] = mol_df['full_mwt'].apply(lambda x: float(x) )
    # res = mol_df[ mol_df['full_mwt'] < 400 ]

    #Display only top few rows:
    print(res.head())

    return res

#====================================================================#

def main():

    # using a list of known targets, find compounds that are active on these targets:
    targets = ['CHEMBL1848', 'CHEMBL3394'] # xxx
    act_df = find_bioactivities_for_targets(targets)

    # extract the list of compounds, and find these compounds' properties:
    mol_df = find_properties_of_compounds(act_df)

    # Filter the compound list based on relevant information
    filtered_mol_df = filter_list_of_compounds(mol_df)

    print("FINISHED\n")

#====================================================================#

if __name__=="__main__":
    main()

#====================================================================#


