import numpy as np 
import pandas as pd
from datetime import datetime as dt, timedelta
from tabulate import tabulate
import re
from create_tables import convert_to_24H


restaurants = pd.read_csv('restaurants.csv')
schedule = pd.read_csv('schedule.csv', index_col = 'timings')

def output_list_of_restaurants(weekday, time, rest=restaurants.copy(), schedule=schedule.copy()):

    _, _, time = convert_to_24H(time) #convert the input time to 24H format
    
    weekdays = {'Monday': 'Mon', 'Tuesday':'Tue', 'Wednesday':'Wed', 'Thursday':'Thu', 'Friday':'Fri', 'Saturday':'Sat', 'Sunday':'Sun'}
    weekday = weekday.title()
    if weekday not in schedule.columns:
        if weekday in weekdays.keys():
            weekday = weekdays[weekday] #replace given weekday string format, with the values inside the schedule table
    
    def get_listed_time(tm):

        for i, tim in enumerate(schedule.index):
 
            if tim>tm:
                return schedule.index[i-1] #if the time is lesser than a certain time, the time before that is chosen to pick the restaurants
                
            elif tim==tm:
                return tim
                
    
    rest1 = rest.set_index('rest_id')['rest_name'].to_dict()
    
    if time not in schedule.index:
        time = get_listed_time(time) 
    
    try:
        rest_ = list(schedule.loc[time, weekday])
        result = pd.Series(rest_).map(rest1) #replace restaurant ids with restaurant names
        headers = ['Restaurant-ID', 'Restaurant-Name']
        #print open restaurants with their ids in a table format
        #print(tabulate(list(zip(rest_, result.values)), headers = headers, tablefmt = 'psql')) 
        return list(rest_)
    except Exception:
        return 'No Restaurants Open on the given day and time'

def take_input(day_time):
    print('Please Input the weekday and time in the same order, separated by a comma:')
    #day_time = input().strip()
    print('Open Restaurants are: ')
    l = day_time.split(',')
    weekday = l[0].strip()
    time = l[1].strip()
    output_list_of_restaurants(weekday, time)


if __name__ == '__main__':

    take_input()


