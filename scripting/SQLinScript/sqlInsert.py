from psdi.server import MXServer
from java.text import SimpleDateFormat
mxServer = MXServer.getMXServer()
userInfo = mxServer.getUserInfo("maxadmin")

custset=MXServer.getMXServer().getMboSet("CUST_OBJ", userInfo) #MboSet of custom object that will write into interface tables
custset.setWhere("PROCESSED=0") #Example field that could be added to indicate whether or not mbo has been processed yet
if not expset.isEmpty(): #Important to verify so no runtime errors occur
	for i in range(0, custset.count()):
		custobjs=custset.getMbo(i)
		currentDate = MXServer.getMXServer().getDate()
		sdf = SimpleDateFormat("yyMMddHHmmssSSS") #I find this a useful way to guarantee uniqueness when writing these statements on interface tables
		
		curdatecomb=str(sdf.format(currentDate))
		custfield1=custobjs.getString("Field_1String")
		custfield2-custobjs.getInt("Field_2Integer")
		custfield3=custobjs.getDouble("Field_3Double")

		conKey = ""
		dbconnect = ""
		statexec = ""
		
		if custfield1=="Invoices"

			try: #You could probably make this a function if they do not differ much in what gets added, but sometimes manually specifying follows KISS principles better

				conKey = custset.getUserInfo().getConnectionKey(); #Grab connection key from mboset to connect to database
				dbconnect = custset.getMboServer().getDBConnection(conKey) #Connect to database with key
				statexec = dbconnect.createStatement() #Create a sql statement with connection key


				loc="INSERT INTO CUST_INTERFACE1(TRANSID, TRANSSEQ, DIFF_FIELD1, DIFF_FIELD2, DIFF_FIELD3) \
					 Values("+curdatecomb+", 1, '"+custfield1+"',"+custfield2+","+custfield3");"

				rs = statexec.execute(loc)
				dbconnect.commit()

			finally:
				if statexec != "":
					statexec.close()
				if conKey != "" and dbconnect != "":
					custset.getMboServer().freeDBConnection(conKey)
					
		elif custfield1=="PurchaseReqs": 
			#This makes the statement more narrow on the band it will insert with. Can be replaced with an else statement if certain all data types will work like this
			#Can also expand this to many more interface tables if necessary
			
			prset=MXServer.getMXServer().getMboSet("PR", userInfo)
			prset.setWhere("PRNUM= 'PR"+str(custfield2)+"'")#Hypothetical example of what is possible
			
			vendornum=prset.getMbo(0).getString("VENDOR")
			
			try:

				conKey = prset.getUserInfo().getConnectionKey(); #Grab connection key from mboset to connect to database
				dbconnect = prset.getMboServer().getDBConnection(conKey) #Connect to database with key
				statexec = dbconnect.createStatement() #Create a sql statement with connection key


				loc="INSERT INTO CUST_INTERFACE2(TRANSID, TRANSSEQ, DIFF_FIELD1, DIFF_FIELD2, DIFF_FIELD3, SHEET_ID, SHEET_NAME) \
					 Values("+curdatecomb+", 1, '"+custfield1+"',"+custfield2+","+custfield3",'"+sheetid+"','"+sheetnam+"');"

				rs = statexec.execute(loc)
				dbconnect.commit()

			finally:
				if statexec != "":
					statexec.close()
				if conKey != "" and dbconnect != "":
					prset.getMboServer().freeDBConnection(conKey)
					
			prset.reset()
			prset.close()
			prset.cleanup()
			
		custobjs.setValue("PROCESSED",1, MboConstants.NOACCESSCHECK | MboConstants.NOACTION | MboConstants.NOVALIDATION)
		
	custset.save()
custset.reset()
custset.cleanup()