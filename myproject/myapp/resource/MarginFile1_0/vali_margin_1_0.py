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

#Validation Helper Functions:


#Variable for manual change
#************************************************************************************************************

row_tracker = 1
#NEED UPDATE 
account_set  = set(['Revenue % of GB', 'GP % of GB', 'Variable GP % of GB'])
pkg_sa_set = set(['Package','Standalone','Part Of Package'])
mer_agn_set = set(['Merchant','Agency','Direct Agency','Not Applicable'])
lob_set = set(['Air','Car','Lodging','Hotel','Insurance','DestSvc' ,'Cruise','Train'])
onlien_offln_ind_set = set(['Online','Offline'])
product_set = set(['3P Package','Car','Hotel','Flight','Cruise', 'EPackage', 'Insurance','Tshop'])



#************************************************************************************************************

def load_pos_data():
	with open(varSettings.pos_txt_file_path) as f:
		content = f.readlines()
	content = [x.strip() for x in content]

	#Remove the redundent header
	return content


def validation_fail_msg(logInfo):
	logInfo.append("The validation process terminates due to above error message")


def section_fail_msg(section_name,logInfo,logError):
	logError.append(section_name + " Column Format isn't Correct")
	validation_fail_msg(logError)


def section_validated_msg(section_name,logInfo):
	logInfo.append(section_name + " Column Format Validated Successfully")
	# row_tracker = 1


def checkAccountFormat(input,logInfo):
	if not isinstance(input, str):
		return False
	if not input in account_set:
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


def checkBusinessTypeFormat(input,logInfo):
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


def checkProductFormat(input,logInfo):
	if not isinstance(input, str):
		return False
	if not input in product_set:
		return False		
	return True


def checkPercentageFormat(input,logInfo):
	if input.endswith('%'):
		input = input[:-1]
		input_change = float(input)



def row_tracker_alert(logInfo):
	logInfo.append("Error input at : " + str(row_tracker))


def row_tracker_incre(logInfo):
	global row_tracker
	row_tracker+=1

def row_tracker_reset():
	global row_tracker
	row_tracker=1

def check_if_less_than_one(input,logInfo):
	return df[df[input] >1].empty


def check_factor_column(column_name,logInfo):
	if check_if_less_than_one(column_name):
		section_validated_msg(column_name)
	else:
		section_fail_msg(column_name,logInfo,logError)
		return


def validateMarginFile_v1(sourceFileName,logInfo,logError):
	print"Initialize the validation process" 
	logInfo.append("Start to Load the margin 1.0 file" +sourceFileName)
	pos_set = load_pos_data()
	zeroList = [0] * len(pos_set)
	pos_list_tuple = zip(pos_set, zeroList)
	pos_dic = dict(pos_list_tuple)

	filename = sourceFileName
	df = pd.read_csv(filename,index_col=False)
	logInfo.append("Load file successfully")
	logInfo.append("Start to validate the column")


#Retrive the header set of the data
	header_set = list(df)

#CheckHeader 
	if(header_set[0].strip() != 'Account' or header_set[1].strip() !='Point of Sale' or header_set[2].strip() != 'Business Type' or header_set[3].strip() != 'Product'):
		logInfo.append("<mark>Header isn't formatted correctly</mark>")
		return



#Account
	row_tracker_reset()
	for account in df[header_set[0]]:
		row_tracker_incre(logInfo)
		if not checkAccountFormat(account,logInfo):
			section_fail_msg(header_set[0],logInfo,logError)
			row_tracker_alert(logInfo)
			return

	section_validated_msg(header_set[0],logInfo)

#POS
#Point of Sale. It should match with site name in dm_omniture_site (e.g., 'Expedia JP', 'Airasiago SG', 'Expedia Barclays'
	row_tracker_reset()
	for pos in df[header_set[1]]:
		row_tracker_incre(logInfo)
		pos = pos.upper() #Convert to All Uppercase for alignment
		if not checkPOSFormat(pos,pos_dic,logInfo,logError):
			section_fail_msg(header_set[1],logInfo,logError)
			row_tracker_alert(logInfo)
			return

	section_validated_msg(header_set[1],logInfo)

#Business Type
	row_tracker_reset()
	for business_type in df[header_set[2]]:
		row_tracker_incre(logInfo)
		if not checkBusinessTypeFormat( business_type,logInfo):
			section_fail_msg(header_set[2],logInfo,logError)
			row_tracker_alert(logInfo)
			return

	section_validated_msg(header_set[2],logInfo)

#   Product
	row_tracker_reset()
	for product in df[header_set[3]]:
		row_tracker_incre(logInfo)
		if not checkProductFormat(product,logInfo):
			section_fail_msg(header_set[3],logInfo,logError)
			row_tracker_alert(logInfo)
			return

	section_validated_msg(header_set[3],logInfo)

	data_column_name = df.columns[4:]
	for date in data_column_name:
		for data_entry in df[date]:
			try:
				checkPercentageFormat(data_entry,logInfo)
			except ValueError:
				logError.append("ValueError: Value can not be converted to float format.")
				section_fail_msg(date,logInfo,logError)
				return

	logInfo.append("Below is a list of site names not shown up in table")
	logInfo.append("Point of sale, number of occurance")
	logInfo.append("START_____________________________________SITE NAME, COUNT DISPLAY_____________________________________")
	for x in pos_dic:
		# if(pos_dic[x]==0):
			logInfo.append((x,pos_dic[x]))
	logInfo.append("END  _____________________________________SITE NAME, COUNT DISPLAY_____________________________________")
	logInfo.append("Validation Successfully Completed")

	logInfo.append("Validation process finished for " + filename + ". Ready to Upload")
