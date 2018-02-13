# ede_marginfile_validation_python


Python script file is created to validate the margin file data quality as requested. Please refer to the version number before download.

Github Links:
https://ewegithub.sb.karmalab.net/EWE/ede_marginfile_validation_python

Environment Configuration:
Please follow the following tutorial to install Panda Package
https://pandas.pydata.org/pandas-docs/stable/install.html

Python Version: 2.7


Resources:
Python Panda Case Usage
https://pandas.pydata.org/pandas-docs/stable/10min.html
 
Margin File Concepts Explanation:
https://confluence/pages/viewpage.action?pageId=530449285#Rules/Standards/FormatforMargin1.0and3.0files-MarginFileValidationPythonProgram
 
To Run:
Margin File 3.0:
-Open Terminal/Command Lind
-cd MarginFile3.0
-python vali_margin_3.0.py filename_csv_format.csv
eg. python vali_margin_3.0.py ../DataFile/sample3.0.csv
 
Margin File 1.0:
-Open Terminal/Command Lind
-cd MarginFile1.0
-python vali_margin_1.0.py filename_csv_format.csv
eg. python vali_margin_1.0.py ../DataFile/sample1.0.csv


Clarification:
File Structure
	-DataFile : Store the .csv data file ready for validation
		-eg. Sample3.0.txt
	-LibraryFile: Store the general library file ready to be loaded into the program
		-eg. pos.txt    

Usage:
	-Updating the library 
		-to update/add new point of sales into the variables.
		arun on Teradata:
			select
			OREPLACE(SITE_NAME,'.',' ') as SITE_NAME
			from P_ADS_BEX_COMMON.DM_OMNITURE_SITE
 
		b.Save the output result to .txt format.
		c.Store at the LibraryFile Location.
		d.Rename the file as pos.txt and delete the original one
	-Run the validation process on file
		



Idea Log Result:

Margin File 3.0 Output Log Example:
Load file successfully
Start to validate the column
YEAR Column Format Validated Successfully
MONTH Column Format Validated Successfully
POS Column Format Validated Successfully
PKG_SA Column Format Validated Successfully
MER_AGN Column Format Validated Successfully
LOB Column Format Validated Successfully
ONLINE_OFFLN_IND Column Format Validated Successfully
REV_ADJ_FACTR_% Column Format Validated Successfully
COS_ADJ_FACTR_% Column Format Validated Successfully
VCOS_ADJ_FACTR_% Column Format Validated Successfully
Validation Successfully Completed
Validation process finished for ETLDM_MARGIN_ADJ_FACTR.csv. Ready to Upload


Margin File 1.0 Output Log Example:
Initialize the validation process
Start to Load the margin 1.0 file
Load file successfully
Start to validate the column
Account Column Format Validated Successfully
 Point of Sale Column Format Validated Successfully
 Business Type Column Format Validated Successfully
Product Column Format Validated Successfully
Validation Successfully Completed
Validation process finished for Rev_GP_by_POS_FY16_201612.csv. Ready to Upload
