#!/usr/bin/env python3
#################################################
# Protein Search using ECOD's AlphaFold DataBase
# Creater: Luke Coster
##################################################
#This is the extra databases needed to be imported
import pandas as pd
import os
# make sure you have pandas downloaded
# if not type "pip intall pandas"  in your command terminal
###################################################

#Opening Your data
print("What is the path to your proteomic data file (Excel Sheet)?")
your_data_loc = input("")
your_data_df = pd.read_excel(your_data_loc,header=None)
print(your_data_df.head(4))

print("What column is your uniprot IDs in (in python Column 1 = 0, Column 2 = 1 , ect.)?")
Uniprot_column = int(input())

print('Is there another column you want to cary over to the end (geneName, Z score, ect) (yes or no)')
extra = str(input())
if extra in ['yes','YES','Yes','yEs','yeS']:
    print('What column is the extra column')
    extra_column = int(input())
    print('What do you want the column to be called')
    extra_name = str(input())
print("Do you want to run all your proteins are just the top 'x' amount of proteins? (all or top)")
run = input("")


if run in ['Top', 'TOP','top','tOp','toP']:
    #find Z score
    print("What column is your Z score? (in python Column 1 = 0, Column 2 = 1 , ect.)")
    Z_score_column = int(input())
    #ask amount
    print("How many proteins do you want to look at? (starts at the top Z score)")
    number_of_proteins = int(input())
    #does the organizing and sorting
    your_data_df= your_data_df.sort_values(by=your_data_df.columns[Z_score_column], ascending=False)
    your_data_df = your_data_df.head(number_of_proteins)

print("what would you like the output data to be called?")
output_file = input("") + ".xlsx"


#making a dictionary of your data
your_data = {'ID':your_data_df[your_data_df.columns[Uniprot_column]].to_list()}
if extra in ['yes','YES','Yes','yEs','yeS']:
    your_data[extra_name]= your_data_df[your_data_df.columns[extra_column]].to_list() #This wont come up again till the end

print("preparing the code")
human_alpha_fold_class_raw_df = pd.read_excel("HomSa_raw_domains.xlsx",header=None) #Contains Uniprot ID's And ECOD domain classifications for AlphaFold Models
ECOD_domain_dictionary_raw_df = pd.read_excel("ecod.latest.domains.xlsx") #ECOD domain classification ID  Dictionary (contains duplicates and redundancies)(version 1.6)

#Cleaning redundancies and duplicates or data that is not needed
print('opened files')
ECOD_domain_dictionary_df = ECOD_domain_dictionary_raw_df.drop(ECOD_domain_dictionary_raw_df.columns[[0,1,2,4,5,6,7,8,13,14,15]], axis = 1)
ECOD_domain_dictionary_df.drop_duplicates(inplace = True)
human_alpha_fold_class_df = human_alpha_fold_class_raw_df.drop(human_alpha_fold_class_raw_df.columns[[1,2,4,5]], axis = 1)
human_alpha_fold_class_df.drop_duplicates(inplace= True)

#Making dictionaries
alpha_fold_human = {'ID': human_alpha_fold_class_raw_df[human_alpha_fold_class_raw_df.columns[0]].tolist(),'Code':human_alpha_fold_class_raw_df[human_alpha_fold_class_raw_df.columns[1]].tolist()}
ECOD_domain_dictionary = {'Code':ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[0]].to_list(),'arch':ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[1]].to_list(), 'x': ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[2]].to_list(),'h':ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[3]].to_list(), 't': ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[4]].to_list()}
print("All Ready\n\thello world")

#starting the process
processing_data = {'ID':[],'Code':[],'arch':[],'x':[],'h':[],'t':[]}
for indx in range(0,len(alpha_fold_human['ID'])):
    if alpha_fold_human['ID'][indx] in your_data['ID']:
        processing_data['ID'] = processing_data['ID'] + alpha_fold_human['ID'][indx]
        processing_data['Code'] = processing_data['Code'] + alpha_fold_human['Code'][indx]

for code in processing_data['Code']:
    indx = ECOD_domain_dictionary['Code'].index(code)
    processing_data['arch'] = processing_data['arch'] + ECOD_domain_dictionary['arch'][indx]
    processing_data['x'] = processing_data['x'] + ECOD_domain_dictionary['x'][indx]
    processing_data['h'] = processing_data['h'] + ECOD_domain_dictionary['h'][indx]
    processing_data['t'] = processing_data['t'] + ECOD_domain_dictionary['t'][indx]    

print('We classified '+ str(len(processing_data['arch']))+ 'proteins')

#finding unclassified proteins
count = 0 #this is a dumpy variable to count unclassified proteins
for id in your_data['ID']:
    if id not in processing_data['ID']:
        processing_data['ID'] = processing_data['ID'] + [id]
        processing_data['Code'] = processing_data['Code'] + ['not_found']
        processing_data['x'] = processing_data['x'] + ['not_found']
        processing_data['h'] = processing_data['h'] + ['not_found']
        processing_data['t'] = processing_data['t'] + ['not_found']
        count = count + 1
print(str(count) + " proteins were unclassified")

if extra in ['yes','YES','Yes','yEs','yeS']:
    processing_data[extra_name] = []
    for id in processing_data['ID']:
        indx = your_data.index(id)
        processing_data[extra_name] = processing_data[extra_name] + your_data[extra_name][indx]
    output_df = pd.DataFrame({extra_name: processing_data[extra_name],'ID': processing_data['ID'], 'Code': processing_data['Code'], 'arch' : processing_data['arch'], 'x_name' : processing_data['x'], 'h_name' : processing_data['h'],'t_name': processing_data['t']})
else:
    output_df = pd.DataFrame({'ID': processing_data['ID'], 'Code': processing_data['Code'], 'arch' : processing_data['arch'], 'x_name' : processing_data['x'], 'h_name' : processing_data['h'],'t_name': processing_data['t']})

output_df.to_excel(output_file, index =False)

print("Do you want a short summarry")
if str(input()) in ['yes','YES','Yes','yEs','yeS']:
    print('Making a summary')
    summary = {}
    for arch in processing_data['arch']:
        summary[arch] = processing_data['arch'].count(arch)
    for arch in summary.keys():
        print( str(arch)+ ": " +str(int(summary[arch])/len(processing_data['arch'])) + "%")
    #this makes a ranking code that will tell the top five
    rank = {}
    for code in processing_data['Code']: # this makes the counts for all the codes
        rank[code]= processing_data['Code'].count(code)
    rank['rank']=['NA','NA','NA','NA','NA']# next part the five most common codes
    rank['NA'] = 0
    def decode(code): #this will be used later to print the 
        if code != 'NA': # this if makes sure it does not crash if there are less than five codes
            indx = ECOD_domain_dictionary['Code'].index(code)
            print('\t'+ECOD_domain_dictionary['arch'][indx]+" | "+ ECOD_domain_dictionary['x'][indx]+" | "+ECOD_domain_dictionary['h'][indx]+' | '+ECOD_domain_dictionary['t'][indx]+'')
    for code in rank.keys():
        if rank[code] > rank[['rank'][4]]:
            if rank[code] > rank[['rank'][3]]:
                if rank[code] > rank[['rank'][2]]:
                    if rank[code] > rank[['rank'][1]]:
                        if rank[code] > rank[['rank'][0]]:
                            rank['rank']= [code] + rank['rank']
                        else:
                            rank['rank']= rank['rank'][0] + [code] + rank['rank'][1:]
                    else:
                        rank['rank']= rank['rank'][:2] + [code] + rank['rank'][2:]
                else:
                    rank['rank']= rank['rank'][:3] + [code] + rank['rank'][3:]
            else:
                        rank['rank']= rank['rank'][:4] + [code] + rank['rank'][4]
        if len(rank['rank']) > 5:
            rank['rank'] = rank['rank'][:5]
    print('1st is '+rank['rank'][0]+" with " + rank[['rank'][0]] ) 
    decode(rank[['rank'][0]])
    print('2nd is '+rank['rank'][1]+" with " + rank[['rank'][1]]) 
    decode(rank[['rank'][1]])
    print('3rd is '+rank['rank'][2]+" with " + rank[['rank'][2]])
    decode(rank[['rank'][2]])
    print('3rd is '+rank['rank'][3]+" with " + rank[['rank'][3]])
    decode(rank[['rank'][3]])
    print('3rd is '+rank['rank'][4]+" with " + rank[['rank'][4]])
    decode(rank[['rank'][4]])