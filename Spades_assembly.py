#this has to be run with python3

import os

#set this using pwd for main directory
WORKINGDIR = r"/nfs1/BIOMED/Danelishvili_Lab/Trimmomatic_data"
OUTPUTDIR = r"/nfs1/BIOMED/Danelishvili_Lab/spades_assembly"
SPADESPATH = r"/local/cluster/SPAdes/bin/spades.py"
FILEPREFIX = r"Ph"
DIVIDER = r"_"


files  = sorted(os.scandir(WORKINGDIR), key=lambda e: e.name)

phage_names = []

for entry in files:
  #look for any folders that start with Ph, 
  # because my phage folders are names in the format "Ph123". 
  # Substitute FILEPREFIX with what your phage files start with,
  # and DIVIDER with name the name separation character
  if entry.is_dir() and entry.name.startswith(f"{FILEPREFIX}"): 
    phage_names.append(entry.name.split(f"{DIVIDER}")[0])

print(phage_names)
    
for phage in phage_names: 
  #this should be the path to the current phage file, 
  # my files are stored within a directory with the suffix "_trimmomatic", 
  # and the files have the suffix "-phage". change this as needed. 
  phage_file = f"{WORKINGDIR}/{phage}_trimmomatic/{phage}-phage.fastq"

  #this is the SPAdes command for a single, interlaced reads file (with forward and reverse reads). See the SPAdes manual to determine what flags are needed for your specific file type. Default k-mers are being used here, use -k {k-mer size} to customize what k-mer size you would like to try
  os.system(f"{SPADESPATH} --12 {phage_file} -o {OUTPUTDIR}/{phage}_spades_output")


#run with python3 -u spades_script.py | tee spades_script.log
#this will redirect all runtime output to a log file


 


