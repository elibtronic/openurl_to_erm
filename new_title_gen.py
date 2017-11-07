

#
# This script will create a new titles csv
# When given a txt of brief bibs ("brief_bib_data.txt") that looks like this:
#  "022","TITLE"
#
# It will use the output of the other script to make this list
# Output will look like
# ISSN,TITLE,SFX_TARGET_NAME
#
# When it hits error it dumps that in the final file


b_file = open("brief_bib_data.txt","r")
lookup_file = open("final-targets.txt","r")

nt_file = open("newtitles.txt","w")

tlookup = dict()
for l in lookup_file:
    spliter = l.split("|")
    tlookup[spliter[2]] = spliter[1]

for b in b_file:
    spliter = b.split(",")
    if spliter[0].strip('"') == "022":
        pass
    else:
        try:
            target = tlookup[spliter[0].strip('"')]
            nt_file.write(b.strip('\n')+',"'+target+'"\n')
        except:
            nt_file.write(b.strip('\n')+',"ERROR IN DATA"\n')
        
