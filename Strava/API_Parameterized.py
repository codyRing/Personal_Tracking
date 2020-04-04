import requests
# import json
# import pandas as pd
# from datetime import timezone, datetime,date
# import pytz

CLIENT_ID = "45065"
CLIENT_SECRET = "83bfe2f4fbc733420f28229112c7b2406b2ccedd"
REDIRECT_URI = 'http://localhost'
AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.strava.com/oauth/token"
Scope = "activity:read_all"

auth = requests.get('{}?response_type=code&client_id={}&redirect_uri={}'.format(AUTHORIZE_URL, CLIENT_ID, REDIRECT_URI))



print(auth.text)

