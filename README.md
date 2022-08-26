# PopGenAnalysis
This repository contains the pipeline script for Population Genetics Analysis built using SnakeMake

Version 1.2.0

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

Version 1.1.1

  The new population list csv file containing samples which passed Quality Checks is now created by a new rule *CreatingNewPopFile*.
  With this, running iHS does not depend on the rule *SortPopulations* since the population list file was created under this rule before.

Version 1.1.0 : QC Steps can be Run/Not Run

  Quality Check rules can be toggles **ON/OFF** by giving the input as a **Value/False** respectively in the config file.
  This includes-

  * rule *VariantMissingness* (geno)
  * rule *IndividualMissingness* (mind)
  * rule *MinorAlleleFrequency* (maf)
  * rule *HardyWeinbergEquilibriumCheck* (hwe)
  * rule *HeterozygosityCheck* (heterozygosity)
