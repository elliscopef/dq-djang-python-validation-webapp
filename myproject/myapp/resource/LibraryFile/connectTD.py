import teradata

import ConfigParser
import io
from .. import varSettings





configfile_name = "udaexec.ini"


def connectTD():
	print "Attempt to connect to TDPRO Database"
	print "************************************"
	print varSettings.td_configfile_name

	with open(varSettings.td_configfile_name) as f:
		file_config = f.read()
#read credential file prior to the connecting
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	config.readfp(io.BytesIO(file_config))
	udaExec = teradata.UdaExec(appName="ConnectTDDEV",version="2",odbcLibPath="/opt/unixodbc-2.3.4-0/share/man/man1/odbcinst.1")

	fh = open(varSettings.pos_txt_file_path, "w")

	with udaExec.connect(method=config.get('DEFAULT', 'method'), system=config.get('TDDEV', 'system'),username=config.get('TDDEV', 'username'), password=config.get('TDDEV', 'password')) as session:
		for row in session.execute("select OREPLACE(SITE_NAME,'.',' ') as SITE_NAME from D_ADS_BEX_COMMON.DM_OMNITURE_SITE"):
#Write the point of sale to file
			fh.write(str(row[0]+"\n"))
	print "File Writing completes. The pox.txt is updated with the latest data from database"
	fh.close()
