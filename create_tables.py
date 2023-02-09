#!pip install numpy, pandas
import numpy as np 
import pandas as pd
from datetime import datetime as dt, timedelta
import re

def convert_to_24H(x): #function replaces a given string of format 11 am to a form 11:00
    l = x.split(' ')
    x = l[0]
    
    #Convert the given string into datetime object
    try:
        x = dt.strptime(x, "%H:%M")
    except Exception: x = dt.strptime(x, "%H")
    
    if (l[-1] == 'am'):
        if x.hour==12:
            x += timedelta(hours = 12) #add 12 hours if the given time is 12 am to convert to 24:00
    elif (l[-1] == 'pm'):
        if x.hour!=12:
            x += timedelta(hours=12) #add 12 hours if the given time is 1 pm to 11 pm to convert into 24H format
    #else: print("Invalid Values, opening time can't be greater than closing time")
    
    return l, x, x.strftime("%H:%M")

def convert_to_24H_list(x): #function replaces a given string of format 11 am to 8 pm to a list of times like [11:00, 12:00,..]
    l = x.split(' - ')
    start, st, _ = convert_to_24H(l[0]) #starting of the range
    end, ed, _ = convert_to_24H(l[-1])#end of the range
    
    if (start[-1] == 'am') and (end[-1] == 'am'):
        if ed.hour==0:
            ed -= timedelta(minutes=1)
        elif ed.hour<st.hour:
            ed += timedelta(days=1)
    elif (start[-1] == 'pm') and (end[-1] == 'pm'):
        if st.hour!=12:
            st = st + timedelta(hours=12)
    elif (start[-1] == 'pm') and (end[-1] == 'am'):
        if ed.hour==0:
            ed -= timedelta(minutes=1)
        else:
            ed += timedelta(days=1)
    return [(st + timedelta(minutes=(x*30))).strftime("%H:%M") for x in range((((ed-st)/3600).seconds+1)*2) if (st + timedelta(minutes=(x*30)))<=ed]

def form_schedule(df: pd.DataFrame)->pd.DataFrame:
    
    #Assigning interpretable names to columns
    df.rename(columns = {0:'restaurants', 1: 'open_timings'}, inplace=True)
    
    #restructuring the dataframe in lexicographical order of restaurants and adding restaurant ids
    df.sort_values(by = 'restaurants', ignore_index=True, inplace=True)
    df['rest_id'] = df.index+1
    
    #Forming restaurants dimension table for ease of access
    restaurants = df[['rest_id', 'restaurants']].rename(columns = {'restaurants': 'rest_name'})
    
    #Extract weekdays and 
    df['weekdays'] = df['open_timings'].apply(lambda x: re.findall('(\w{3}\-*\w*)', x))
    df['timings'] = df['open_timings'].apply(lambda x: re.findall('(\d+:*\d* \w+ -* \d+:*\d* \w+)', x))
    
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    def replace_range(x): #function replaces a given string of format Mon-Thu to a list of weekdays [Mon, Tue, Wed, Thu]
        if '-' in x:
            l = x.split('-')
            start = weekdays.index(l[0])
            end = weekdays.index(l[-1])
            temp = []
            temp = [weekdays[i] for i in range(start,end+1,1)]
            return temp
    
    def collect_days(x): #function collects the days in a list of lists based on ranges or individual days 
        days = []
        for i, day in enumerate(x):
            if '-' in day:
                try: 
                    if len(days[i-1])==1:
                        days[i-1]+=replace_range(day)
                    else: days.append(replace_range(day))
                except Exception:
                    days.append(replace_range(day))
            elif (i>0 and i<(len(x)-1) and ('-' in x[i-1]) and ('-' in x[i+1])): 
                days[i-1] += [day]
            else: 
                days.append([day])
        return days
    
    df.weekdays = df.weekdays.apply(lambda x: collect_days(x))
    df.drop(columns = 'open_timings', inplace=True)
    
    df = df.explode(column = ['weekdays', 'timings']) #initial explode for converting list of lists to lists
    df.timings = df.timings.apply(lambda x: convert_to_24H_list(x)) #extract time ranges from strings
    t = df.explode(column = 'weekdays').explode(column='timings') #explode list of days and times for individual values
    t = t.groupby(['timings', 'weekdays'], as_index=False).agg({'rest_id': set}) #groupby times and weeks to collect list of restaurants based on group
    schedule = t.pivot(columns='weekdays', index='timings', values='rest_id') #form schedule data set showing open restaurants based on time and day
    
    return restaurants, schedule

if __name__ == '__main__':
    
    filename = 'restaraunts-opening-hour.xlsx'
    df = pd.read_excel(filename, header=None).rename(columns = {0:'restaurants', 1: 'open_timings'})

    #extract the restaurants table and schedules from the given data into 2 dataframes
    restaurants, schedule = form_schedule(df.copy()) 

    restaurants.to_csv('restaurants.csv')
    schedule.to_csv('schedule.csv')