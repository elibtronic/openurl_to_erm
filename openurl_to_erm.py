

#
# openurl_to_erm
#
# Usage: python openurl_to_erm.py opens first txt it finds and resolves into final.txt
#

import os
import string

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

  return ermReady




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


outfile = open("final.txt","w")
outfile.write(HEADING_LINE+"\n")
for line in infile:
  outfile.write(resolve(line))

outfile.close()
infile.close()
print " fin"
