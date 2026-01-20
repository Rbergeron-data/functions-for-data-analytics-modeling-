#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 14:30:37 2026

@author: renebergeron
"""



## 1. setup base info:
MyKey= "62zuB2YwdHcXfd4IELlMd8TKLcs8g6Mhpe1VaNkJ"

##**
base = "https://api.usa.gov/crime/fbi/cde/"





#%% Creating a function contd from first attempt and now to refine into functional format
## this function is to aid in the building of FBI database retrieval, it is a work in progress, so be nice

 ##
import regex as re
import requests
import pandas as pd

def initialize_FBI_API(base, path, params, PersonalKey):   
    ##** Read me:
        ## This will initialize a list that is needed later for multiyear pulls along with pull your first dataframe (verifying the connection)
        ## base: server URL; str
        ## path: extension path; str
        ## params: parameters to pass to API; must be dictionary format
        ## PersonalKey: your personal API Key; str
    ##
    df = None
    
    ext_var_qs = re.findall(r'\{(.*?)\}', path)
    ext_var_rs=[]
    for x in ext_var_qs:
        peace = input(f"Enter {x}:")
        ext_var_rs.append(f"{peace}")
    path_ext = '/'.join(ext_var_rs)
    path_base = path.split("{")[0]
    fullPath = f"{path_base}{path_ext}"
    
    fullURL = f"{base}{fullPath}"
    header = {'X-Api-Key': PersonalKey}
    
    response = requests.get(fullURL, params=params, headers=header)
    if response.status_code == 200:
        print("\n Successful!")
        loc_data = response.json()
    elif response.status_code == 503:
        print("\n FBI Server Currently Overloaded, Try Again Later")
    else:
        print(f"\n Request Failed, responseCode: {response.status_code}")

    df = pd.DataFrame(loc_data)
    url = response.url
    url = url.split("?")[0]
    lyst_API = [df,
                params,
                header,
                PersonalKey,
                url]
    
    return df, lyst_API

#%% creating a simpler but more in depth input function to pull api from results of FBI_API_REQUEST
import requests
import pandas as pd

def FBI_API_short(URL, params, header):
    response = requests.get(URL, params=params, headers=header)
    
    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        print("\n SUCCESS!")
    elif response.status_code == 503:
        print("\n Server busy, try again later.")
    else:
        print(f"\n Fail- \n Error: {response.status_code}")
    return data
#%% Create a loop function to pull and append DF
##
import pandas as pd

def MultiYearPull(lyst_API,start,end):
    ##** this is the read me of sorts:
    ## lyst_API: resultant list from the initialization function; list
    ## start: start year; int
    ## end: end year; int
    
    df_lyst = []
    if "year" in lyst_API[1]:
        params = lyst_API[1].copy()
        for x in range(start, end+1):
            params['year'] = x
            df = FBI_API_short(lyst_API[4], params=params, header=lyst_API[2])
            df_lyst.append(df)
    else:
        print("\n Fail! \nThis request cannot be pulled")
        
    if df_lyst:
        return pd.concat(df_lyst, ignore_index=True)
    return pd.DataFrame()