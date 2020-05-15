import requests
import json
import pandas as pd
# activities_url = 'https://www.strava.com/api/v3/athlete/activities?access_token=c6b3bbbe6161c78cb491343620fbbc7d502cd4bb'
limit_Date = '2020-01-01'
activities_url = 'https://www.strava.com/api/v3/athlete/activities'
header = {'Authorization':'Bearer a8875754446e59f79460f039a77e21c7547b3804'}
param  = {'start_date_local' : limit_Date}

my_dataset = requests.get(activities_url,headers=header,params=param) #.json()
# y=json.load(my_dataset)

print(my_dataset.keys())
# for x in range(len(my_dataset)):
#      print(my_dataset[x]['id'],my_dataset[x]['name'])


# print(len(my_dataset))

