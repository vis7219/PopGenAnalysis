args = commandArgs(trailingOnly = TRUE)
filein = args[1]
fileout = args[2]
no_of_sd = strtoi(args[3])

het <- read.csv(filein, head=TRUE, sep= '\t')
het$HET_RATE = (het$"OBS_CT" - het$"O.HOM.")/het$"OBS_CT"
het_fail = subset(het, (het$HET_RATE < mean(het$HET_RATE)-no_of_sd*sd(het$HET_RATE)) | (het$HET_RATE > mean(het$HET_RATE)+no_of_sd*sd(het$HET_RATE)));
het_fail$HET_DST = (het_fail$HET_RATE-mean(het$HET_RATE))/sd(het$HET_RATE);
write.table(het_fail, fileout, row.names=FALSE)
