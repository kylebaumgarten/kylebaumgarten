import json, requests, zipfile, io, os
maximourl=os.getenv('maxurl')
maximoos=os.getenv('mobileobjstruc')
persongroup=os.getenv('currpersongroup')
apikey=os.getenv('maxapi')
home=os.getenv('HOME')
def request_active_id():
    r=requests.get(maximourl+"maximo/api/os/"+maximoos+"?oslc.select=MOBILEDBID&oslc.where=persongroup%3D%22"+persongroup+"%22%20and%20status%3D%22ACTIVE%22&lean=1", headers={"apikey":apikey})
    response=r.json()
    return response

def parse_json(r):
    id:int=0
    for i in r['member']:
        id=i["mobiledbid"]
    return id
    
def download_mobiledb(id):
    url=maximourl+"maximo/api/graphite/mobile/db?mobileDbId="+str(id)
    r=requests.get(url, headers={"apikey":apikey}, stream=True)
    z=zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(home+"/mobiledb/")

if __name__=="__main__":
    json=request_active_id()
    value=parse_json(json)
    if value:
        downloaded=download_mobiledb(value)
