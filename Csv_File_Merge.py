import os
import fnmatch
import csv
import pandas as pd
InitFold = "U:\\DataWarehous\\Anita\\DOJ\\Firm_Overview_Txt_Extracted"
MaskedFold = "U:\DataWarehous\Anita\DOJ\Masked SRM Files"
ConcatFold= 'U:\\DataWarehous\\Anita\\DOJ\\Firm_Overview_txt_Concatenated\\'
OrigFold = 'U:\DataWarehous\Anita\DOJ\Original_Advisor_Firm_Files'
DestFold='U:\DataWarehous\Anita\DOJ\Advisor_Firm_Files_WithMasked\\'
df_mask = pd.DataFrame(columns=['#advisor_firm_id','eff_dt','firm_overview_txt'])

'''for year in ['2013','2014','2015','2016','2017','2018','2019','2020']:
    
    #if fnmatch.fnmatch(files,'advisor_firm_hist_ff_201*.csv'):
    for files in os.listdir(ConcatFold):
        file_start = "advisor_firm_hist_ff_"+ year +"_*.csv"
        #print(file_start)
        if fnmatch.fnmatch(files,file_start):
            file_path = ConcatFold +"\\"+ files
            dfs = pd.read_csv(file_path,index_col=None,encoding='iso-8859-1',low_memory=False)
            df_mask=df_mask.append(dfs,sort=False)
            #df_mask=df_mask.sort_values(by=['eff_dt'])
            print(files)
        else:
            continue
    fileDir=DestFold + "advisor_firm_hist_ff_masked_"+ year+".csv"
    df_mask.to_csv(fileDir,index=False)'''
    
#MaskFile=DestFold+"MaskFile_Consolidated.csv" 
#df_mask.to_csv(MaskFile,index=False)
for filename1 in os.listdir(OrigFold):
    if filename1.endswith(".csv"):
    #if fnmatch.fnmatch(filename1,"*2020____126.csv"):
    # print(os.path.join(directory, filename))
        filename=filename1
        file_path1 = OrigFold +"\\"+ filename1
        print(filename1)
        for year in ['2013','2014','2015','2016','2017','2018','2019','2020']:
    
            #if fnmatch.fnmatch(files,'advisor_firm_hist_ff_201*.csv'):
            for files in os.listdir(DestFold):
                file_start = "advisor_firm_hist_ff_masked_"+ year+".csv"
                #print(file_start)
                if fnmatch.fnmatch(files,file_start):
                    file_path = DestFold+ files
                    dfs = pd.read_csv(file_path,index_col=None,encoding='iso-8859-1',low_memory=False)
                    df_mask=df_mask.append(dfs,sort=False)
                    #df_mask=df_mask.sort_values(by=['eff_dt'])
                    print(files)
                
                    cols = pd.read_csv(file_path1, nrows=1).columns
                    #df_master=pd.DataFrame(columns=cols)
                    df = pd.read_csv(file_path1,index_col=None,usecols=cols,low_memory=False,encoding='iso-8859-1') 
                    #print(df['eff_dt'].max())
                    #print(df['eff_dt'].min())
                    #df_master=df_master.append(df,sort=False)
                    df_mask.reset_index(drop=True,inplace=True)
                    df.reset_index(drop=True,inplace=True)
                    #df = pd.concat([df,df_mask], axis=1, join='inner').reindex(df.index) # keys=['#advisor_firm_id','eff_dt'])
                    df=pd.merge(left=df,right=df_mask, how='left', left_on=['#advisor_firm_id','eff_dt'], right_on=['#advisor_firm_id','eff_dt'])
                    #df=df.iloc[2:]
                    #levels=None, names=None, verify_integrity=False, copy=True)
                    #print(df)
                        
                else:
                    continue
    else:
        continue

    df=df.drop('firm_overview_txt_x',axis=1)
    df=df.rename(columns={'firm_overview_txt_y':'firm_overview_txt'})
    FinalFile= DestFold + filename
    df.to_csv(FinalFile,index=False)


'''for filename1 in os.listdir(InitFold):
    #if filename1.endswith(".csv"):
    if fnmatch.fnmatch(filename1,"advisor_firm_hist_ff_2019_17.csv"):
         # print(os.path.join(directory, filename))
        file_path1 = InitFold +"\\"+ filename1
        print(file_path1)
        if filename1 in os.listdir(MaskedFold):
                file_path2 = MaskedFold +"\\"+ filename1
                print(file_path2)
                #df_mask = pd.read_csv(file_path2,index_col=None,usecols=['firm_overview_txt'],encoding='iso-8859-1')
                #print(df_mask)
                #df_init = pd.read_csv(file_path1,index_col=None,usecols=['#advisor_firm_id','eff_dt'],encoding='iso-8859-1')
                #print(df_init) 
                cols1 = pd.read_csv(file_path1, nrows=1).columns
                cols2 = pd.read_csv(file_path2, nrows=1).columns
                df_init = pd.read_csv(file_path1,index_col=None,usecols=cols1,encoding='iso-8859-1')
                print(df_init)
                df_mask = pd.read_csv(file_path2,index_col=None,usecols=cols2,encoding='iso-8859-1')
                print(df_mask) 
                df = pd.concat([df_init, df_mask], axis=1, sort=False)
                ConcatFile=ConcatFold+filename1
                df.to_csv(ConcatFile,index=False)
        else:
            print("Error, Masked file not found in the directory")
            break
        
    else:
        continue'''

