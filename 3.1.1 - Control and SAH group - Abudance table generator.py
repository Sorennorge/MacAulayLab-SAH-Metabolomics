# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 11:33:18 2023

@author: dcs839
"""

### Create weigted data for enrichment analysis ###

## Need normalized data ## -> coming from a later script ##

import os
import pandas as pd


## Folders ##

Folder1 = "Data/Meta data"
Folder2 = "Data/Normalized data"
Folder3 = "Data/Enrichment data/Control group C"
Folder4 = "Data/Enrichment data/Control group C & D Weighted"
os.makedirs(Folder4,exist_ok=True)
## Files ##

File1 = "Meta_data_groups.xlsx"
File2 = "Group C Normalized data.xlsx"
File3 = "Group D Normalized data.xlsx"
File4 = "Group C Normalized data without outliers.xlsx"
File5 = "Group D Normalized data without outliers.xlsx"


File_out_1 = "Group C - Weighted data.xlsx"
File_out_2 = "Group D - Weighted data.xlsx"

File_out_3 = "Group C - Weighted data without outliers.xlsx"
File_out_4 = "Group D - Weighted data without outliers.xlsx"


## Load color scheme and create color mapping ##
Color_file = "Color_scheme_groups.csv"
df_color = pd.read_csv(os.path.join(Folder1,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

## Load meta data ##

df_meta = pd.read_excel(os.path.join(Folder1,File1))
df_meta = df_meta.loc[df_meta['LOI'] == "Yes"]
df_meta_mapping = df_meta[['Compounds','Groups']].set_index('Compounds')

### With outliers ###

## Load data ##

# Group C #
df_normalized_C = pd.read_excel(os.path.join(Folder2,File2)).rename(columns={"Unnamed: 0":"Samples"}).set_index('Samples')
#df_normalized_C = pd.read_excel(os.path.join(Folder2,File2)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_C_T = df_normalized_C.T

# Group D #
df_normalized_D = pd.read_excel(os.path.join(Folder2,File3)).rename(columns={"Unnamed: 0":"Samples"}).set_index('Samples')
#df_normalized_D = pd.read_excel(os.path.join(Folder2,File3)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_D_T = df_normalized_D.T
## Modify data ##
# Group C #
df_C_grouped = pd.concat([df_normalized_C_T,df_meta_mapping],join="inner",axis=1)
df_C_sum = df_C_grouped.groupby('Groups').sum()

# Group D #

df_D_grouped = pd.concat([df_normalized_D_T,df_meta_mapping],join="inner",axis=1)
df_D_sum = df_D_grouped.groupby('Groups').sum()

## Sum data ##

# Group C #
df_C_sum['Mean'] = df_C_sum.mean(axis=1)
df_C_sum = df_C_sum.reset_index()

# Group D #
df_D_sum['Mean'] = df_D_sum.mean(axis=1)
df_D_sum = df_D_sum.reset_index()

### C Group ###
df_C_sum_sorted_sum = df_C_sum.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_C = df_C_sum_sorted_sum.index.tolist()
pop_index_C = df_C_sum_sorted_sum.index[df_C_sum_sorted_sum['Groups']=='Small group collection'].tolist()[0]
idx_C.pop(pop_index_C)
df_C_sum_sorted_sum = df_C_sum_sorted_sum.reindex(idx_C+[pop_index_C]).reset_index(drop=True)
df_C_sum_sorted_sum.to_excel(os.path.join(Folder4,File_out_1),index=False)

### D Group ###
df_D_sum_sorted_sum = df_D_sum.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_D = df_D_sum_sorted_sum.index.tolist()
pop_index_D = df_D_sum_sorted_sum.index[df_D_sum_sorted_sum['Groups']=='Small group collection'].tolist()[0]
idx_D.pop(pop_index_D)
df_D_sum_sorted_sum = df_D_sum_sorted_sum.reindex(idx_D+[pop_index_D]).reset_index(drop=True)
df_D_sum_sorted_sum.to_excel(os.path.join(Folder4,File_out_2),index=False)

### Without outliers ###

## Load data ##

# Group C #
df_normalized_C_wo = pd.read_excel(os.path.join(Folder2,File4)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_C_T_wo = df_normalized_C_wo.T

# Group D #
df_normalized_D_wo = pd.read_excel(os.path.join(Folder2,File5)).rename(columns={"Sample number":"Samples"}).set_index('Samples')
df_normalized_D_T_wo = df_normalized_D_wo.T
## Modify data ##
# Group C #
df_C_grouped_wo = pd.concat([df_normalized_C_T_wo,df_meta_mapping],join="inner",axis=1)
df_C_sum_wo = df_C_grouped_wo.groupby('Groups').sum()

# Group D #

df_D_grouped_wo = pd.concat([df_normalized_D_T_wo,df_meta_mapping],join="inner",axis=1)
df_D_sum_wo = df_D_grouped_wo.groupby('Groups').sum()

## Sum data ##

# Group C #
df_C_sum_wo['Mean'] = df_C_sum_wo.mean(axis=1)
df_C_sum_wo = df_C_sum_wo.reset_index()

# Group D #
df_D_sum_wo['Mean'] = df_D_sum_wo.mean(axis=1)
df_D_sum_wo = df_D_sum_wo.reset_index()

### C Group ###
df_C_sum_sorted_sum_wo = df_C_sum_wo.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_C_wo = df_C_sum_sorted_sum_wo.index.tolist()
pop_index_C_wo = df_C_sum_sorted_sum_wo.index[df_C_sum_sorted_sum_wo['Groups']=='Small group collection'].tolist()[0]
idx_C_wo.pop(pop_index_C_wo)
df_C_sum_sorted_sum_wo = df_C_sum_sorted_sum_wo.reindex(idx_C_wo+[pop_index_C_wo]).reset_index(drop=True)
df_C_sum_sorted_sum_wo.to_excel(os.path.join(Folder4,File_out_3),index=False)

### D Group ###
df_D_sum_sorted_sum_wo = df_D_sum_wo.sort_values(by=['Mean'],ascending=False,ignore_index=True)
idx_D_wo = df_D_sum_sorted_sum_wo.index.tolist()
pop_index_D_wo = df_D_sum_sorted_sum_wo.index[df_D_sum_sorted_sum_wo['Groups']=='Small group collection'].tolist()[0]
idx_D_wo.pop(pop_index_D_wo)
df_D_sum_sorted_sum_wo = df_D_sum_sorted_sum_wo.reindex(idx_D_wo+[pop_index_D_wo]).reset_index(drop=True)
df_D_sum_sorted_sum_wo.to_excel(os.path.join(Folder4,File_out_4),index=False)
