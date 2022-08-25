# PopGenAnalysis
This repository contains the pipeline script for Population Genetics Analysis built using SnakeMake


Version 1.0.1 : QC Steps can be Run/Not Run

  Quality Check rules can be toggles **ON/OFF** by giving the input as a **Value/False** respectively in the config file.
  This includes-

  * rule *VariantMissingness* (geno)
  * rule *IndividualMissingness* (mind)
  * rule *MinorAlleleFrequency* (maf)
  * rule *HardyWeinbergEquilibriumCheck* (hwe)
  * rule *HeterozygosityCheck* (heterozygosity)
