#!/usr/bin/env python


import shlex, subprocess
from subprocess import Popen, PIPE


#output = subprocess.call(['ede_marginfile_validation_python/LibraryFile/validateMarginFile.sh 3 margin3_1.csv'])
session = subprocess.Popen(['./validateMarginFile.sh','3','../DataFile/sample3.0.csv'], stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()

print stdout

if stderr:
    raise Exception("Error "+str(stderr))