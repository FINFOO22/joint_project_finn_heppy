#!/usr/bin/env python

# 01082025 - testing OpenF1 API
# So here this project requires access to the speeds, obtaining the average from the ##top three speeds## (p1, p2, p3) of the track from the ##past two years##
from datetime import datetime
import urllib
from urllib.request import urlopen
import json
from math import sqrt
from time import sleep
#response = urlopen('https://api.openf1.org/v1/session_result?session_key=latest')
#data = json.loads(response.read().decode('utf-8'))
#print(data)
from converting_timestamp_into_numerical import *



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
    time = 0.0
    while True:
        try:
            sleep(time)
            response = urlopen(('https://api.openf1.org/v1/' + url_extension))
            break
        except urllib.error.HTTPError:
            time = (time+0.01)*2
    data = json.loads(response.read().decode('utf-8'))
    return data


# Obtain Meetings information: INFO REQUIRED FOR REQUEST: meeting name (user input)

input_variable = 'Singapore Grand Prix'.replace(" ", "%20") # temporary -> URLs dont have spaces, instead either + or %20 --> replace ' ' with '%20'
print(f'Obtaining the most recent meetings from {input_variable}')
data = request_and_get_data(f'meetings?meeting_name={input_variable}')[-2:] # [-2:] as this returns the two most recent track meetings

# Obtain Sessions information: INFO REQUIRED FOR REQUEST: meeting_key (obtained from Meetings request), session_type (as of 05082025 I am using Race for simplicity)
data_2 = []
session_type = 'Race'
for meeting in data:
    track_id = int(meeting['circuit_key'])
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






#print(data)
#print(data_2)
#print(sessions)
#print(session_laps) # session laps is a: dict (key is session_key) and value is a dict with key as driver_number and value is a list every lap that is an OUT OF PIT LAP (every lap is a dict)
#quit()


# creating function based on the testing_track_calculation.py script : 12082025
def calc_track_distance(all_location_points):
    total_distance_travelled = 0
    for i in range(0, (len(all_location_points)-1), 1): # so we dont loop to last point, as this will have no next position which we calculate distance travelled from
        pos_1 = (all_location_points[i]['x'], all_location_points[i]['y'], all_location_points[i]['z'])

        pos_2 = (all_location_points[i+1]['x'], all_location_points[i+1]['y'], all_location_points[i+1]['z'])

        # calculate distance travelled
        travelled_distance = sqrt((pos_1[0]-pos_2[0])**2 + (pos_1[1]-pos_2[1])**2 + (pos_1[2]-pos_2[2])**2)
        total_distance_travelled += travelled_distance
    return total_distance_travelled


# now calculating overall distance of track for every lap of the top three drivers
sectors_split = {}
# theoretical dictionary layout for sectors_split:
{1: [['every sec 1 time'], ['every sec 1 distance']],
     2:[['same but for sec 2']],
     3:[['same but for sec 3']],
     'complete': [['same but for whole track']]
     }


#print(session_laps) # 
st_speeds = [] # to store all the st_speeds 

for session_key, driver in session_laps.items():
    print(f'Collating the data for session key: {session_key}')
    for driver_number, laps in driver.items():
        print(f'\t# Collating data from driver: {driver_number}')
        #print(driver_number)
        #print(laps)
        for i in range(0, len(laps)-1, 1):
            if laps[i]['date_start'] is None:
                continue # SOME OF THE LAPS HAVE INCOMPLETE INFoRMATION - I DONT KNOW WHY

            if laps[i]['lap_number'] != (laps[i+1]['lap_number'] - 1): # as it should be lap compared to the very next lap after
                # (but could be removed if that lap was a pit lap therefore we will have to exclude measuring that one) 
                continue
            else:
                try:
                    
                    exact_start_time = laps[i]['date_start'] # this is a string thatll need to be broken down to work out where sectors end and start within laps to calc their exact distance --> and subsequently the speeds
                    #print(exact_start_time)
                    date, start_time = datetime_conversion(exact_start_time)
                    try:
                        time_sect_1 = start_time + laps[i]['duration_sector_1']
                        time_sect_2 = time_sect_1 + laps[i]['duration_sector_2']
                    except TypeError: # some laps have no values on their sector times
                        continue
                    final_time = datetime_conversion(laps[i+1]['date_start'])
                    # now that we have requested all the lap I can do a binary search for all the coord splits
                    # then calculate distances HOWEVER , sector finishing times are not inline with the coordinate recording timepoints, so how do I make an accurate guess to the track distance
                    # if I cannot get the exact location of the car when they complete sector x?
                    
                    # This is NEXT STEP
                    

                    
                    all_location_points = request_and_get_data(f"location?session_key={session_key}&driver_number={driver_number}&date>={laps[i]['date_start']}&date<={laps[i+1]['date_start']}")
                    sectors = [laps[i]['duration_sector_1'], laps[i]['duration_sector_2']]
                    sectors_time_points = [time_sect_1, time_sect_2]
                    # 24082025
                    # calculating for sector 1
                    index_to_start_from = 0
                    # sectors_split = {}
                    dist_travelled = 0
                    for sector_index in range(0, len(sectors)): # this is a SLOW way to search, might need to change it in the future CAN work out final sector by subtracting these from the complete distance
                        for index in range(index_to_start_from, len(all_location_points)):
                            if datetime_conversion(all_location_points[index]['date'])[1] > sectors_time_points[sector_index]: # this means it has gone past the sector (the index before is the correct one)
                                sector_distance_travelled = calc_track_distance(all_location_points=all_location_points[index_to_start_from:index]) # will return everything except current index on
                                try:
                                    sector_distance_travelled = sector_distance_travelled + t2_dist
                                except:
                                    #print('Here')
                                    pass

                                
                                t1 = datetime_conversion(all_location_points[index-1]['date'])[1]
                                
                                t2 = datetime_conversion(all_location_points[index]['date'])[1]
                                #print(f't1: {t1} | t2: {t2}')

                                t1t2_dist_travelled = calc_track_distance(all_location_points=all_location_points[index-1:index+1])
                                #print(f'distance travelled between these time points: {t1t2_dist_travelled}')

                                time_gap = t2 - t1
                                #print(f'time gap between these: {time_gap}')

                                gap = datetime_conversion(all_location_points[index-1]['date'])[1]
                                gap = sectors_time_points[sector_index] - gap
                                #print(f'time on sector {sector_index+1}: {sectors[sector_index]} | gap between last time point in sector {sector_index+1} and actual sector completion time: {gap}')

                                t1_dist = (t1t2_dist_travelled)*(gap/time_gap)
                                t2_dist = (t1t2_dist_travelled)*((time_gap-gap)/time_gap)
                                #print(f't1_dist: {t1_dist} | t2_dist: {t2_dist}')

                                sector_distance_travelled = sector_distance_travelled + t1_dist
                                #print(f'sector_distance_travelled: {sector_distance_travelled}')
                                # update the dictionary
                                try:# access the dictionary
                                    times_distances = sectors_split[(sector_index+1)]
                                    times_distances[0] = times_distances[0] + [sectors[sector_index]]
                                    times_distances[1] = times_distances[1] + [sector_distance_travelled]
                                    
                                    sectors_split[(sector_index+1)] = times_distances
                                    dist_travelled += sector_distance_travelled
                                    
                                    index_to_start_from = index
                                except:
                                    sectors_split[(sector_index+1)] = [[sectors[sector_index]],[sector_distance_travelled]]
                                    dist_travelled += sector_distance_travelled


                                    index_to_start_from = index
                                break # to end this loop as we found the cutoff of sector n -> sector n+1
                    
                    # now add the total distance and total time taken for that lap AND the final sector
                    complete_distance_travelled = calc_track_distance(all_location_points=all_location_points)

                    
                    # now add sector 3 
                    try:
                        times_distances = sectors_split[3]
                        times_distances[1] = times_distances[1] + [(complete_distance_travelled-dist_travelled)]
                        times_distances[0] = times_distances[0] + [laps[i]['duration_sector_3']]
                        sectors_split[3] = times_distances

                        times_distances = sectors_split['complete']
                        times_distances[1] = times_distances[1] + [complete_distance_travelled]
                        times_distances[0] = times_distances[0] + [laps[i]['lap_duration']]
                        sectors_split['complete'] = times_distances
                    except:
                        sectors_split[3] = [[laps[i]['duration_sector_3']],[(complete_distance_travelled-dist_travelled)]]
                        sectors_split['complete'] = [[laps[i]['lap_duration']],[complete_distance_travelled]]


                    #print(f"Driver: {driver_number}\nLap: {laps[i]['lap_number']}\nTravelled: {complete_distance_travelled}")
                    #print(sectors_split)
                    #quit()
                    
                except urllib.error.HTTPError:
                    time = 0.2
                    while True:
                        if time > 4: # arbitrary time
                            print(f'Request time rest is: {time} seconds')
                        sleep(time)  
                        try:
                            exact_start_time = laps[i]['date_start'] # this is a string thatll need to be broken down to work out where sectors end and start within laps to calc their exact distance --> and subsequently the speeds
                            all_location_points = request_and_get_data(f"location?session_key={session_key}&driver_number={driver_number}&date>={laps[i]['date_start']}&date<={laps[i+1]['date_start']}")
                            distance_travelled = calc_track_distance(all_location_points=all_location_points)

                            print(f"Driver: {driver_number}\nLap: {laps[i]['lap_number']}\nTravelled: {distance_travelled}")
                            break
                        except urllib.error.HTTPError:
                            time = time*2

            try:
                st_speeds += [int(laps[i]['st_speed'])] # to retain the st_speed info # THEY HAVENT ALWAYS REFCORDED THE SPEEDS
            except:
                pass
# 24082025
# Next steps: apply the try except clause for requests for the whole script  -done
# allow script to run for every lap - done
# start writing the function that inputs this into SQL format




# 25082025
from testing_sqlite_functionality import *

update_database(track_id=track_id, speed_data=sectors_split, session_keys=session_keys, st_speeds=st_speeds)











quit()
# calculated the distance --> what now?
# Step one:
# use the converting timestamp function to get exact times,
# Get the time in seconds when the lap starts, and work out the time at which each sector ends AND starts
# from here can work out the distances of each sector and the subsequent speed 


# HOW?
# datetime_conversion(datetime_string: str) the start of lap
# add the sector time to it --> reconvert that to the datetime format string --> MAKE a request for the individual sectors (every location within that timeframe)
# calculate distances travelled for each 
# average them and record --> pipe all the necessary information into the script that writes the sql table.







# testing SQLite, a built in python package fro small - medium databases.
# following a tutorial - https://www.youtube.com/watch?v=pd-0G0MigUA - 08082025
import sqlite3

conn = sqlite3.connect('aerofoil_optimization.db')

c = conn.cursor()

c.execute("""CREATE TABLE track_info (
          track_id integer,
          rl_length real,
          mean_speed integer,
          mean_speed_s1 integer,
          mean_speed_s2 integer,
          mean_speed_s3 integer,
          UB_speed integer,
          LB_speed integer
          )""")


