# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:10:29 2022

@author: dcs839
"""

### Data analysis - Outlier test for whole samples ###

## Requirements ##
# Raw data - Metabolomics #

## Libraries ##

import os
import numpy as np
import pandas as pd
from OUTLIERS import smirnov_grubbs as grubbs

## functions ##

##  Files ##

# Input #
file1_input = "Viime 2_v2.csv"

# Output #
file2_transpose = "Viime 2_transposed.csv"

file3_init_sample_lookup_file = "Initial_Sample_lookup_table.csv"
file4_init_sample_file = "Initial_raw_data_lookup_C_and_D_transposed.csv"

file5_outliers = "Outlier_table.csv"

file6_look_up = "Sample_lookup_table.csv"
file7_sample_file = "raw_data_C_and_D_transposed.csv"

## Folders ##
# input #
Folder1 = "Data/Raw data"

# output #
Folder2 = "Data/Data cleaning"
Folder3 = "Data/Lookup data"


os.makedirs(Folder2,exist_ok=True)
os.makedirs(Folder3,exist_ok=True)


## Global variables ##

# initial data variables for data cleaning #

init_Name_list = []
init_QC_dict = {}
init_Group_D_dict = {}
init_Group_C_dict = {}

# Outlier calculations #

Outlier_dict_C = {}
Outlier_dict_D = {}

Group_C_without_outliers = {}
Group_D_without_outliers = {}

## Transpose raw data with pandas  ##

if os.path.isfile(os.path.join(Folder1,file2_transpose)):
    pass
else:
    df = pd.read_csv(os.path.join(Folder1,file1_input),delimiter=";",encoding = "cp1252")
    
    df_transposed = df.transpose()
    
    df_transposed.to_csv(os.path.join(Folder1,file2_transpose),index=True,sep=";",header=False)

## read transposed raw data, extract Group C and D, and save as initial raw data ##

# create header for initial raw data table #
header = "Name"
header_QC = []
for x in range(1,16,1):
    header_QC.append("QC_{}".format(x))
header_D = []
for x in range(1,15,1):
    header_D.append("D_{}".format(x))
header_C = []
for x in range(1,14,1):
    header_C.append("C_{}".format(x))
    

# Read transported raw data -> write initial sample lookup table #
Header_flag = 1
with open(os.path.join(Folder2,file3_init_sample_lookup_file),'w+') as out:
    out.write("Sample number;ID\n")
    with open(os.path.join(Folder1,file2_transpose),'r') as read:
        for line in read:
            if Header_flag == 1:
                line = line.strip().replace('"','').split(";")
                QC = line[1:16]
                C_samples = line[56:69]
                D_samples = line[69:84]
                for x in range(0,len(header_QC),1):
                    out.write("{};{}\n".format(header_QC[x],QC[x]))
                for x in range(0,len(header_C),1):
                    out.write("{};{}\n".format(header_C[x],C_samples[x]))
                for x in range(0,len(header_D),1):
                    out.write("{};{}\n".format(header_D[x],D_samples[x]))
                Header_flag = 0
            else:
                pass
    read.close()    
out.close()

## Load sample lookup into dataframe ##
df_sample_lookup = pd.read_csv(os.path.join(Folder2,file3_init_sample_lookup_file),sep=";")
# Convert into dict #
df_sample_lookup_dict = df_sample_lookup.set_index('ID')['Sample number'].to_dict()
# Generate new header list #
Header_list = list(df_sample_lookup_dict.values())
## Load transposed raw data ##
df_raw = pd.read_csv(os.path.join(Folder1,file2_transpose),sep=";",skiprows=[1])
# Rename columns to new sample names #
df_raw.rename(columns=(df_sample_lookup_dict),inplace=True)

# Extract QC, group C, and group D #
df_raw_QC_C_D = df_raw[['Name']+Header_list]

## Save initial raw data table ##
df_raw_QC_C_D.to_csv(os.path.join(Folder2,file4_init_sample_file),index=False,sep=";")


## Run inital sampe outliers ##

with open(os.path.join(Folder2,file4_init_sample_file),'r') as read:
    next(read)
    for line in read:
        line = line.strip().split(";")
        Name = line[0]
        QC = line[1:16]
        Group_C = line[16:29]
        Group_D = line[29:43]
        init_Name_list.append(Name)
        init_QC_dict[Name] = np.array(QC,dtype=float)
        init_Group_D_dict[Name] = np.array(Group_D,dtype=float)
        init_Group_C_dict[Name] = np.array(Group_C,dtype=float)
read.close()

## run grubbs test for outliers in initial raw data ##

outlier_overview_C = {}
outlier_overview_D = {}

for key in init_Name_list:
    Outlier_dict_C[key] = {}
    Outlier_dict_D[key] = {}
    Group_C_without_outliers[key] = grubbs.test(init_Group_C_dict[key], alpha=.05)
    Group_D_without_outliers[key] = grubbs.test(init_Group_D_dict[key], alpha=.05)
    
    outlier_index_C = grubbs.two_sided_test_indices(init_Group_C_dict[key], alpha=.05)
    outlier_index_D = grubbs.two_sided_test_indices(init_Group_D_dict[key], alpha=.05)
    for i in outlier_index_C:
        outlier_sample_C = "C_{}".format(i+1)
        if outlier_sample_C in outlier_overview_C:
            outlier_overview_C[outlier_sample_C] += 1
        else:
            outlier_overview_C[outlier_sample_C] = 1
    for i in outlier_index_D:
        outlier_sample_D = "D_{}".format(i+1)
        if outlier_sample_D in outlier_overview_D:
            outlier_overview_D[outlier_sample_D] += 1
        else:
            outlier_overview_D[outlier_sample_D] = 1

## Percentage calculateion ##
outlier_overview_percentage = {}
for key in outlier_overview_C:
    outlier_overview_percentage[key] = round(outlier_overview_C[key]/len(init_Name_list)*100,2)
for key in outlier_overview_D:
    outlier_overview_percentage[key] = round(outlier_overview_D[key]/len(init_Name_list)*100,2)   
## Save outliers to table ##
with open(os.path.join(Folder2,file5_outliers),'w+') as out:
    out.write("Sample;outliers;percentage\n")
    for key in outlier_overview_C:
        out.write("{};{};{}\n".format(key,outlier_overview_C[key],outlier_overview_percentage[key]))
    for key in outlier_overview_D:
        out.write("{};{};{}\n".format(key,outlier_overview_D[key],outlier_overview_percentage[key]))
out.close()

# Exclusion of samples based on percentage of outliers within the sample #
Sample_exclusion_list = []
for key in outlier_overview_percentage:
    if outlier_overview_percentage[key] > 20:
        Sample_exclusion_list.append(key)

# Remove excluded samples from header list #
Header_list_without_outlier_samples = []
for key in Header_list:
    if key not in Sample_exclusion_list:
        Header_list_without_outlier_samples.append(key)
    else:
        pass

## Save sample lookup file ##
# remove excluded samples from lookup data frame #
df_lookup_clean = df_sample_lookup[df_sample_lookup['Sample number'].isin(Header_list_without_outlier_samples)]
# Save dataframe to file #
df_lookup_clean.to_csv(os.path.join(Folder3,file6_look_up),index=False,sep=";")

## Save transposed raw data without outlier samples ##
# Remove excluded samples from raw data frame #
df_raw_QC_C_D_without_outlier_samples = df_raw_QC_C_D[['Name']+Header_list_without_outlier_samples]
# Save dataframe to file #
df_raw_QC_C_D_without_outlier_samples.to_csv(os.path.join(Folder2,file7_sample_file),index=False,sep=";")
