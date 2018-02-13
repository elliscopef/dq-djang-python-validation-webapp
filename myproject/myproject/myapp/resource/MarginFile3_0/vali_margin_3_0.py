


from .. import varSettings

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
import sys
import pandas as pd
import numpy as np

try:  
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

global pos_dic

#Connect to the teradata  
# udaExec = teradata.UdaExec (appName="HelloWorld", version="1.0",
#         logConsole=False)
 
# session = udaExec.connect(method="odbc", system="tddev",
#         username="D_DM_BEX_CLICKSTREAM_ADB", password="D_DM_BEX_CLICKSTREAM_ADB284641");
 
# for row in session.execute("select OREPLACE(SITE_NAME,'.',' ') as SITE_NAME from D_ADS_BEX_COMMON.DM_OMNITURE_SITE"):
#     print(row)


#Validation Helper Functions:

#Variable for manualchange
#************************************************************************************************************

row_tracker = 1
#NEED UPDATE 

pkg_sa_set = set(['Package','Standalone','Part Of Package'])
mer_agn_set = set(['Merchant','Agency','Direct Agency'])
lob_set = set(['Air','Car','Lodging','Hotel','Insurance','DestSvc' ,'Cruise','Train'])
onlien_offln_ind_set = set(['Online','Offline'])

#************************************************************************************************************



def load_pos_data():
	with open(varSettings.pos_txt_file_path) as f:
		content = f.readlines()

	content = [x.strip() for x in content]

	return content


def validation_fail_msg():
	print "The validation process terminates due to above error message"


def section_fail_msg(section_name):
	print section_name + " Column Format isn't Correct"
	validation_fail_msg()


def section_validated_msg(section_name):
	print section_name + " Column Format Validated Successfully"
	global row_tracker 
	row_tracker = 1


def checkYearFormat(int):
	return len(str(int)) == 4


def checkMonthFormat(input):
	if not isinstance(input, int):
		return False
	if not 1<= input <= 12:
		return False
	return True


def checkPOSFormat(input,pos_dic):
	if not isinstance(input, str):
		return False
	if not input in pos_dic:
		print input + " is not a recognized site name"
		return False
	pos_dic[input] = int(pos_dic[input])+1	
	return True


def checkPkg_saFormat(input):
	if not isinstance(input, str):
		return False
	if not input in pkg_sa_set:
		return False		
	return True


def checkMer_agnFormat(input):
	if not isinstance(input, str):
		return False
	if not input in mer_agn_set:
		return False		
	return True


def checkLobFormat(input):
	if not isinstance(input, str):
		return False
	if not input in lob_set:
		return False		
	return True


def checkOnline_offFormat(input):
	if not isinstance(input, str):
		return False
	if not input in onlien_offln_ind_set:
		return False		
	return True


def row_tracker_alert():
	print "Error input at : " + str(row_tracker)


def row_tracker_incre():
	global row_tracker
	row_tracker+=1


def check_if_less_than_one(input,df):
	return df[df[input] >1].empty


def check_factor_column(column_name,df):
	if check_if_less_than_one(column_name,df):
		section_validated_msg(column_name)
	else:
		section_fail_msg(column_name)
		sys.exit(0)



def validateMarginFile_v3(sourceFileName):
	print"Initialize the validation process" 
	print "Start to Load the margin 3.0 file"
	pos_set  = load_pos_data()
	filename = sourceFileName
	df = pd.read_csv(filename,index_col=False)
	print "Load file successfully"
	print "Start to validate the column"


	zeroList = [0] * len(pos_set)
	pos_list_tuple = zip(pos_set, zeroList)
	pos_dic = dict(pos_list_tuple)



	header_set = list(df)
	#CheckHeader 
	if(header_set[0].strip() != 'YEAR' or header_set[1].strip() !='MONTH' or header_set[2].strip() != 'POS' or header_set[3].strip() != 'PKG_SA' or header_set[4].strip() != 'MER_AGN' or header_set[5].strip() != 'LOB' or header_set[6].strip() != 'ONLINE_OFFLN_IND' ):
		if(header_set[7].strip() != 'REV_ADJ_FACTR_%' or header_set[8].strip() != 'COS_ADJ_FACTR_%' or header_set[9].strip() != 'VCOS_ADJ_FACTR_%'):
			print "Header isn't formatted correctly"
			sys.exit(0)


#YEAR
#YEAR in YYYY format
	for year in df[header_set[0].strip()]:
		row_tracker_incre()
		if not checkYearFormat(year):
			section_fail_msg(header_set[0].strip())
			row_tracker_alert()
			sys.exit(0)
	section_validated_msg(header_set[0].strip())

#Month
# in mm format
	for month in df[header_set[1].strip()]:
		row_tracker_incre()
		if not checkMonthFormat(month):
			section_fail_msg(header_set[1].strip())
			row_tracker_alert()
			sys.exit(0)

	section_validated_msg(header_set[1].strip())

#POS
#Point of Sale. It should match with site name in dm_omniture_site (e.g., 'Expedia JP', 'Airasiago SG', 'Expedia Barclays'
	for pos in df[header_set[2].strip()]:
		row_tracker_incre()
		pos = pos.upper() #Convert to All Uppercase for alignment
		if not checkPOSFormat(pos,pos_dic):
			section_fail_msg(header_set[2].strip())
			row_tracker_alert()
			sys.exit(0)

	section_validated_msg(header_set[2].strip())


#PKG_SA
#Valid values 
#Case sensitive
	for pkg_sa in df[header_set[3].strip()]:
		row_tracker_incre()
		if not checkPkg_saFormat(pkg_sa):
			section_fail_msg(header_set[3].strip())
			row_tracker_alert()
			sys.exit(0)

	section_validated_msg(header_set[3].strip())



#Business Model Name
#Case sensitive
	for mer_agn in df[header_set[4].strip()]:
		row_tracker_incre()
		if not checkMer_agnFormat(mer_agn):
			section_fail_msg(header_set[4].strip())
			row_tracker_alert()
			sys.exit(0)

	section_validated_msg(header_set[4].strip())

#LOB
	for lob in df[header_set[5].strip()]:
		row_tracker_incre()
		if not checkLobFormat(lob):
			section_fail_msg(header_set[5].strip())
			row_tracker_alert()
			sys.exit(0)

	section_validated_msg(header_set[5].strip())

#onlien_offln_ind
#Online/offline indicator - Valid Values 
#Case Sensitive
	for onlien_offln_ind in df[header_set[6].strip()]:
		row_tracker_incre()
		if not checkOnline_offFormat(onlien_offln_ind):
			section_fail_msg(header_set[6].strip())
			row_tracker_alert()
			sys.exit(0)

	section_validated_msg(header_set[6].strip())

#dest_airpt_iata_regn_name
#Destination Airport Region Name (for Air only)

#dom_intl_ind
#International or Domestic (for air only)

#rev_adj_factr_%
 #<=1 
#Adj Factr for Net Rev. It should beelse process will be aborted.
	check_factor_column(header_set[7].strip(),df)
#rev_adj_factr_unit
#Adj Factr for Net Rev(for Air only)


#cos_adj_factr_%
#<=1 
#Adj Factr for Cost of Sale. It should be <=1 else process will be aborted.
	check_factor_column(header_set[8].strip(),df)

#cos_adj_factr_unit
# Adj Factr for Cost of Sale(for Air only)

# vcos_adj_factr_%
#<=1 
# Adj Factr for Variable Cost of Sale. It should be <=1 else process will be aborted.
	check_factor_column(header_set[9].strip(),df)

# vcos_adj_factr_unit
# Adj Factr for Variable cost of sale(for Air only)

	print "Below is a list of site names not shown up in table"
	print "Point of sale, number of occurance"
	for x in pos_dic:
		if(pos_dic[x]==0):
			print (x,pos_dic[x])
	

	print "Validation Successfully Completed"

	print "Validation process finished for " + filename + ". Ready to Upload"
