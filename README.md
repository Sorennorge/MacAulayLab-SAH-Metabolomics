# MacAulayLab-SAH-Metabolomics
The work and scripts are done by the MacAulay Lab.
All programs used are free and open-source. In the interest of open science and reproducibility, all data and source code used in our research is provided here.
Feel free to copy and use code, but please cite:
(coming soon)
Remember rewrite file_names and folder_names suitable for your pipeline.
Note: Many of the tables output have converted dot to comma for danish excel annotation

## The RNAseq and Analysis follows these steps:
## Raw data analysis - Library Build, Mapping and Quantification ##
The analysis uses RNA STAR for mapping and RSEM for TPM quantification.
### RNA-STAR and RSEM Library build and indexing ###

1.1.1 - RNA_STAR_Indexing.sh \
1.2.1 - RSEM_Indexing.sh

### RNA-STAR Mapping and RSEM quantification ###

1.1.2 -RNA_STAR_RNAseq2.sh \
1.2.2 - RSEM_RNAseq2.sh

### Generate count table ###

2.1.1 - Generate count table from raw data.py 

### Generate overview table and overview table of transport ###
Requirements:
Metadata table of transport (example in script). 

3.1.1 - Overview table of light and dark phase
