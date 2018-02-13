import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
import shlex, subprocess
from subprocess import Popen, PIPE
import cgi   





def validateFile(file_path):
    print "prior to validate the file at : ", file_path
    form = cgi.FieldStorage()
    file_format = form.getvalue('file_format')
    print "file format is  : "
    print file_format  
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'validateMarginFile.sh')
    print dir
    session = subprocess.Popen(['./validateMarginFile.sh','3',file_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    print stdout
    print "after exe"



validateFile("xxxyyy");