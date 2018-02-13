
from MarginFile3_0 import vali_margin_3_0
from MarginFile1_0 import vali_margin_1_0
from LibraryFile import connectTD




def validateMarginFileProcess(filename,versionNumber):
	connectTD.connectTD()
	if(versionNumber == 3):
		print "Start to trigger validateMarginFile_v3 func"
		vali_margin_3_0.validateMarginFile_v3(filename)
	if(versionNumber == 1):
		print "Start to trigger validateMarginFile_v1 func"
		vali_margin_1_0.validateMarginFile_v1(filename)