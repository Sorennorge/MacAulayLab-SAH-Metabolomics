# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:15:29 2022

@author: dcs839
"""

import os
import pandas as pd
import numpy as np

# Folders #

Folder1 = "Data/Normalized data"
Folder2 = "Data/Lookup data"
Folder3 = "Data/Meta data"

Folder4 = "Data/Meta data/Control group C"
os.makedirs(Folder4,exist_ok=True)

Folder5 = "Data/PCA data/Sex/Control"
os.makedirs(Folder5,exist_ok=True)
Folder6 = "Data/PCA data/Age/Control"
os.makedirs(Folder6,exist_ok=True)


## Files ##

File1 = "Group C Normalized data.xlsx"
File2 = "Sample_lookup_table.csv"
File3 = "C_and_D_ages_and_sex_and_hypertension.csv"

# Output #
File4 = "Metadata_control_group_C_overview.csv"

PCA_sex_data = "PCA_data_sex.csv"
PCA_sex_targets = "PCA_targets_sex.csv"
PCA_age_data = "PCA_data_age.csv"
PCA_age_targets = "PCA_targets_age.csv"

## Read raw data ##

# Read data #
df_normalized = pd.read_excel(os.path.join(Folder1,File1)).rename(columns=({"Unnamed: 0":"Samples"})).set_index("Samples")
df_normalized_T = df_normalized.T


# Create lists of samples 
Group_C_list = df_normalized_T.columns.values.tolist()

## Load sample lookup ##
df_sample_lookup = pd.read_csv(os.path.join(Folder2,File2),sep=";")
# Convert into dict #
df_sample_lookup_dict = df_sample_lookup.set_index('ID')['Sample number'].to_dict()

## Load metadata ##
df_meta_data = pd.read_csv(os.path.join(Folder3,File3),sep=";")
# Add new sampleID #
df_meta_data['Sample ID'] = df_meta_data['Sample number'].map(df_sample_lookup_dict)
# Create metadata mapping dicts
Sex_mapping = dict(df_meta_data[['Sample ID', 'Sex']].values)
Age_mapping = dict(df_meta_data[['Sample ID', 'Age']].values)

## Create meta data overview as dataframe (for PCA targets) ##

Meta_data_overview = df_sample_lookup[df_sample_lookup['Sample number'].isin(Group_C_list)].copy().reset_index(drop=True)
# Add sex to the overview (and PCA target) #
Meta_data_overview['Sex'] = Meta_data_overview['Sample number'].map(Sex_mapping)
Meta_data_overview['Sex targets'] = np.where(Meta_data_overview['Sex'] == "Kvinde", 0, 1)
# Add Age to the overview (and PCA target) #
Meta_data_overview['Age'] = Meta_data_overview['Sample number'].map(Age_mapping)
Meta_data_overview['Age targets'] = np.where(Meta_data_overview['Age'] <= 60, 1, 0)
Meta_data_overview = Meta_data_overview.set_index('Sample number')

# Save overview data #
Meta_data_overview.to_csv(os.path.join(Folder4,File4),sep=";")

## Save normalized PCA data ##
# Sex PCA #
df_normalized_T.to_csv(os.path.join(Folder5,PCA_sex_data),index=False,header=False,sep=";")
Meta_data_overview[['Sex','Sex targets']].to_csv(os.path.join(Folder5,PCA_sex_targets),sep=";")
# Age PCA #
df_normalized_T.to_csv(os.path.join(Folder6,PCA_age_data),index=False,header=False,sep=";")
Meta_data_overview[['Age','Age targets']].to_csv(os.path.join(Folder6,PCA_age_targets),sep=";")