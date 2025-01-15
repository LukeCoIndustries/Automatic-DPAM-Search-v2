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
def Protein_search(File,Uniprot_col,run,Output_name,extra = None, Extra_col=None, Extra_name=None, Zscore=None,Protein_count=None):
    your_data_df = pd.read_excel(File,header=None)
    Uniprot_column = int(Uniprot_col)
    if extra in ['yes','YES','Yes','yEs','yeS']:
        extra_column = int(Extra_col)
        extra_name = str(Extra_name)

    if run in ['Top', 'TOP','top','tOp','toP','top ']:
        #find Z score
        Z_score_column = int(Zscore)
        #ask amount
        number_of_proteins = int(Protein_count)
        #does the organizing and sorting
        your_data_df= your_data_df.sort_values(by=your_data_df.columns[Z_score_column], ascending=False)
        your_data_df = your_data_df.head(number_of_proteins)


    output_file = Output_name+ ".xlsx"


    #making a dictionary of your data
    your_data = {'ID':your_data_df[your_data_df.columns[Uniprot_column]].to_list()}
    if extra in ['yes','YES','Yes','yEs','yeS']:
        your_data[extra_name]= your_data_df[your_data_df.columns[extra_column]].to_list() #This wont come up again till the end

    print("preparing the code")
    human_alpha_fold_class_df = pd.read_excel("HomSa_raw_domains.xlsx",header=None) #Contains Uniprot ID's And ECOD domain classifications for AlphaFold Models
    ECOD_domain_dictionary_df = pd.read_excel("ecod.latest.domains.xlsx") #ECOD domain classification ID  Dictionary (contains duplicates and redundancies)(version 1.6)

    #Cleaning redundancies and duplicates or data that is not needed
    print('opened files')
    ECOD_domain_dictionary_df = ECOD_domain_dictionary_df.drop(ECOD_domain_dictionary_df.columns[[0,1,2,4,5,6,7,8,13,14,15]], axis = 1)
    ECOD_domain_dictionary_df.drop_duplicates(inplace = True)
    human_alpha_fold_class_df = human_alpha_fold_class_df.drop(human_alpha_fold_class_df.columns[[1,2,4,5]], axis = 1)
    human_alpha_fold_class_df.drop_duplicates(inplace= True)

    #Making dictionaries
    alpha_fold_human = {'ID': human_alpha_fold_class_df[human_alpha_fold_class_df.columns[0]].tolist(),'Code':human_alpha_fold_class_df[human_alpha_fold_class_df.columns[1]].tolist()}
    ECOD_domain_dictionary = {'Code':ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[0]].tolist(),'arch':ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[1]].tolist(), 'x': ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[2]].to_list(),'h':ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[3]].to_list(), 't': ECOD_domain_dictionary_df[ECOD_domain_dictionary_df.columns[4]].to_list()}

    #starting the process
    processing_data = {'ID':[],'Code':[],'arch':[],'x':[],'h':[],'t':[]}
    for indx in range(0,len(alpha_fold_human['ID'])):
        if alpha_fold_human['ID'][indx] in your_data['ID']:
            processing_data['ID'] = processing_data['ID'] + [alpha_fold_human['ID'][indx]]
            processing_data['Code'] = processing_data['Code'] + [alpha_fold_human['Code'][indx]]


    for code in processing_data['Code']:
        for indx in range(0,len(ECOD_domain_dictionary['Code'])):
            none_found = 0#this is a dumby variable to keep a track of proteins that have a code not in the dictionary
            if code in ECOD_domain_dictionary['Code'][indx]: #this extra step in necessary because soom codes have extra specificities
                processing_data['arch'] = processing_data['arch'] + [ECOD_domain_dictionary['arch'][indx]]
                processing_data['x'] = processing_data['x'] + [ECOD_domain_dictionary['x'][indx]]
                processing_data['h'] = processing_data['h'] + [ECOD_domain_dictionary['h'][indx]]
                processing_data['t'] = processing_data['t'] + [ECOD_domain_dictionary['t'][indx]]
                none_found = 1
                break
        if none_found == 0:
                processing_data['arch'] = processing_data['arch'] + ['not found in the ECOD dictionary']
                processing_data['x'] = processing_data['x'] + ['not found in the ECOD dictionary']
                processing_data['h'] = processing_data['h'] + ['not found in the ECOD dictionary']
                processing_data['t'] = processing_data['t'] + ['not found in the ECOD dictionary']


    print('We classified '+ str(len(processing_data['arch']))+' proteins')

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

    if extra in ['yes','YES','Yes','yEs','yeS']:
        processing_data[extra_name] = []
        for id in processing_data['ID']:
            indx = your_data['ID'].index(id)
            processing_data[extra_name] = processing_data[extra_name] + [your_data[extra_name][indx]]
        print(str(count) + " proteins were unclassified")
        output_df = pd.DataFrame({extra_name: processing_data[extra_name],'ID': processing_data['ID'], 'Code': processing_data['Code'], 'arch' : processing_data['arch'], 'x_name' : processing_data['x'], 'h_name' : 
        processing_data['h'],'t_name': processing_data['t']})
    else:
        output_df = pd.DataFrame({'ID': processing_data['ID'], 'Code': processing_data['Code'], 'arch' : processing_data['arch'], 'x_name' : processing_data['x'], 'h_name' : processing_data['h'],'t_name': processing_data['t']})

    output_df.to_excel(output_file, index =False)
    sumry = 'yes'
    sumry = str(input())
    if sumry in ['yes','YES','Yes','yEs','yeS']:
        print('Making a summary')
        summary = {}
        for arch in processing_data['arch']:
            summary[arch] = processing_data['arch'].count(arch)
        for arch in summary.keys():
            print( str(arch)+ ": " +str(round(((summary[arch])/len(processing_data['arch'])*100),2)) + "%")
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
            if code != 'rank':
                if rank[code] > rank[rank['rank'][4]]:
                    if rank[code] > rank[rank['rank'][3]]:
                        if rank[code] > rank[rank['rank'][2]]:
                            if rank[code] > rank[rank['rank'][1]]:
                                if rank[code] > rank[rank['rank'][0]]:
                                    rank['rank']= [code] + rank['rank']
                                else:
                                    rank['rank']= [rank['rank'][0]] + [code] + rank['rank'][1:]
                            else:
                                rank['rank']= rank['rank'][:2] + [code] + rank['rank'][2:]
                        else:
                            rank['rank']= rank['rank'][:3] + [code] + rank['rank'][3:]
                    else:
                                rank['rank']= rank['rank'][:4] + [code] + [rank['rank'][4]]
                if len(rank['rank']) > 5:
                    rank['rank'] = rank['rank'][:5]
        
        print('1st is '+str(rank['rank'][0])+" with " + str(rank[rank['rank'][0]])) 
        decode(rank['rank'][0])
        print('2nd is '+str(rank['rank'][1])+" with " + str(rank[rank['rank'][1]])) 
        decode(rank['rank'][1])
        print('3rd is '+str(rank['rank'][2])+" with " + str(rank[rank['rank'][2]]))
        decode(rank['rank'][2])
        print('4th is '+str(rank['rank'][3])+" with " + str(rank[rank['rank'][3]]))
        decode(rank['rank'][3])
        print('5th is '+str(rank['rank'][4])+" with " + str(rank[rank['rank'][4]]))
        decode(rank['rank'][4])