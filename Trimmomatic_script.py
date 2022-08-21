#this has to be run with python3

#set this using pwd for main directory 
WORKINGDIR = r'/nfs1/BIOMED/Danelishvili_Lab/Untrimmed_Read_Data'
OUTPUTDIR = r"/nfs1/BIOMED/Danelishvili_Lab/Trimmomatic_data"
HOSTGENOME = r"smeg_sequence.fasta"
FILEPREFIX = r"Ph"
DIVIDER = r"_"

FASTQCLOCATION = r"/local/cluster/fastqc/fastqc"
TRIMMOMATICLOCATION = r"/local/cluster/Trimmomatic/trimmomatic-0.39.jar"

import os

os.system("bwa index smeg_sequence.fasta")

list_of_Ph_files = []

pair_completed = False


# This will parse through the directory where the original, 
# untrimmed paired reads have been stored. 
# Substitute WORKINGDIR with the directory 
# where the original reads can be found. 
files = sorted(os.scandir(WORKINGDIR), key=lambda e: e.name)

for entry in files:
  # add all the original read files to the list of ph files
  if not entry.path.endswith(".fastq.gz"): continue # move on to next file if it's not .fq
  list_of_Ph_files.append(entry.name)
  print((entry.name.split("-")[8]).split("_")[0]) 
#print(list_of_Ph_files)

x = 0

while x < len(list_of_Ph_files):
  # assign the folder name based on the file name -- 
  # my files specifically had the phage prefix and number at the 
  # 8th segment of the file name, divided by "-" and then "_". 
  # Your files may be named differently, change this line according 
  # to your file naming format
  folder_name = (list_of_Ph_files[x].split("-")[8]).split("_")[0] # Folder name based on the prefix of the files
  file_1 = list_of_Ph_files[x]
  file_2 = list_of_Ph_files[x+1]

#make directory for current phage in the output directory 
  os.system(f"mkdir {OUTPUTDIR}/{folder_name}_trimmomatic")  

#run fastqc to quality check for adapters on untrimmed files 
  os.system(f" {FASTQCLOCATION} {file_1} {file_2} --outdir=fastqc/. >fastqc/{folder_name}.log 2>&1") 

# trim the files using trimmomatic. I have specified Illumina nexterea adapters,
# but this may be different based on your sequencing method. 
# Make sure to replace the adapter argument with the correct adapter name
  os.system(f"java -jar {TRIMMOMATICLOCATION} PE -threads 20 -phred33 -summary {OUTPUTDIR}/{folder_name}_trimmomatic/statsSummaryFile-{folder_name}.txt -validatePairs {WORKINGDIR}/{file_1} {WORKINGDIR}/{file_2} -baseout {OUTPUTDIR}/{folder_name}_trimmomatic/{folder_name}-trimmed ILLUMINACLIP:./adapters/NexteraPE-PE.fa:2:30:10 ILLUMINACLIP:./adapters/TruSeq3-PE.fa:2:30:10 MAXINFO:30:0.8 >{OUTPUTDIR}/{folder_name}_trimmomatic/trimmomatic-{folder_name}.log 2>&1") 

#fastqc quality check again to make sure nextera adapters removed
  os.system(f" {FASTQCLOCATION} {OUTPUTDIR}/{folder_name}_trimmomatic/{folder_name}-trimmed_1P {OUTPUTDIR}/{folder_name}_trimmomatic/{folder_name}-trimmed_2P --outdir=trimmed-fastqc/. >trimmed-fastqc/{folder_name}.log") 

  print("\n\n\n")
  x+=2

