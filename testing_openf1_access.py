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


def practise():
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
    # print(data)
    # The data is chronological - [-1] in the list of dicts will be the most recent meeting_key
    #
    # data = [1,2,3,4,5]
    # obtain the last 2 meeting_keys
    data = data[-2:] # this will obtain the previous TWO meeting_keys
    print(data)


    # Current issue - API rejecting requests -- > this happens occassionally, server down?
    data_2 = []
    #next step - sessions
    for meeting in data:
        session_type = 'Race' # for now putting race, Heppy suggests model for Qual (faster speeds, car tuned for greater power versus race)
        input_variable = f'{meeting['meeting_key']}'
        url_request = base_link + f'sessions?meeting_key={input_variable}&session_type={session_type}'
        response = urlopen(url_request)
        data_int = json.loads(response.read().decode('utf-8')) # json ,loads puts it into a list anyway so should not do: data_2 += [data_int]
        data_2 += data_int

    print('here is the information on the meetings (older meets first in list)')
    print(data_2)

    # next steps - session_results
    sessions = {}
    for session in data_2:
        # return the top 3 drivers
        session_key = f'{session['session_key']}'
        url_request = base_link + f'session_result?session_key={session_key}' + '&position<=3'
        response = urlopen(url_request)
        data_3 = json.loads(response.read().decode('utf-8'))
        sessions[session['session_key']] = data_3

    print('here are the top three positions for the two MOST RECENT sessions at this track')
    print(sessions)


    # next step is to access the lap times of every lap where they were NOT PITTED at the start
    session_laps = {}
    session_keys = list(sessions.keys())
    for session_key in session_keys:
        session_laps[session_key] = []
        for pos in range(0,len(sessions[session_key])): # this should be 3 - as it is the top three positions in the session_results request
            url_request = base_link + f'laps?session_key={session_key}&driver_number={sessions[session_key][pos]['driver_number']}&is_pit_out_lap=false' # this should be the driver number (accessed from session results data)
            # the the is pit out lap as false so only the laps on track whole time & the session_key
            response = urlopen(url_request)
            data_4 = json.loads(response.read().decode('utf-8'))
            session_laps[session_key] += data_4


    print('here are the laps and timings for the top three drivers in the most recent two track meets!\n\n\n\n\n')
    print(session_laps)
    # should extract the necessary information but should be all hear (except the track distance!!)









# Next put in the simplified function (a few mini functions (the data request lines))
def request_and_get_data(url_extension):
    response = urlopen(('https://api.openf1.org/v1/' + url_extension))
    data = json.loads(response.read().decode('utf-8'))
    return data


# Obtain Meetings information: INFO REQUIRED FOR REQUEST: meeting name (user input)
input_variable = 'Singapore Grand Prix'.replace(" ", "%20") # temporary -> URLs dont have spaces, instead either + or %20 --> replace ' ' with '%20'
data = request_and_get_data(f'meetings?meeting_name={input_variable}')[-2:] # [-2:] as this returns the two most recent track meetings

# Obtain Sessions information: INFO REQUIRED FOR REQUEST: meeting_key (obtained from Meetings request), session_type (as of 05082025 I am using Race for simplicity)
data_2 = []
session_type = 'Race'
for meeting in data:
    data_2 += request_and_get_data(f'sessions?meeting_key={meeting['meeting_key']}&session_type={session_type}')
    

# Obtain Session Results: INFO REQUIRED FOR REQUEST: session_key (obtained from Sessions request), top 3 placed (<= 3)
sessions = {}
for session in data_2:
    session_key = f'{session['session_key']}'
    sessions[session_key] = request_and_get_data(f'session_result?session_key={session_key}&position<=3')

# Obtain Lap information: INFO REQURIED FOR REQUEST: session_key (obtained from Sessions request), driver_number (obtained from the Session Results request), is_pit_out_lap (FALSE, we only want laps with pit interruption)
session_keys = list(sessions.keys())
session_laps = {}
for session_key in session_keys:
    session_laps[session_key] = {}
    for pos in range(0,len(sessions[session_key])):
        session_laps[session_key][sessions[session_key][pos]['driver_number']] = request_and_get_data(f'laps?session_key={session_key}&driver_number={sessions[session_key][pos]['driver_number']}&is_pit_out_lap=false')






print(data)
print(data_2)
print(sessions)
print(session_laps)













# testing SQLite, a built in python package fro small - medium databases.
# following a tutorial - https://www.youtube.com/watch?v=pd-0G0MigUA - 08082025
import sqlite3

conn = sqlite3.connect('aerofoil_optimization.db')

c = conn.cursor()

c.execute("""CREATE TABLE track_info (
          track_id integer,
          length real,
          mean_speed integer,
          mean_speed_s1 integer,
          mean_speed_s2 integer,
          mean_speed_s3 integer,
          UB_speed integer,
          LB_speed integer
          )""")


