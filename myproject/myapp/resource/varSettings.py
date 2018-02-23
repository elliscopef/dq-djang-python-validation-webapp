import sys
import os
from contextlib import contextmanager
from cStringIO import StringIO
import io

global vali_margin_shell_script
global vali_margin_30_path
global vali_margin_10_path
global pos_txt_file_path
global td_configfile_name
global stdoutRedirect

global mystdout
global old_stdout


# old_stdout = sys.stdout
# sys.stdout = mystdout = StringIO()

# print('Got stdout: "{0}"'.format(f.getvalue()))

# sys.path[0]  = /Users/mifang/Documents/Expedia/Project/tutorial/djangoTutorial/dq-djang-python-validation-webapp/myproject/
vali_margin_shell_script = os.path.join(sys.path[0], 'myproject/myapp/resource/validateMarginFile.sh')
pos_txt_file_path = os.path.join(sys.path[0], 'myproject/myapp/resource/LibraryFile/pos.txt')
td_configfile_name = os.path.join(sys.path[0], 'myproject/myapp/resource/LibraryFile/udaexec.ini')
# vali_margin_10_path = 
# vali_margin_30_path =
print vali_margin_shell_script
print pos_txt_file_path

# if __name__ == "__main__":

    


