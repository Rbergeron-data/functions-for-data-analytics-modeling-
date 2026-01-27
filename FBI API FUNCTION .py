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

## Data retrieved via API
## Data Information: https://le.fbi.gov/informational-tools/ucr/ucr-technical-specifications-user-manuals-and-data-tools#Use-of-Force
## relevant: https://www.king5.com/article/news/local/seattle/seattle-capitol-hill-organized-protest-five-years-later/281-a1bc7480-823a-4194-a841-c713671a470e#:~:text=SEATTLE,social%20justice%20uprising%20of%202020.




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
        return None, None
    else:
        print(f"\n Request Failed, responseCode: {response.status_code}")
        return None, None

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
#%% Create a loop function to pull multiple years
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




#%% HERE DOWN IS ACTUAL RESEARCH

## create initial dictionary, see?
see = {"year": 2020,
       "quarter": 4}

initially = initialize_FBI_API(base= "https://api.usa.gov/crime/fbi/cde/", path= "uof/reports/{grp}/{spec}", 
                               params= see, PersonalKey= "62zuB2YwdHcXfd4IELlMd8TKLcs8g6Mhpe1VaNkJ")
multi = MultiYearPull(initially[1], 2019, 2024)

#%% explore
## group by year
month_agg = multi.groupby(by= ['month_number']).agg(
    submitting_inc_Mean= ('submitting_inc', 'mean'),
    not_submitting_Mean= ('not_submitting', 'mean')).reset_index()
#%% explore more
year_agg = multi.groupby(by= ['data_year']).agg(
    submitting_inc_Mean= ('submitting_inc', 'mean'),
    not_submitting_Mean= ('not_submitting', 'mean')).reset_index()
#%%
import seaborn as sns
import matplotlib as plt
#%% plot the years
sns.set_theme(style= 'whitegrid')

bar = sns.barplot(data= multi,
                  x= 'month_number',
                  y= 'not_submitting',
                  hue= 'data_year') 
#%%
sns.set_theme(style='whitegrid')
bar_avg_by_month = sns.barplot(data= year_agg,
                               x= 'data_year',
                               y= 'submitting_inc_Mean')
#%%
bar_avg_by_year = sns.barplot(data= month_agg,
                               x= 'month_number',
                               y= 'submitting_inc_Mean')
#%%
bar_avg_by_month_no = sns.barplot(data= month_agg,
                               x= 'month_number',
                               y= 'not_submitting_Mean')
#%%
bar_avg_by_year_no = sns.barplot(data= year_agg,
                               x= 'data_year',
                               y= 'not_submitting_Mean')
#%%
import seaborn.objects as so
#%% stack some graphs

bar_line_month = (
    so.Plot(data= month_agg,
            x= 'month_number')
    .scale(y= so.Continuous(),
           y2= so.Continuous())
    .add(so.Bar(), so.Dodge(), y= 'submitting_inc_Mean')
    .add(so.Line(),  y= 'not_submitting_Mean')
    .add(so.Line(), y= 'not_submitting_Mean', yaxis= "y2" )
    .label(title= 'FBI Use of Force reports',
           x= 'Month',
           y= 'Average Incidents',
           y2= 'Average Not Reporting')
)

bar_line_month.show()
#%%
##first initialize
fig, ax = plt.pyplot.subplots(layout= 'constrained')
ax.bar(year_agg['data_year'], year_agg['submitting_inc_Mean'], label= 'Incidents', color='blue')
ax.grid(False)
ax.set_ylabel('Average Incidents per Month', color= 'blue')
secax = ax.twinx()
secax.plot(year_agg['data_year'] , year_agg['not_submitting_Mean'], label= 'NonReports', color= 'red')
secax.set_ylabel('Average NonReports per Month', color='red')
secax.grid(False)
fig.suptitle("FBI Use of Force Reporting: (WA state)")

plt.show()

## Reminder that not all trends should be trusted at face value. 

