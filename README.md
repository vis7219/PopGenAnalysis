# PopGenAnalysis

## Overview:

This repository contains the pipeline script for Population Genetics Analysis built using SnakeMake for the GenomeIndia Project. The types of analysis done by this pipeline is:  
  1. ADMIXTURE
  2. Principal Component Analysis (PCA)
  3. Integrated Haplotype Score (iHS)
  4. Cross-Population Extended Haplotype Homozygosity Test (XP-EHH)
  5. TreeMIX
  
The pipeline is divided into four sections:  
  1. Quality Check
  2. Finding Common Variants
  3. Phasing
  4. Analysis
  
   ![Pipeline Flowchart](https://user-images.githubusercontent.com/52356143/187366638-ec7ec1fb-ff6b-454f-bbaf-847d2a9990e8.png)

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
    snakemake --cores 1 --use-conda
__--cores__ is the number of threads that the pipeline will use.  

The *--cores* option in the command line and the *threads* option in the config.yaml file work together.  

* If the threads provided in *--cores* is lesser than what is provided in *threads*, then SnakeMake will consider *--cores* input.  
* If threads provided in *--cores* is more than what is provided by *threads*, SnakeMake will try to parallelize if enough threads are available.  
    
## Running in a slurm cluster:
  
    cd PopGenAnalysis
    snakemake --profile slurm --use-conda
    
  Any necessary modifications required to run the pipeline in a cluster can be done in the *config.yaml* file in the *slurm* folder.
  
The *--cpus-per-task* in the slurm config file and the *--cores* option in the command line work together.

* If the threads provided in *--cores* is lesser than what is provided in *--cpus-per-task*, then SnakeMake will consider *--cores* input.  
* If threads provided in *--cores* is more than what is provided by *--cpus-per-task*, SnakeMake will try to parallelize multiple jobs in a node to use maximum threads.

__NOTE:__ Before running the pipeline in both cases, it is better to 
  * Create a dag file to visually see if the job order is correct. It will almost always be correct, but if it is not, please inform me.
  
        snakemake --dag | dot -Tsvg > dag.svg
        
  * Perform a dry run to manually check if the inputs/outputs for all rules are correct and if the number of jobs makes sense.
  
        snakemake --cores 1 -n
  
--------------------------------------------------------------------------------------------------------------------------------------------------------
## Pipeline Configuration

The *config.yaml* in the config folder is where all the changes to the pipeline parameters is done.

* __samples__

|Parameters|Value|Notes|
|----------|-----|-----|
|own|str|Name of your file. Should be in the form of "__name__.vcf.gz". Should be inside the config folder|
|ref|str|Name of the reference file. Should be in the form of "__name__.vcf.gz". Should be inside the config folder|

* __population_file__

|Parameters|Value|Notes|
|----------|-----|-----|
|population_file|str|Name of the population file in csv format. Should have 3 columns with headers<ul><li>ID - Sample IDs of yours and reference file in an order that you want your results in</li><li>Pop - Name of the population to which the sample belongs to</li><li>SuperPop - Name of the superpopulation to which the sample belongs to</li></ul>|

* __chromosome__

|Parameters|Value|Notes|
|----------|-----|-----|
|chromosome|int|No. of chromosomes present in the input files. Ideally it should be 22 since the pipeline only uses autosomes|

* __threads__

|Parameters|Value|Notes|
|----------|-----|-----|
|threads|int|No. of threads to be used by SnakeMake. More details above|

* __Analysis__

|Parameters|Value|Notes|
|----------|-----|-----|
|ADMIXTURE|bool|Tells the pipeline to run ADMIXTURE|
|SmartPCA|bool|Tells the pipeline to run SmartPCA|
|iHS|bool|Tells the pipeline to run iHS|
|XPEHH|bool|Tells the pipeline to run XPEHH|
|TreeMIX|bool|Tells the pipeline to run TreeMIX|

* __QualityCheck__

|Parameters|Value|Notes|
|----------|-----|-----|
|geno|float/int/bool|Removes variants which are missing in more than the given value number of samples. If it should not be run, __False__ should be given|
|mind|float/int/bool|Removes individuals which have more than the given value number of missing variants. If it should not be run, __False__ should be given|
|maf|float/int/bool|Removes variants which have maf lesser than the given value. If it should not be run, __False__ should be given|
|hwe|float/int/bool|Removes variants which are lower than the given value hardy-weinberg equilibrium. If it should not be run, __False__ should be given|
|heterozygosity|int/bool|Removes individuals more than the given value standard deviations from heterozygosity. If it should not be run, __False__ should be given|

* __iHS__

|Parameters|Value|Notes|
|----------|-----|-----|
|maf|int/float|Not functionally useful as of now since selscan by default removes variants with MAF <= 0.05|
|bins|int|No. of bins to be normalized in|
|pop|list|Populations for which iHS should be done|
|pop_type|str|The type of populations|

* __xpEHH__

|Parameters|Value|Notes|
|----------|-----|-----|
|pop|list|Your populations for which XP-EHH sdould be done|
|reference_pop|list|Populations against which XP-EHH will be done|
|pop_type|str|The type of populations. Both populations should be same type|
|mapping_pop|list|The populations which should be used in creating maps. Ideally should be same as __pop__|
|bins|int|no. of bins to be normalized in|

* __ADMIXTURE__

|Parameters|Value|Notes|
|----------|-----|-----|
|K|int|No. of ancestral populations. If value greater than 2, does ADMIXTURE from K=2 to K=given value|
|iterations|int|No. of times ADMIXTURE analysis should be done for each K|
|LDPruning  WindowSize|int|Window size considered for LD Pruning|
|LDPruning Shift|int|No. of base pairs to shift the window|
|LDPruning CorrelationCoefficient|float|Variant pairs above this value are considered to be LD, thus, removed|

* __SmartPCA__

|Parameters|Value|Notes|
|----------|-----|-----|
|LDPruning  WindowSize|int|Window size considered for LD Pruning|
|LDPruning Shift|int|No. of base pairs to shift the window|
|LDPruning CorrelationCoefficient|float|Variant pairs above this value are considered to be LD, thus, removed|
|Ethnicity_pop|list|SmartPCA gives 2 results-<ul><li>Overall PCA between your samples and reference samples</li><li>PCA between all the populations in your samples. The given value tells the pipeline which of the populations to consider.</li></ul>|
|pop_type|str|The population type for the second type of SmartPCA results|

* __TreeMIX__

|Parameters|Value|Notes|
|----------|-----|-----|
|Root|str|The populations which is to be considered as the root/oldest population|
|MigrationEdges|int|Number of migrations. If value more than 0, does gives results for MigrationEdges = 0 to MigrationEdges = given value|
|LDPruning WindowSize|int|Window size considered for LD Pruning|
|LDPruning Shift|int|No. of base pairs to shift the window|
|LDPruning CorrelationCoefficient|float|Variant pairs above this value are considered to be LD, thus, removed|

-------------------------------------------------------------------------------------------------------------------------------------------------------

## Troubleshooting

* The pipeline gives an error in the *rule HeterozygosityCheck* when running in a slurm cluster?  
This could mean that the rule is not able to run an Rscript because it cannot find R. Usually in clusters, the softwares are loaded as modules. Try loading the R module and run the pipeline again.

-------------------------------------------------------------------------------------------------------------------------------------------------------

#### Change 1.2.2

  All the analysis are now togglable to On/Off from the config file.

#### Change 1.2.1

  1. Indexing of a vcf file was done every time a rule was invoked. This led to problems when running in clusters since multiple nodes are re-writing the index files which cause some the rules in some nodes to not recognize the index file. New rules for indexing added.
  2. Location of the 'Filteredpop.csv' file was changed in multiple rules to the new location.

#### Change 1.2.0

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

#### Change 1.1.1

  The new population list csv file containing samples which passed Quality Checks is now created by a new rule *CreatingNewPopFile*.
  With this, running iHS does not depend on the rule *SortPopulations* since the population list file was created under this rule before.

#### Change 1.1.0 : QC Steps can be Run/Not Run

  Quality Check rules can be toggles **ON/OFF** by giving the input as a **Value/False** respectively in the config file.
  This includes-

  * rule *VariantMissingness* (geno)
  * rule *IndividualMissingness* (mind)
  * rule *MinorAlleleFrequency* (maf)
  * rule *HardyWeinbergEquilibriumCheck* (hwe)
  * rule *HeterozygosityCheck* (heterozygosity)
