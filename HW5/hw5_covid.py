#bring in modules 
import os
import json
import requests

# list of states/territories
states = [
    'al', 'ar', 'as', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 
    'gu', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 
    'me', 'mi', 'mn', 'mo', 'mp', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 
    'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'pr', 'ri', 'sc', 
    'sd', 'tn', 'tx', 'ut', 'va', 'vi', 'vt', 'wa', 'wi', 'wv', 'wy']

# states = ['as']

#function mapping state abbreviations to full names
def state_name(state_abbr):
    state_names = {
        'al': 'Alabama', 'ar': 'Arkansas', 'as': 'American Samoa', 'az': 'Arizona', 'ca': 'California',
        'co': 'Colorado', 'ct': 'Connecticut', 'dc': 'District of Columbia', 'de': 'Delaware', 'fl': 'Florida',
        'ga': 'Georgia', 'gu': 'Guam', 'hi': 'Hawaii', 'ia': 'Iowa', 'id': 'Idaho', 'il': 'Illinois',
        'in': 'Indiana', 'ks': 'Kansas', 'ky': 'Kentucky', 'la': 'Louisiana', 'ma': 'Massachusetts',
        'md': 'Maryland', 'me': 'Maine', 'mi': 'Michigan', 'mn': 'Minnesota', 'mo': 'Missouri',
        'mp': 'Northern Mariana Islands', 'ms': 'Mississippi', 'mt': 'Montana', 'nc': 'North Carolina',
        'nd': 'North Dakota', 'ne': 'Nebraska', 'nh': 'New Hampshire', 'nj': 'New Jersey', 'nm': 'New Mexico',
        'nv': 'Nevada', 'ny': 'New York', 'oh': 'Ohio', 'ok': 'Oklahoma', 'or': 'Oregon', 'pa': 'Pennsylvania',
        'pr': 'Puerto Rico', 'ri': 'Rhode Island', 'sc': 'South Carolina', 'sd': 'South Dakota', 'tn': 'Tennessee',
        'tx': 'Texas', 'ut': 'Utah', 'va': 'Virginia', 'vi': 'Virgin Islands', 'vt': 'Vermont', 'wa': 'Washington',
        'wi': 'Wisconsin', 'wv': 'West Virginia', 'wy': 'Wyoming'}
    # Look up the state name based on the abbreviation
    state_name = state_names.get(state_abbr)
    return state_name

#function to format dates because I did it a few times
def format_date(unformatted_date):
    date_string = str(unformatted_date)
    if len(date_string) == 8:       #for full dates
        year = date_string[0:4]
        month = date_string[4:6]
        day = date_string[6:]
        formatted_date = month+"-"+day+"-"+year
    else:   #for finding months. If I do an if statement checking for a length of 6, it still works but it gives me errors
        year = date_string[0:4]
        month = date_string[4:6]
        formatted_date = month+"-"+year
    return formatted_date

#set keys that we need from the api
date_key = "date"
positive_increase_key = "positiveIncrease"

# Statement to start it off. Wasn't sure if it was needed for each state but didn't seem like it
print("Covid Confirmed Cases Statistics\n")
for state in states:
    
    #set url and create dictionary for state
    url = "https://api.covidtracking.com/v1/states/"+state+"/daily.json"
    req = requests.get(url)
    covid_tracking_dict = json.loads(req.text)
    
    #save state info to a json
    curr_dir = os.path.dirname(__file__)    #sets directory of file path
    file = open(curr_dir+"/"+state+".json", "w")
    file_path = os.path.join(curr_dir, state + ".json") #sets file path
    with open(file_path, "w") as file:
        json.dump(covid_tracking_dict, file)    #writes to file path
    
    
    #print state name
    print("State/Territory:", state_name(state))
    
    #find average new cases per day
    positive_increase_list = []
    for day in covid_tracking_dict:
        positive_increase_list.append(day[positive_increase_key])   #creates list of increases 
        sum_positive_increase = sum(positive_increase_list)         #finds average number from list 
        count_positive_increase = len(positive_increase_list)
        avg_positive_increase = sum_positive_increase/count_positive_increase
    print("Average new daily cases:", avg_positive_increase)
    
    #find date with highest number of new cases
    for day in covid_tracking_dict:
        highest_increase_amount = max(positive_increase_list)       #finds largest value from increase list
        if day[positive_increase_key] == highest_increase_amount:   #searches increase list for that value above
            highest_increase_day = day[date_key]
    print("Day with highest increase:", format_date(highest_increase_day))  
    
    #find most recent date with no new covid cases
    closest_zero_positive = ""    #sets base value
    for day in covid_tracking_dict:
        if day[positive_increase_key] == 0 and closest_zero_positive == "": #since it starts with the most recent, it finds the first date with a value of 0 increases
            closest_zero_positive = day[date_key]
    print("Most recent day with no increase:", format_date(closest_zero_positive))
    
    #find months with highest number of new cases and fewest
    month_total = {}
    highest_month_total = 0.0   #sets base values for each state
    highest_month = ""
    for day in covid_tracking_dict:
        year_month = str(day[date_key])[0:6]    #converts year_month to string to manipulate it
        if year_month in month_total:
            month_total[year_month] += day[positive_increase_key]   #if the year_month exitsts, add the value
        else:
            month_total[year_month] = day[positive_increase_key]    #if the year_month doesn't exist, add the first value
        for month, total in month_total.items():        #calculates most cases
            if total > highest_month_total:
                highest_month_total = total
                highest_month = month
        for month, total in month_total.items():        #calculates fewst cases
            lowest_month_total = highest_month_total
            if total < lowest_month_total:
                lowest_month_total = total
                lowest_month = month
    print("Month with most new cases:", format_date(highest_month))
    print("Month with least new cases:", format_date(lowest_month))
    print()
    

    
   