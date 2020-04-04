import requests
import json
import pandas as pd
from datetime import timezone, datetime,date
import pytz
CLIENT_ID = "45065"
CLIENT_SECRET = "83bfe2f4fbc733420f28229112c7b2406b2ccedd"
REDIRECT_URI = 'http://localhost'
AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.strava.com/oauth/token"
Scope = "activity:read_all"

#Making this URL in postman currently
res =requests.get('https://www.strava.com/api/v3/activities?per_page=200&access_token=8f5e84194f120fa7ee94fb6f857774f32880f49e')
var = json.loads(res.text)

pac = pytz.timezone('America/Los_Angeles')
utc = pytz.timezone('UTC')


with open('../Data/Strava/strava_activitities.txt', 'w') as outfile:
      json.dump(var,outfile)

df = pd.read_json(res.text)
df['start_date']=pd.to_datetime(df.start_date)
df = df.set_index('start_date')
df.to_csv('../data/Strava/Strava_Results.csv',)


# #df.tz_convert(pac)
#
# df['hour']= df.index.strftime('%H')
#
# data = df[['hour','distance','moving_time']]
#
# data.to_csv('./data/results.csv')
#
# #df = df.tz_convert(pac)
#
# #print(df[['distance','moving_time']])


