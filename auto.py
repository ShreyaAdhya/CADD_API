import requests
import json
import pandas as pd
import itertools

#reading the data from a .CSV file containing chromosome number, position, alternate and reference allele
df = pd.read_csv('Data.csv')
#df.head(3)

#Converting df data into String datatype
df = df.astype({'REF.x':'string'})
df = df.astype({'ALT.x':'string'})
df = df.astype({'POS':'string'})

#Extracting columns from the df : the Chromosome position, Reference allele and Alternate allele
ref_list = df["REF.x"].tolist()
alt_list = df["ALT.x"].tolist()
pos_list = df["POS"].tolist()

#Introducing an empty df
df_final = pd.DataFrame()


for i, ref in enumerate(ref_list): 
    #Introduce empty df to hold the value of each query
    df2 = pd.DataFrame()
    
    #Extracting the data using API in form of JSON file
    link = "https://cadd.gs.washington.edu/api/v1.0/GRCh38-v1.5/11:"+pos_list[i]+"_"+ref+"_"+alt_list[i]
    #print(link)  
    response = requests.get(link)
    #type(response)
    
    #Saving the JSON file
    with open(pos_list[i]+"_"+ref+"_"+alt_list[i]+'.json', 'wb') as outf:
        outf.write(response.content)
        
    #Converting JSON file to df    
    df2 = pd.read_json(pos_list[i]+"_"+ref+"_"+alt_list[i]+'.json', orient='records')  
    
    #Combing the data into the final df
    df_final = pd.concat([df_final,df2])
    
#Reordering the column names
df_final = df_final[['Chrom','Pos','Ref','Alt','RawScore','PHRED']]
df_final = df_final.reset_index(drop=True)
    
#Saving as a .csv file
df_final.to_csv('Data_of_CADD.csv')
