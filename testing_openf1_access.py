#!/usr/bin/env python

# 01082025 - testing OpenF1 API
# So here this project requires access to the speeds, obtaining the average from the ##top three speeds## (p1, p2, p3) of the track from the ##past two years##
from datetime import datetime
from urllib.request import urlopen
import json

#response = urlopen('https://api.openf1.org/v1/session_result?session_key=latest')
#data = json.loads(response.read().decode('utf-8'))
#print(data)




# firstly we need the meetings API (give us the country_name, meeting_name, location (which can be used for OPEN METEO), and meeting_key (can be used to find NEXT block of information) AND number_of_laps (use on the laps API)
# secondly we need the top three racers for the most recent two years (6 racers) --> we want session_result API (driver_number, position, session_key, meeting_key)
# to get the 'Race' session_key for the meeting_key, we need the session API also --> now we have the information to access the laps for the race itself.
# now that we have driver_number for p1p2p3, we use the meeting key and access to complete lap information --> we need the laps API

# meetings API -> session_result API -> session API -> laps API

# Next step is to edit the string.

# MEETINGS API:
# country_name = name of country the track resides in
# meeting_name = Track name 
# location = location of track within country, this can be utilised for open meteo
# meeting_key = this is a chronological unique identifier for this meeting (specific to that individual grand prix but NOT specific to the session (Qual, Sprint, or Race etc.))
# number_of_laps = total number of laps completed (should be equal for racers (in a RACE) unless they dnf)

# SESSION API:
# session_key = unique identifier that is specific to the session itself not just the meeting 
# session_name = specifiy 'Race' in the API call to obtain the session_key of that RACE

# SESSION_RESULT API:
# driver_number = unique identifier for drivers
# position = the position they came in that session_key (we want the session_key of the RACE)
# session_key = unique identifier that is specific to the session itself not just the meeting 
# meeting_key = this is a chronological unique identifier for this meeting (specific to that individual grand prix but NOT specific to the session (Qual, Sprint, or Race etc.))


# LAPS API:
# session_key = unique identifier that is specific to the session itself not just the meeting
# lap_number = the lap within the race (we know the total number of laps in the session)
# duration_sector_1/2/3 = the time take to complete those sectors of the track during that lap
# st_speed = the speed trap, where top speed is recorded on that specific lap
# is_pit_out_lap = boolean value, if True means car was in pit during this lap (ACKNOWLEDGE AND REMOVE THESE LAP TIMES AND DISTANCES IN AVG SPEED CALCULATIONS)
# lap_duration = the total lap duration adding each sector together

# Current primary issues to navigate:
# Issue 1 --> How to manipulation html string for API calls for each section
# The HTML is not too difficult to understand that will be relatively easy
# Issue 2 --> no where on openF1 does it have complete track distance. I will have to access this else but will be messy?




# Initial script, learning to navigate the API
# Location/Track name is a USER INPUT

input_variable = 'Singapore Grand Prix'.replace(" ", "%20") # temporary -> URLs dont have spaces, instead either + or %20 --> replace ' ' with '%20'
base_link = 'https://api.openf1.org/v1/'
# I am having issues accessing information via inputting the track name.
current_year = [datetime.now().year][0]

print((base_link + f'meetings?meeting_name={input_variable}'))

# Obtain Meetings information:
response = urlopen((base_link + f'meetings?meeting_name={input_variable}'))
# response = urlopen((base_link + f'meetings?meeting_key=latest'))

# response = urlopen('https://api.openf1.org/v1/race_control?flag=BLACK%20AND%20WHITE&driver_number=1&date>=2023-01-01&date<2023-09-01')

data = json.loads(response.read().decode('utf-8'))
print(data)
# The data is chronological - [-1] in the list of dicts will be the most recent meeting_key

# obtain the last 2 meeting_keys
#data = data[-2:]#
#print(data)


# Current issue - API rejecting requests