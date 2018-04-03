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
MIN_NUM_COLUMN = 10
row_tracker = 1
#NEED UPDATE 

pkg_sa_set = set(['Package','Standalone','Part Of Package'])
mer_agn_set = set(['Merchant','Agency','Direct Agency'])
lob_set = set(['Air','Car','Lodging','Hotel','Insurance','DestSvc' ,'Cruise','Train'])
onlien_offln_ind_set = set(['Online','Offline'])
column_name_order = ['YEAR','MONTH','POS','PKG_SA','MER_AGN','LOB','ONLINE_OFFLN_IND','DEST_AIRPT_IATA_REGN_NAME','DOM_INTL_IND','REV_ADJ_FACTR_%','REV_ADJ_FACTR_UNIT','COS_ADJ_FACTR_%','COS_ADJ_FACTR_UNIT','VCOS_ADJ_FACTR_%','VCOS_ADJ_FACTR_UNIT','MESOLOY_ADJ_FACTR_%','MESOLOY_ADJ_FACTR_UNIT','MESO_ADJ_FACTR_%','MESO_ADJ_FACTR_UNIT','LOYALTY_ADJ_FACTR_%','LOYALTY_ADJ_FACTR_UNIT','OTHER_ADJ_FACTR_%','OTHER_ADJ_FACTR_UNIT','BEC_ADJ_FACTR_UNIT']
#************************************************************************************************************



def load_pos_data():
	with open(varSettings.pos_txt_file_path) as f:
		content = f.readlines()

	content = [x.strip() for x in content]

	return content


def validation_fail_msg(logInfo):
	logInfo.append("The validation process terminates due to above error message")
	return


def section_fail_msg(section_name,logInfo,logError):
	logError.append(section_name + " Column Format isn't Correct")
	validation_fail_msg(logInfo)


def section_validated_msg(section_name,logInfo):
	logInfo.append(section_name + " Column Format Validated Successfully")
	global row_tracker 
	row_tracker = 1


def checkYearFormat(int,logInfo):
	return len(str(int)) == 4


def checkMonthFormat(input,logInfo):
	if not isinstance(input, int):
		return False
	if not 1<= input <= 12:
		return False
	return True


def checkPOSFormat(input,pos_dic,logInfo,logError):
	if not isinstance(input, str):
		return False
	if not input in pos_dic:
		logError.append(input + " is not a recognized site name")
		return False
	pos_dic[input] = int(pos_dic[input])+1	
	return True


def checkPkg_saFormat(input,logInfo):
	if not isinstance(input, str):
		return False
	if not input in pkg_sa_set:
		return False		
	return True


def checkMer_agnFormat(input,logInfo):
	if not isinstance(input, str):
		return False
	if not input in mer_agn_set:
		return False		
	return True


def checkLobFormat(input,logInfo):
	if not isinstance(input, str):
		return False
	if not input in lob_set:
		return False		
	return True


def checkOnline_offFormat(input,logInfo):
	if not isinstance(input, str):
		return False
	if not input in onlien_offln_ind_set:
		return False		
	return True


def row_tracker_alert(logInfo):
	logInfo.append("Error input at : " + str(row_tracker))


def row_tracker_incre(logInfo):
	global row_tracker
	row_tracker+=1

def row_tracker_reset():
	global row_tracker
	row_tracker=1


def check_if_less_than_one(input,df,logInfo,logError):
	return df[df[input] >1].empty


def check_factor_column(column_name,df,logInfo,logError):
	if check_if_less_than_one(column_name,df,logInfo,logError):
		section_validated_msg(column_name,logInfo)
	else:
		section_fail_msg(column_name,logInfo,logError)



def validateMarginFile_v3(sourceFileName,logInfo,logError):
	print"Initialize the validation process" 
	logInfo.append("Start to Load the margin 3.0 file: "+sourceFileName)
	pos_set  = load_pos_data()
	filename = sourceFileName
	try:
		df = pd.read_csv(filename,index_col=False)
	except:
		logInfo.append("Reading csv file failes.Please upload a csv file.")
		return
	logInfo.append("Load file successfully")
	logInfo.append("Start to validate the column")


	zeroList = [0] * len(pos_set)
	pos_list_tuple = zip(pos_set, zeroList)
	pos_dic = dict(pos_list_tuple)



	header_set = list(df)
	print header_set
	#CheckHeader 
	if(len(header_set) <= MIN_NUM_COLUMN):
		logError.append(len(header_set))
		logError.append("Header column count number isn't correct ")
		return 

	for i in range(9):
		if(header_set[i].strip()!=list(column_name_order)[i]):
			logError.append("Header:" +column_name_order[i]+" isn't formatted correctly")
			return



#YEAR
#YEAR in YYYY format
	row_tracker_reset()
	for year in df[header_set[0].strip()]:
		row_tracker_incre(logInfo)
		if not checkYearFormat(year,logInfo):
			row_tracker_alert(logInfo)
			section_fail_msg(header_set[0].strip(),logInfo,logError)
	section_validated_msg(header_set[0].strip(),logInfo)

#Month
# in mm format
	row_tracker_reset()
	for month in df[header_set[1].strip()]:
		row_tracker_incre(logInfo)
		if not checkMonthFormat(month,logInfo):
			row_tracker_alert(logInfo)
			section_fail_msg(header_set[1].strip(),logInfo,logError)
	section_validated_msg(header_set[1].strip(),logInfo)

#POS
#Point of Sale. It should match with site name in dm_omniture_site (e.g., 'Expedia JP', 'Airasiago SG', 'Expedia Barclays'
	row_tracker_reset()
	for pos in df[header_set[2].strip()]:
		row_tracker_incre(logInfo)
		pos = pos.upper() #Convert to All Uppercase for alignment
		if not checkPOSFormat(pos,pos_dic,logInfo,logError):
			row_tracker_alert(logInfo)
			section_fail_msg(header_set[2].strip(),logInfo,logError)
	section_validated_msg(header_set[2].strip(),logInfo)


#PKG_SA
#Valid values 
#Case sensitive
	row_tracker_reset()
	for pkg_sa in df[header_set[3].strip()]:
		row_tracker_incre(logInfo)
		if not checkPkg_saFormat(pkg_sa,logInfo):
			row_tracker_alert(logInfo)
			section_fail_msg(header_set[3].strip(),logInfo,logError)
	section_validated_msg(header_set[3].strip(),logInfo)



#Business Model Name
#Case sensitive
	row_tracker_reset()
	for mer_agn in df[header_set[4].strip()]:
		row_tracker_incre(logInfo)
		if not checkMer_agnFormat(mer_agn,logInfo):
			row_tracker_alert(logInfo)
			section_fail_msg(header_set[4].strip(),logInfo,logError)
	section_validated_msg(header_set[4].strip(),logInfo)

#LOB
	row_tracker_reset()
	for lob in df[header_set[5].strip()]:
		row_tracker_incre(logInfo)
		if not checkLobFormat(lob,logInfo):
			row_tracker_alert(logInfo)
			section_fail_msg(header_set[5].strip(),logInfo,logError)
	section_validated_msg(header_set[5].strip(),logInfo)

#onlien_offln_ind
#Online/offline indicator - Valid Values 
#Case Sensitive
	row_tracker_reset()
	for onlien_offln_ind in df[header_set[6].strip()]:
		row_tracker_incre(logInfo)
		if not checkOnline_offFormat(onlien_offln_ind,logInfo):
			row_tracker_alert(logInfo)
			section_fail_msg(header_set[6].strip(),logInfo,logError)
	section_validated_msg(header_set[6].strip(),logInfo)

#dest_airpt_iata_regn_name
#Destination Airport Region Name (for Air only)

#dom_intl_ind
#International or Domestic (for air only)

#rev_adj_factr_%
 #<=1 
#Adj Factr for Net Rev. It should beelse process will be aborted.
	check_factor_column(header_set[7].strip(),df,logInfo,logError)
#rev_adj_factr_unit
#Adj Factr for Net Rev(for Air only)


#cos_adj_factr_%
#<=1 
#Adj Factr for Cost of Sale. It should be <=1 else process will be aborted.
	check_factor_column(header_set[8].strip(),df,logInfo,logError)

#cos_adj_factr_unit
# Adj Factr for Cost of Sale(for Air only)

# vcos_adj_factr_%
#<=1 
# Adj Factr for Variable Cost of Sale. It should be <=1 else process will be aborted.
	check_factor_column(header_set[9].strip(),df,logInfo,logError)

# vcos_adj_factr_unit
# Adj Factr for Variable cost of sale(for Air only)

	logInfo.append("Below is a list of site names not shown up in table")
	logInfo.append("Point of sale, number of occurance")
	logInfo.append(" START_____________________________________SITE NAME, COUNT DISPLAY_____________________________________")

	for x in pos_dic:
		# if(pos_dic[x]==0):
			logInfo.append((x,pos_dic[x]))
	logInfo.append(" END  _____________________________________SITE NAME, COUNT DISPLAY_____________________________________")

	logInfo.append("Validation Successfully Completed")

	logInfo.append("Validation process finished for " + filename + ". Ready to Upload")
	print logInfo
