# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 10:28:47 2023

@author: dcs839
"""
#column_names = df.columns.values.tolist()
### Metabolomics data analysis ###

## Libraries ##

import os
import numpy as np
import pandas as pd
import math
import statsmodels.stats.multitest as smt
from scipy.stats import gmean
from scipy.stats import ttest_ind
from OUTLIERS import smirnov_grubbs as grubbs

## Functions ##

def log2FC_func(A,B):
    FC = B/A
    log2FC = round(math.log(FC,2),4)
    return log2FC

## Folders ##

Folder0= "Data/Meta data"
Folder1 = "Data/Data cleaning"
Folder2 = "Data/Raw data analysis"
os.makedirs(Folder2, exist_ok=True)
Folder3 = "Data/PCA data/Raw"
os.makedirs(Folder3, exist_ok=True)
Folder4 = "Data/Data analysis"
os.makedirs(Folder4,exist_ok=True)
Folder5 = "Data/Normalized data"
os.makedirs(Folder5,exist_ok=True)

## Files ##

File0 = "Meta_data_groups.xlsx"
File1 = "raw_data_C_and_D_transposed.csv"
File2 = "Raw_data_DP.xlsx"
File3 = "PCA_data.xlsx"
File4 = "PCA_targets.xlsx"
File5 = "Outlier overview.xlsx"
File6 = "DP overview.xlsx"
File7 = "Data analysis overview.xlsx"
File8 = "Data analysis overview V2.xlsx"
# Normalized #
File9 = "Normalized data for group C and D.xlsx"
File10 = "Group C Normalized data.xlsx"
File11 = "Group D Normalized data.xlsx"
# Normalized without outliers 
File12 = "Normalized data for group C and D without outliers.xlsx"
File13 = "Group C Normalized data without outliers.xlsx"
File14 = "Group D Normalized data without outliers.xlsx"

### load data ###

# Meta data #

df_groups = pd.read_excel(os.path.join(Folder0,File0))
df_groups_LOI = df_groups.loc[df_groups['LOI'] == "Yes"]
LOI_metabolite_list = df_groups_LOI['Compounds'].tolist()

df = pd.read_csv(os.path.join(Folder1,File1),sep=";")

Header = df.columns.values.tolist()
QC_list = list(filter(lambda x: x.startswith('QC_'), Header))
Group_C_list = list(filter(lambda x: x.startswith("C_"), Header))
Group_D_list = list(filter(lambda x: x.startswith("D_"), Header))

# Modulate data for dict conversion #

df = df.set_index('Name')
Info_dict_QC = dict(zip(df.index, df[QC_list].values))
Info_dict_C = dict(zip(df.index, df[Group_C_list].values))
Info_dict_D = dict(zip(df.index, df[Group_D_list].values))

Compounds = df.index.tolist()

## Calculate raw descriptive power (DP) ##
Raw_DP_dict = {}
Raw_Significant_metabolite_list = []
# Find DP of raw data and list of significant Compounds -> DP > 2.5 #
for key in Compounds:
    Group_C_and_D_concatenated = np.concatenate((Info_dict_C[key], Info_dict_D[key]), axis=None)
    Raw_DP = np.std(Group_C_and_D_concatenated,ddof=1)/np.std(Info_dict_QC[key],ddof=1)
    Raw_DP_dict[key] = Raw_DP
    if Raw_DP > 2.5:
        if key in LOI_metabolite_list: #NEW!!!
            Raw_Significant_metabolite_list.append(key)
        else:
            pass
        #Raw_Significant_metabolite_list.append(key)
    else:
        pass
    
# create dataframe from DP values (raw) #
raw_df_DP = pd.DataFrame({'Compounds': list(Raw_DP_dict.keys()),'DP':list(Raw_DP_dict.values())})

raw_df_DP['Significance'] = np.where(raw_df_DP['DP'] >= 2.5, "Yes", "No")

if os.path.isfile(os.path.join(Folder2,File2)):
    pass
else:
    raw_df_DP.to_excel(os.path.join(Folder2,File2),sheet_name='Raw DP calc',header=True,index=False)

## Create PCA plot tables ##

df_without_QC = df[Group_C_list+Group_D_list]
# transpose data for correct PCA annotation #
PCA_df_T = df_without_QC.T
# Only include Compounds with DP > 2.5 #
PCA_df = PCA_df_T.loc[:, PCA_df_T.columns.isin(Raw_Significant_metabolite_list)]

PCA_targets = pd.DataFrame(index=PCA_df.index.copy())
PCA_targets['Samples'] = PCA_targets.index
#PCA_targets.loc[PCA_targets['Samples'].str.startswith('QC_'), 'Target'] = 'QC'
PCA_targets.loc[PCA_targets['Samples'].str.startswith('C_'), 'Target'] = 'Group C'
PCA_targets.loc[PCA_targets['Samples'].str.startswith('D_'), 'Target'] = 'Group D'

if os.path.isfile(os.path.join(Folder3,File3)):
    pass
else:
    PCA_df.to_excel(os.path.join(Folder3,File3),sheet_name='PCA data',header=False,index=False)

if os.path.isfile(os.path.join(Folder3,File4)):
    pass
else:
    PCA_targets.to_excel(os.path.join(Folder3,File4),sheet_name='PCA Targets',header=False,index=False)

## For PCA plot ##
# Run script 3.1.2 - PCA plots for raw data #

## Normalize data for Compounds DP > 2.5 ##
# Reduce dataframe to only Compounds with DP > 2.5 #
df_significant = df[df.index.isin(Raw_Significant_metabolite_list)]
# Calculate geomean for Compounds
df_geomean = pd.DataFrame(index=df_significant.index.copy())
df_geomean['geomean'] = gmean(df_significant.iloc[:, df_significant.columns.get_indexer(QC_list)], axis=1)

# Normalize data based on geomean #
DF_normalized = df_significant.loc[:,Group_C_list+Group_D_list].div(df_geomean["geomean"], axis=0)
## Remove outliers
DF_normalized_without_outliers =  DF_normalized.copy()

## Save normalized data to files ##

DF_normalized_all_T = DF_normalized.reset_index().rename(columns=({"Name":"Samples"})).set_index('Samples').T
DF_normalized_all_T.to_excel(os.path.join(Folder5,File9),sheet_name='Normalized data',index=False)

# Divide normalized data into two seperate files #

DF_normalized_all_T_C = DF_normalized_all_T.T[Group_C_list].T
DF_normalized_all_T_D = DF_normalized_all_T.T[Group_D_list].T

DF_normalized_all_T_C.to_excel(os.path.join(Folder5,File10),sheet_name='Normalized data C')
DF_normalized_all_T_D.to_excel(os.path.join(Folder5,File11),sheet_name='Normalized data C')


index_list = DF_normalized.index
column_list = np.array(DF_normalized.columns.tolist())
counter = 0
for i in DF_normalized.index:
    # Get array for control (C) and Disease (D)
    numpy_array_C = np.array(DF_normalized.loc[i,Group_C_list])
    numpy_array_D = np.array(DF_normalized.loc[i,Group_D_list])
    # Get outlier index #
    outlier_index_C =  grubbs.two_sided_test_indices(numpy_array_C, alpha=.05)
    outlier_index_C = np.array(outlier_index_C,dtype=int)
    outlier_index_D =  grubbs.two_sided_test_indices(numpy_array_D, alpha=.05)
    outlier_index_D = np.array(outlier_index_D,dtype=int)
    outlier_index_D = (outlier_index_D + 11)
    all_entries = np.concatenate((outlier_index_C,outlier_index_D), axis=0)
    if len(all_entries) > 0:
        #print(all_entries)
        cols = column_list[all_entries].tolist()
        #print(cols)
        for loc_col in cols:
            DF_normalized_without_outliers.at[i,loc_col] = np.nan
        #print(i)


# Transpose normalized data #
# Here without outliers #!!! 
DF_normalized_T = DF_normalized_without_outliers.T.copy()
DF_normalized_T = DF_normalized_T.reset_index().rename(columns=({'index':"Sample number"}))
# Save normalized - transposed data to file #
DF_normalized_T.to_excel(os.path.join(Folder5,File12),sheet_name='Normalized data',index=False)

## Divide normalized data into two seperate files ##

DF_normalized_T_C = DF_normalized_T.set_index('Sample number').T[Group_C_list].T
DF_normalized_T_D = DF_normalized_T.set_index('Sample number').T[Group_D_list].T

DF_normalized_T_C.to_excel(os.path.join(Folder5,File13),sheet_name='Normalized data C')
DF_normalized_T_D.to_excel(os.path.join(Folder5,File14),sheet_name='Normalized data C')
                          

## Create overview table - without outliers ##

df_overview = DF_normalized_without_outliers.reset_index()[['Name']].copy()
df_overview = df_overview.set_index('Name')
## Add Mean and SD to overview ##
# Group C #
df_overview["Group C Mean"] = DF_normalized_without_outliers[Group_C_list].mean(axis=1)
df_overview["Group C SD"] = DF_normalized_without_outliers[Group_C_list].std(axis=1,ddof=1)
# Group D #
df_overview["Group D Mean"] = DF_normalized_without_outliers[Group_D_list].mean(axis=1)
df_overview["Group D SD"] = DF_normalized_without_outliers[Group_D_list].std(axis=1,ddof=1)

# Add Log2FC #
df_overview["Log2FC"] = np.log2(df_overview["Group D Mean"]/df_overview["Group C Mean"])
## add p-value of welch t test #
df_overview['Pvalue'] = ttest_ind(DF_normalized_without_outliers[Group_C_list], DF_normalized_without_outliers[Group_D_list],nan_policy='omit',equal_var = False, axis=1)[1]
df_overview['Padj'] = smt.fdrcorrection(df_overview['Pvalue'],alpha=0.05,method="indep")[1]

## Save overview table to file ###
df_overview = df_overview.reset_index().rename(columns={'Name':"Compounds"})
df_overview.to_excel(os.path.join(Folder4,File7),sheet_name='Overview',header=True,index=False)