# MacAulayLab SAH Metabolomics #
The work and scripts are done by the MacAulay Lab. \
All programs used are free and open-source. In the interest of open science and reproducibility, all data and source code used in our research is provided here. \
Feel free to copy and use code, but please cite: \
(coming soon) \
Remember rewrite file_names and folder_names suitable for your pipeline.

## The Metabolomic Analysis follows these steps:

## Data preprocessing ##
### filtering out samples with very high amount of outliers (20%) ###
1.0.1 - Data preprocessing - clean for sample outliers.py

## sort data, normalize, remove outliers and save all in seperate files ##
2.1.1 - Data preprocessing - Data analysis.py

## Create Abundance tables ##
Abundance tables are used in 9.1.1 as well \
3.1.1 - Control and SAH group - Abudance table generator.py \
3.2.1 - Control and SAH group - Abundance piechart.py

## Enrichment (piechart) analysis ##
4.1.1 - Control group - Enrichment data generator.py
4.1.2 - Control group - Enrichment plots.py

## PCA plots for control group (age and sex) ##
5.1.1 - Control group - Subset data for PCA age and sex.py
5.2.1 - Control group - PCA sex plot.py
5.2.2 - Control group - PCA age plot.py
5.3.1 - Control group - PCA Sex Supplementary plots for each groups.py
5.3.2 - Control group - PCA Age Supplementary plots for each groups.py

## Abundance of lipid group as a function of age ##
6.1.1 - Control group - Generate data for age function plots.py
6.2.1 - Control group - Plot age as function of groups.py
6.3.1 - Control group - Plot age as function of individual groups (supp).py

## PCA plots for SAH group (age and sex) ##
7.1.1 - SAH group - Subset data for PCA age and sex.py
7.2.1 - SAH group - PCA sex plot.py
7.2.2 - SAH group - PCA age plot.py
7.3.1 - SAH group - PCA Sex Supplementary plots for each groups.py
7.3.2 - SAH group - PCA Age Supplementary plots for each groups.py

## PCA for control and SAH groups ##
8.1.1 - Control and SAH group - PCA plot.py
8.2.1 - Control and SAH - PCA plots - Individual groups.py

## Abundance barplot for lipid groups ##
9.1.1 -  Control and SAH group - Bar plot - Group abunance.py

## Volcano plot ##
10.1.1 Generate data for Volcano plot.py
10.1.2 Volcano plot grouped_v2.R
 
## Individual lipid group analysis and barplots ##
11.1.1 - Control and SAH - Barplots -Individual groups analysis.py

## Create supplementary tables ##
12.1.1 - Supplementary tables.py
