# PopGenAnalysis

## Overview:

This repository contains the pipeline script for Population Genetics Analysis built using SnakeMake for the GenomeIndia Project. The types of analysis done by this pipeline is:
  
  1. ADMIXTURE
  2. Principal Component Analysis (PCA)
  3. Integrated Haplotype Score (iHS)
  4. Cross-Population Extended Haplotype Homozygosity Test (XP-EHH)
  5. TreeMIX
  
The pipeline is divided into four sections:
  
  #### 1. Quality Control
        
   a. Removing Multiallelic Variants
        
   b. Removing Duplicates
        
   c. Variant Missingness Check
        
   d. Individual Missingness Check
        
   e. Minor Allele Frequency (MAF) Check
        
   f. Hardy-Weinberg Equilibrium Check
        
   g. Heterozygosity Check
        
  #### 2. Finding Common Variants
  
  #### 3. Phasing
  
  #### 4. Analysis

## Required packages:
  1. [Conda](https://docs.conda.io/en/latest/miniconda.html)
  2. [R](https://www.r-project.org/)
  3. [Mamba](https://github.com/mamba-org/mamba)
  
    conda activate base
    conda install mamba
    
  4. [Snakemake](https://snakemake.readthedocs.io/en/stable/)
   
    conda create -n snakemake
    conda activate snakemake
    conda install snakemake
--------------------------------------------------------------------------------------------------------------------------------------------------------
## Running in a local computer:
    
    cd PopGenAnalysis
    snakemake --use-cores 1 --use-conda
    
## Running in a slurm cluster:
  
    cd PopGenAnalysis
    snakemake --profile slurm --use-conda

--------------------------------------------------------------------------------------------------------------------------------------------------------
#### Version 1.2.2

  All the analysis are now togglable to On/Off from the config file.

#### Version 1.2.1

  1. Indexing of a vcf file was done every time a rule was invoked. This led to problems when running in clusters since multiple nodes are re-writing the index files which cause some the rules in some nodes to not recognize the index file. New rules for indexing added.
  2. Location of the 'Filteredpop.csv' file was changed in multiple rules to the new location.

#### Version 1.2.0

  1. iHS script functionality changed. Now iHS can be done on any population in the __Pop/SuperPop__ column for __own__ file. Additional rules added for this are:
      * rule *iHS_Merge*
      * rule *iHS_PopSplit*
      * rule *iHS_PopChromSplit*
  2. Made modifications in the iHS rules such that the results of iHS is neatly arranged in folder. The affected rules are:
      * rule *iHS_Preparation*
      * rule *iHS_Phasing*
      * rule *iHS_Merge*
      * rule *iHS_MapCreation*
      * rule *iHS*
      * rule *iHS_Normalization*

#### Version 1.1.1

  The new population list csv file containing samples which passed Quality Checks is now created by a new rule *CreatingNewPopFile*.
  With this, running iHS does not depend on the rule *SortPopulations* since the population list file was created under this rule before.

#### Version 1.1.0 : QC Steps can be Run/Not Run

  Quality Check rules can be toggles **ON/OFF** by giving the input as a **Value/False** respectively in the config file.
  This includes-

  * rule *VariantMissingness* (geno)
  * rule *IndividualMissingness* (mind)
  * rule *MinorAlleleFrequency* (maf)
  * rule *HardyWeinbergEquilibriumCheck* (hwe)
  * rule *HeterozygosityCheck* (heterozygosity)
