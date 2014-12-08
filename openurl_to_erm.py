

#
# openurl_to_erm
#
# Usage: python openurl_to_erm.py opens first txt it finds and resolves into final.txt
#

import os
import string
import urllib2

from settings import *
#
#
#
def resolve(sfxIn):

  jdata = sfxIn.split('\t')
  title = jdata[1]
  issn = jdata[3].replace("-","")
  #use eISSN as fallback
  if issn == "":
    issn = jdata[7].replace("-","")
  url = BASE_URL+issn
  ermReady = GENERIC_TARGET_NAME+SEPARATOR+title+SEPARATOR+issn+SEPARATOR+url+"\n"

  return issn,ermReady


running_tally = {}

if __name__ == "__main__":
  print "Resolving",
  for f in os.listdir(os.getcwd()):
    if f[-3:] == "txt" and f != "final.txt":
      infile = open(f,"r")
      break
  if not infile:
    print " input file not found"
    exit
  print ""

for line in infile:
  key,data = resolve(line)
  #will only keep if ISSN or eISSN is associated with title
  if key != "":
    running_tally[key]= data



#Grab SP data as well
print "Grabbing SP file...",
sp_file = urllib2.urlopen("http://sfx.scholarsportal.info/brock/cgi/public/get_file.cgi?file=holdings_brock.txt")
for s in sp_file:
  key,data = resolve(s)
  running_tally[key]= data
print "done"


outfile = open("final.txt","w")
outfile.write(HEADING_LINE+"\n")

for k in sorted(running_tally):
  outfile.write(running_tally[k])


outfile.close()
infile.close()
print " fin"
