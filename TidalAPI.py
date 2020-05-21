import getpass as pas
import base64 as b64
import requests as req
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
class Tidal:
    def __init__(self,Url,*Param):
        #self.userid = UserId
        #self.password = Password
        self.url = Url
        paramCnt = len(Param)
        if  paramCnt==2:
            self.parName = Param[0]
            self.parDate = Param[1]
        else:
            Print('Pass the parmeters correctly')
    
    def GetResult(self):
        
        # Construct GET URL with appended parameters:
        lv_url = self.url + 'JobRun.getList?query=(parentname LIKE \'%' + self.parName + '%\' AND productiondateasstring LIKE \'' + self.parDate + '%\')'
        #+ '%\' AND duration> \'' + str(7200) + '\')'
        print(lv_url)
        # Set URL encoding:
        lv_url = lv_url.encode('ISO-8859-1')
    # Get Authorization/Authentication credentials from user:
        lv_user = input('Enter TIDAL User Name:')
        lv_pswd = pas.getpass('Enter TIDAL Password:')
        lv_userAndPass = bytes(lv_user + ":" + lv_paswd, 'utf-8')
        lv_userAndPass = b64.b64encode(lv_userAndPass).decode("ascii")
        # Set Content-Type in HTTP Request header:
        lv_headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Authorization' : 'Basic %s' % lv_userAndPass }
 
        # Submit HTTP GET to Tidal TES Rest API URL; timeout after a minute:
        try:
            lv_response = req.get(lv_url,headers=lv_headers,timeout=60)
            print('******************')
            print('code:' + str(lv_response.status_code))
            print('headers:' + str(lv_response.headers))
            print('******************') 
            lv_response.raise_for_status()
            lv_http_rc = lv_response.status_code
            lv_http_resp = lv_response.content
        except req.exceptions.HTTPError as errh:
            print('http error:' + errh)
 
    # Evaluate HTTP Response code:
        if lv_http_rc >= 500:
            print("There are some server errors")
        elif lv_http_rc == 200:
            lv_http_resp = 'SUCCESS'.format(lv_http_rc)
            print("\nResponse Content(text):\n " + lv_http_resp)
            with open('tidalResp.xml','wb') as f:
                f.write(lv_response.content)
            #lv_root = ET.fromstring(lv_response.content)
            lv_root = ET.parse('tidalResp.xml')
            root = lv_root.getroot()
            tmp_dict = {}
            attr_list = []
            xlist=[]
            lv_ns = {'rootxml':'http://purl.org/atom/ns#','my_jobrun': 'http://www.tidalsoftware.com/client/tesservlet'}
            for root_jobrun in lv_root.findall('rootxml:entry', lv_ns):
                root_name = root_jobrun.find('rootxml:id', lv_ns)
                #print(root_name.text)
                for lv_jobrun in root_jobrun.findall('my_jobrun:jobrun',lv_ns):
                    lv_name = lv_jobrun.find('my_jobrun:name', lv_ns)
                    lv_id = lv_jobrun.find('my_jobrun:id', lv_ns)
                    lv_parentid = lv_jobrun.find('my_jobrun:parentid', lv_ns)
                    lv_parent_name = lv_jobrun.find('my_jobrun:parentname', lv_ns)
                    lv_duration = lv_jobrun.find('my_jobrun:duration', lv_ns)
                    lv_statusname = lv_jobrun.find('my_jobrun:statusname',lv_ns)
                    tmp_dict['id'] = lv_id.text
                    tmp_dict['jobname'] = lv_name.text
                    tmp_dict['parentid'] = lv_parentid.text
                    #tmp_dict['parentname'] = lv_parent_name.text
                    tmp_dict['parentname'] = lv_parent_name.text
                    tmp_dict['statusname'] = lv_statusname.text
                    tmp_dict['duration'] = lv_duration.text
                    #print(tmp_dict)
                    attr_list.append(tmp_dict.copy())
            #print(attr_list)
            #print(attr_dict)
            df = pd.DataFrame(attr_list)
            #id_name_dict = dict(zip(df.id,df.jobname))
            #parent_dict = dict(zip(df.id,df.parentid))
            child_dict = dict(zip(df.parentid,df.id))
            def find_child(x):
                jobid = child_dict.get(x,None)
                #print(jobid)
                if jobid is None:
                    return "No"
                else:
                    return "Yes" 
            """def find_parent(x):
                value = parent_dict.get(x, None)
                if value is None:
                    return ""
                else:
                    # Incase there is a id without name.
                    if id_name_dict.get(value, None) is None:
                        return "" + find_parent(value)
                    return str(id_name_dict.get(value)) +", "+ find_parent(value)"""
            #df['Parent_Hierarchy'] = df.id.apply(lambda x: find_parent(x)).str.rstrip(', ')
            df['DoesHasChild'] = df.id.apply(lambda x: find_child(x))
            #xlist.append(df.id.apply(lambda x: find_parent(x)
            df = df[df.DoesHasChild == 'No']
            df = df[~df.jobname.str.contains('end batch|end_batch|endbatch|start batch|start_batch|startbatch',case=False,na=False,regex=True)]
            df = df.drop(['DoesHasChild'],axis=1)
            df_completed = df[df.statusname == 'Completed Normally']
            df_Failed = df[df.statusname == 'Completed AbNormally']
            df1 = df_completed[['id','duration']].apply(pd.to_numeric)
            df_completed = df_completed.sort_values(by= ['parentname','jobname'])
            #df_completed = df_completed[df_completed.duration.apply(pd.to_numeric)>1200]
            #df1 = (df[df['Parent_Hierarchy'] != ''])
            #df1 = df1.set_index('Parent_Hierarchy')
            #df1 = df1.drop(['parentid'],axis=1)
            print(df_completed)
            #df1 =pd.DataFrame(lst)
            #print(df2)
            df_completed.to_csv("Tidal_Report_Duration_PROD_Completed.csv")
            #df_completed.to_html("Tidal_Report_Duration_PROD_Completed.html")
            #df_Failed.to_html("Tidal_Report_Duration_PROD_Failed.html")
            df1.plot(x ='id',y='duration',kind='scatter',title="Duration of Tidal Jobs")
            plt.show()
            
if __name__ == '__main__':
    #APIInputs= Tidal('tidal url','jobname','20200106')
    APIInputs= Tidal('tidal url','jobname','20200415')
    print(APIInputs.parName)
    APIInputs.GetResult()

