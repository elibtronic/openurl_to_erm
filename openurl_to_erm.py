
#
# openurl_to_erm
#
# Usage: python openurl_to_erm.py opens first txt it finds and resolves into final.txt
#
# Also requires https://pypi.python.org/pypi/Unidecode/0.04.1 to peform transliterations

import os
import string
import urllib2
import sys
import re
import codecs
from unidecode import unidecode

from settings import *

def resolveERM(sfxIn):

  jdata = sfxIn.split('\t')
  title = str(jdata[1])
  #If text language of journal is Korean, Chinese, or Russian can't transliterate title
  if re.search('kor',jdata[33]) or re.search('chi',jdata[33]) or re.search('thai',jdata[33]) or re.search('rus',jdata[33]):
    title = ""
    #keep track of error titles
    error_tally.append(sfxIn)
    return title,""
  
  issn = jdata[3]
  #use eISSN as fallback
  if issn == "":
    issn = jdata[7]
  url = BASE_URL+issn
  ermReady = title+SEPARATOR+title+SEPARATOR+issn+SEPARATOR+url+"\n"

  return issn,ermReady

def resolveTarget(sfxIn):

  jdata = sfxIn.split('\t')
  title = str(jdata[1])
  #If text language of journal is Korean, Chinese, or Russian can't transliterate title
  if re.search('kor',jdata[33]) or re.search('chi',jdata[33]) or re.search('thai',jdata[33]) or re.search('rus',jdata[33]):
    title = ""
    #keep track of error titles
    error_tally.append(sfxIn)
    return title,""
  
  issn = jdata[3]
  #use eISSN as fallback
  if issn == "":
    issn = jdata[7]
  url = BASE_URL+issn
  sfx_target= jdata[5]
  targetReady = title+SEPARATOR+sfx_target+SEPARATOR+issn+SEPARATOR+url+"\n"

  return issn,targetReady



running_tally = {}
error_tally = []

if __name__ == "__main__":
  print "Resolving",
  for f in os.listdir(os.getcwd()):
    if f[-3:] == "txt" and f != "final.txt" and f != "final_iii.txt" and f != "titles_not_kept.txt":
      infile = open(f,'r')
      break
  if not infile:
    print " input file not found"
    exit
  print ""

for line in infile:
  key,data = resolveERM(line)
  key_targets, data_targets = resolveTarget(line)
  #will only keep if ISSN or eISSN is associated with title
  if key != "":
    running_tally[key]= data
    running_tally_targets[ley_targets] = data_targets



#Grab SP data as well
print "Grabbing SP file...",
sp_file = urllib2.urlopen("http://sfx.scholarsportal.info/brock/cgi/public/get_file.cgi?file=holdings_brock.txt")
for s in sp_file:
  key,data = resolveERM(s)
  key_targets, data_targets = resolveTarget(s)
  running_tally[key]= data
  running_tally[key_targets] = data_targets
print "done"


outfile = open("final.txt","wb")
outfile_targets = open("final-targets.txt","wb")
errorfile = open("titles_not_kept.txt","wb")

outfile.write(HEADING_LINE+"\n")
outfile_targets.write(HEADING_LINE+"\n")

# I hate strings in Python
for k in sorted(running_tally):
  outfile.write(unidecode(running_tally[k].decode('string-escape').decode('utf-8')))

for k in sorted(running_tally_targets):
  outfile_targets.write(unidecode(running_tally_targets[k].decode('string-escape').decode('utf-8')))

for k in sorted(error_tally):
  errorfile.write(unidecode(k.decode('string-escape').decode('utf-8')))


outfile.close()
outfile_targets.close()
errorfile.close()
infile.close()
print " fin"
