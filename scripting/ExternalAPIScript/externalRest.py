#initialized as null
#Response Body is what will return after the rest call
responseBody=""
#grab ticketid
sr = request.getQueryParam("id")

#basic imports
from psdi.mbo import MboConstants
from psdi.server import MXServer  
currentDate = MXServer.getMXServer().getDate()
# set user
mxServer = MXServer.getMXServer()
userInfo = mxServer.getUserInfo("maxadmin")

# Get SR
newlocSet = MXServer.getMXServer().getMboSet("SR", userInfo)
newlocSet.setQbe("TICKETID", "="+str(sr))
if not newlocSet.isEmpty():
    #newlocSet.reset()
    response=int(request.getQueryParam("response"))
    SR=newlocSet.getMbo(0)
    ticketspec=SR.getMboSet("SRSPECCLASS")
    ticketspec.setFlag(MboConstants.DISCARDABLE, True)
    originaldesc=SR.getString("DESCRIPTION_LONGDESCRIPTION")
    #basic response for all SR's
    basicresponse="""\n\nTicketID: """+SR.getString("TICKETID")+"""
        \nDescription of Service Request: """+SR.getString("Description")+"""\n\nReported By: """+SR.getString("REPORTEDBY")+"""
        \nReported on: """+str(SR.getDate("REPORTDATE"))
        
    approvedresponse=""
    classificationset=SR.getMboSet("CLASSSTRUCTURE")
    classificationset.setFlag(MboConstants.DISCARDABLE, True)
    if not classificationset.isEmpty():
       for i in range(0,ticketspec.count()):
            if not ticketspec.getMbo(i).isNull("NUMVALUE") and not ticketspec.getMbo(i).isNull("ALNVALUE"):
                approvedresponse=approvedresponse+"""\n\n"""+ticketspec.getMbo(i).getString("ASSETATTRID")+""": """+ticketspec.getMbo(i).getString("ALNVALUE")+" Value: "+str(ticketspec.getMbo(i).getDouble("NUMVALUE"))
            elif not ticketspec.getMbo(i).isNull("NUMVALUE") and ticketspec.getMbo(i).isNull("ALNVALUE"):
                approvedresponse=approvedresponse+"""\n\n"""+ticketspec.getMbo(i).getString("ASSETATTRID")+""": """+str(ticketspec.getMbo(i).getDouble("NUMVALUE"))
            elif ticketspec.getMbo(i).isNull("NUMVALUE") and not ticketspec.getMbo(i).isNull("ALNVALUE"):
                approvedresponse=approvedresponse+"""\n\n"""+ticketspec.getMbo(i).getString("ASSETATTRID")+""": """+ticketspec.getMbo(i).getString("ALNVALUE") 
    
    #This is the main driver for the script.
    #I could likely refactor to not repeat myself, but I find this easier to read
    if SR.getString("STATUS")=="WAPPR":
        if response==1: #if approved
            
            SR.setValue("DESCRIPTION_LONGDESCRIPTION",originaldesc+"""\n\n Client Host: """+str(request.getClientHost())+"""\n\n Client Address: """+str(request.getClientAddr())+""" Tenant Code: """+str(request.getRequestTenantCode())+
            """ Rest Session: """+str(request.getRESTSession())+""" MXSession: """+str(request.getMXSession())+""" Get For User: """+str(request.getForUser())+""" Header Params: """+str(request.getHeaderParams()))
            #Very basic example but just shows the flexibility
            SR.changeStatus("APPR", currentDate, str(request.getClientAddr()), MboConstants.NOACCESSCHECK)
            responseBody="""Service Request Accounting Approved."""+basicresponse+approvedresponse
        elif response==0:
            SR.setValue("DESCRIPTION_LONGDESCRIPTION", originaldesc+"""\n\n Client Host: """+str(request.getClientHost())+"""\n\n Client Address: """+str(request.getClientAddr())+""" Tenant Code: """+str(request.getRequestTenantCode())+
            """ Rest Session: """+str(request.getRESTSession())+""" MXSession: """+str(request.getMXSession())+""" Get For User: """+str(request.getForUser())+""" Header Params: """+str(request.getHeaderParams()))
            SR.changeStatus("CANCELLED", currentDate,str(request.getClientAddr()), MboConstants.NOACCESSCHECK)
            responseBody="Service Request Cancelled"+basicresponse
    else:
        responseBody="Status cannot be changed on this Service Request"
        #TODO: Could probably flesh out handling of different statuses and be more descriptive here - I leave that to you!
    newlocSet.save()
newlocSet.close()
newlocSet.cleanup()    