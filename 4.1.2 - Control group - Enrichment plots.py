# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:03:04 2023

@author: dcs839
"""

### Enrichment plots ###

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set(font_scale=3)

## functions ##

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}%\n({v:d})'.format(pct, v=val)
    return my_format

font_size = 24
## Folders ##

Folder1 = "Data/Enrichment data/Control group C"
Folder2 = "Results/Enrichement Analysis/Control group C"
Folder3 = "Data/Meta data"

os.makedirs(Folder2,exist_ok=True)
    
## Files ##

File1 = "Enrichement_data_all_group_C.csv"


File3 = "Enrichment_plot_all_percent_exploded.png"

## Load color scheme and create color mapping ##
Color_file = "Color_scheme_groups.csv"
df_color = pd.read_csv(os.path.join(Folder3,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

## Load data ##

# All metabolite groups ##
df_all = pd.read_csv(os.path.join(Folder1,File1),sep=";")

## Create plot data ##
# Variables #
data_all = df_all['Count']
labels_all = df_all['Groups']

## Create color palettes for plots #
color_all = labels_all.to_frame().replace({"Groups": Color_mapping})['Groups'].tolist()

## Set exploded set ##

explode_set_all = [0.15]*len(color_all)

# plot data #
print("Creating enrichment plot for all Compounds")
plt.figure(figsize=(20,20))
plt.pie(data_all, labels = labels_all,
        colors = color_all,
        explode=explode_set_all,
        autopct=autopct_format(data_all),
        textprops={'fontsize': font_size},
        wedgeprops = {"edgecolor":"black",'linewidth': 1.2,"alpha": 0.65},
        counterclock=False,
        startangle=90,
        pctdistance=1.2,
        labeldistance=1.3)
print("Saving plot...")
plt.savefig(os.path.join(Folder2,File3),dpi=600,bbox_inches='tight')
plt.show()
print("Done.")