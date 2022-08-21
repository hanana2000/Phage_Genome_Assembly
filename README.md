# Phage_Genome_Assembly
# Hannah Kapoor -- can be contacted at hannahkapoor00@gmail.com
# Co-mentor Dr. Stephen Ramsey 
# Oregon State University 

This code must be run with Python3. 

To run all three of these files, the following programs are needed: 
- Trimmomatic 
- BWA
- Samtools 
- SPAdes 
- FASTQ

Input files should be illumina paired end reads. These will be processed by the first script, and the output of the first script will be in input for the second script and so on. 
The files were intended to be used in the following order: 
- Trimmomatic_script
- Smegmatis_Host_filtering
- Spades_assembly

The trimmomatic script removes the adapter sequences at the ends of the paired reads. 
The Smegmatis host filter script will remove all reads that match to the host genome. 
The Spades assembly script will assemble the reads into larger contigs, and possibly output the entire assembled genome. 
Several Fastq quality checks will also be done within theses files, and Fastq files will be outputted into the corresponding directories. These can be used to determine if adapter sequences have been removed succesfully and if host DNA contamination is present. 
All files have comments indicating variables that need to be changed based on your file structure. 
Constant variables will need to be changed to exact directory paths (working directory, output directory, path to programs)

Here is an example of the command to run the first script:  
python3 -u Trimmomatic_script.py | tee Trimmomatic_script.log

This will output all runtime activity to a log file. 

