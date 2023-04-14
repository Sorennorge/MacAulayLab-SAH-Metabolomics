# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 09:24:23 2023

@author: dcs839
"""

### Bar chart group C and D ###

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy
from scipy import stats
sns.set(font_scale=2)
sns.set_style("white")

## Folders ##
Folder1 = "Data/Enrichment data/Control group C & D Weighted"
Folder2 = "Results/Abundance/Group barplot"
os.makedirs(Folder2,exist_ok=True)

## Files ##
File1 = "Group C - Weighted data without outliers.xlsx"
File2 = "Group D - Weighted data without outliers.xlsx"
bar_file = "Abundance bar plot.png"
overview_file = "Bar chart overview.xlsx"

## load data ##

df_c = pd.read_excel(os.path.join(Folder1,File1))
#df_c = df_c[['Groups','mean']]
df_c = df_c.drop(['Mean'], axis=1)
#df_c['Group'] = "Control"

    
df_d = pd.read_excel(os.path.join(Folder1,File2))
#df_d = df_d[['Groups','mean']]
df_d = df_d.drop(['Mean'], axis=1)
#df_d['Group'] = "SAH"

stacked_d = df_d.set_index('Groups').stack().reset_index()
stacked_d = stacked_d.drop(['level_1'], axis=1).rename(columns={0:"Values"})
stacked_d['State'] = "SAH"

stacked_c = df_c.set_index('Groups').stack().reset_index()
stacked_c = stacked_c.drop(['level_1'], axis=1).rename(columns={0:"Values"})
stacked_c['State'] = "Control"
df_data = pd.concat([stacked_c,stacked_d],ignore_index=True)
#sns.barplot(data=df_data, x="Groups", y="mean", hue="Group")

plt.figure(figsize=(14,8))
p1 = sns.barplot(data=df_data, x="Groups", y="Values",
                 hue="State",palette = ['grey','darkred'],estimator=np.mean,ci = 68) #bootstrap ci 68% is SEM
plt.xticks(rotation=90,ha='right',rotation_mode='anchor')
plt.ylabel('Lipid abundance')
plt.xlabel('')
plt.title("Lipid group abundance")
p1.legend_.set_title(None)
plt.ylim([0,90])
sns.despine(top=True, right=True, left=False, bottom=True)
p1.axhline(y=0.0,color='black',linewidth=2)
plt.savefig(os.path.join(Folder2,bar_file),dpi=600,bbox_inches='tight')
plt.show()


df_d_T = df_d.set_index('Groups').T.reset_index(drop=True)
df_c_T = df_c.set_index('Groups').T.reset_index(drop=True)
df_c_T['Group'] = "Control"
df_d_T['Group'] = "SAH"
df_data_combined = pd.concat([df_c_T,df_d_T],axis=0,ignore_index=True)

col_names = df_data_combined.columns.values.tolist()[:-1]

control_df = df_data_combined[df_data_combined['Group'] == 'Control']
sah_df = df_data_combined[df_data_combined['Group'] == 'SAH']

def convert_pvalue_to_asterisks(pvalue):
    if pvalue <= 0.0001:
        return "****"
    elif pvalue <= 0.001:
        return "***"
    elif pvalue <= 0.01:
        return "**"
    elif pvalue <= 0.05:
        return "*"
    return "ns"

P_value_dict = {}
mean_C_dict = {}
SEM_C_dict = {}
mean_D_dict = {}
SEM_D_dict = {}
P_value_dict_sig = {}
for metabolite_group in col_names:
    #print(metabolite_group)
    control_values = np.array(control_df[metabolite_group].to_list(),dtype=float)
    sah_values = np.array(sah_df[metabolite_group].to_list(),dtype=float)
    stat, pvalue = scipy.stats.ttest_ind(sah_values,control_values,equal_var = False)
    mean_control = np.mean(control_values)
    mean_SAH = np.mean(sah_values)
    SEM_control = stats.sem(control_values,ddof=1)
    SEM_SAH = stats.sem(sah_values,ddof=1)
    #print(stat,pvalue)
    P_value_dict[metabolite_group] = pvalue
    P_value_dict_sig[metabolite_group] = convert_pvalue_to_asterisks(pvalue)
    mean_C_dict[metabolite_group] = mean_control
    SEM_C_dict[metabolite_group] = SEM_control
    mean_D_dict[metabolite_group] = mean_SAH
    SEM_D_dict[metabolite_group] = SEM_SAH

df_overview = df_c[['Groups']].copy()
df_overview['Control mean'] = df_overview.Groups.map(mean_C_dict)
df_overview['Control SEM'] = df_overview.Groups.map(SEM_C_dict)
df_overview['SAH mean'] = df_overview.Groups.map(mean_D_dict)
df_overview['SAH SEM'] = df_overview.Groups.map(SEM_D_dict)
df_overview['Pvalue'] = df_overview.Groups.map(P_value_dict)
df_overview['Significance'] = df_overview.Groups.map(P_value_dict_sig)

df_overview.to_excel(os.path.join(Folder2,overview_file),index=False)