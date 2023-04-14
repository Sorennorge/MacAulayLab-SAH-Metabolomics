# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:43:36 2023

@author: dcs839
"""

### Abundance piecharts ###

## Libraries ##

import os
import pandas as pd
import matplotlib.pyplot as plt

font_size = 24

## Function ##
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = pct*total/100.0
        return '{:.1f}%\n({v:.2f})'.format(pct, v=val)
    return my_format

## Folders ##

Folder_0 = "Data/Meta data"

Folder_1 = "Data/Enrichment data/Control group C & D Weighted"
Folder_2 = "Results/Enrichement Analysis/Abundance"
os.makedirs(Folder_2,exist_ok=True)

Color_file = "Color_scheme_groups.csv"

## Files ##

File_1 = "Group C - Weighted data.xlsx"
File_2 = "Group D - Weighted data.xlsx"

File_out_1 = "Abundance piechart - group C.png"
File_out_2 = "Abundance piechart - group D.png"

## Load data ##

## Load color scheme and create color mapping ##

df_color = pd.read_csv(os.path.join(Folder_0,Color_file),sep=";")
Color_mapping = dict(df_color[['Groups', 'Colors']].values)

# Data #
df_C = pd.read_excel(os.path.join(Folder_1,File_1))
df_D = pd.read_excel(os.path.join(Folder_1,File_2))

## Create variables for plots ##

data_all_C = df_C['Mean']
labels_all_C = df_C['Groups']

data_all_D = df_D['Mean']
labels_all_D = df_D['Groups']

## Create color palettes for plots #
color_all_C = labels_all_C.to_frame().replace({"Groups": Color_mapping})['Groups'].tolist()
color_all_D = labels_all_D.to_frame().replace({"Groups": Color_mapping})['Groups'].tolist()

explode_set_all_C = [0.15]*len(color_all_C)
explode_set_all_D = [0.15]*len(color_all_D)


print("Creating enrichment plot for all Compounds - Group C")
plt.figure(figsize=(20,20))
plt.pie(data_all_C, labels = labels_all_C,
        colors = color_all_C,
        explode=explode_set_all_C,
        autopct=autopct_format(data_all_C),
        textprops={'fontsize': font_size},
        wedgeprops = {"edgecolor":"black",'linewidth': 1.2,"alpha": 0.65},
        counterclock=False,
        startangle=90,
        pctdistance=1.2,
        labeldistance=1.3)
print("Saving plot...")
plt.savefig(os.path.join(Folder_2,File_out_1),dpi=600,bbox_inches='tight')
plt.show()
print("Done.")

print("Creating enrichment plot for all Compounds - Group D")
plt.figure(figsize=(20,20))
plt.pie(data_all_D, labels = labels_all_D,
        colors = color_all_D,
        explode=explode_set_all_D,
        autopct=autopct_format(data_all_D),
        textprops={'fontsize': font_size},
        wedgeprops = {"edgecolor":"black",'linewidth': 1.2,"alpha": 0.65},
        counterclock=False,
        startangle=90,
        pctdistance=1.2,
        labeldistance=1.3)
print("Saving plot...")
plt.savefig(os.path.join(Folder_2,File_out_2),dpi=600,bbox_inches='tight')
plt.show()
print("Done.")