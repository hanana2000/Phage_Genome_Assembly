#this has to be run with python3

#set this using pwd for main directory 
WORKINGDIR = r"/nfs1/BIOMED/Danelishvili_Lab/Trimmomatic_data"
OUTPUTDIR = r"/nfs1/BIOMED/Danelishvili_Lab/Trimmed_Deduped_Data"
HOSTGENOME = r"smeg_sequence.fasta"
ORIGREADSDIR = r"/nfs1/BIOMED/Danelishvili_Lab/Untrimmed_Read_Data"
FILEPREFIX = r"Ph"
DIVIDER = r"_"


import os

os.system(f"bwa index {HOSTGENOME}")

directory = r'./'

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

x = 0

for phage in phage_names:
  # the folder name variable is assigned based on the 
  # prefix+phage number at the begining of the file name. 
  # Replace the "DIVIDER" variable with the character 
  # that separates the prefix from the rest of the foldername. 

  # make a directory for the current phage in the output directory 
  os.system(f"mkdir {OUTPUTDIR}/{phage}")
  
  #check against smegmatis genome to filter out smeg DNA, 
  # output to a bam alignment file called {phage number}-smegmatis.bam
  os.system(f"bwa mem -t 32 {HOSTGENOME} {WORKINGDIR}/{phage}_trimmomatic/{phage}-trimmed_1P {WORKINGDIR}/{phage}_trimmomatic/{phage}-trimmed_2P | samtools sort -@ 32 -o {WORKINGDIR}/{phage}_trimmomatic/{phage}-smegmatis.bam -")

  # Use samtools to remove reads that were aligned to host genome in 
  # the 
  # DO NOT -f 4, use -f 12 so it will remove pairs even if only one of the pair mapped to smegmatis. 
  os.system(f"samtools view -b -f 12 {WORKINGDIR}/{phage}_trimmomatic/{phage}-smegmatis.bam >{WORKINGDIR}/{phage}_trimmomatic/{phage}.bam")
  os.system(f"samtools sort -@ 8 -n {WORKINGDIR}/{phage}_trimmomatic/{phage}.bam -o {WORKINGDIR}/{phage}_trimmomatic/{phage}-sorted.bam")

  #convert bam file to fastq file with filtered, trimmed reads
  os.system(f"samtools bam2fq {WORKINGDIR}/{phage}_trimmomatic/{phage}-sorted.bam >{WORKINGDIR}/{phage}_trimmomatic/{phage}-phage.fastq")
  
  print("\n\n\n")

  


