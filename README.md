# PopGenAnalysis
This repository contains the pipeline script for Population Genetics Analysis built using SnakeMake


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
