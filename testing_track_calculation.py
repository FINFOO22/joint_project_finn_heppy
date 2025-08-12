from datetime import datetime
from urllib.request import urlopen
import json
from math import sqrt


def request_and_get_data(url_extension):
    response = urlopen(('https://api.openf1.org/v1/' + url_extension))
    data = json.loads(response.read().decode('utf-8'))
    return data


data_start = request_and_get_data("laps?session_key=9161&driver_number=63&lap_number=8") # here is a test example 
print(data_start) # this has the lap time when it STARTED, and the duration 

data_end = request_and_get_data("laps?session_key=9161&driver_number=63&lap_number=9") # here is a test example - CHNAGED TO LAP 9 to see when track ended VERSUS when it started
print(data_end)

# now we have data start and start of lap after
# here is an example html request: location?session_key=9161&driver_number=81&date>2023-09-16T13:03:35.200&date<2023-09-16T13:03:35.800
all_location_points = request_and_get_data(f"location?session_key={data_start[0]['session_key']}&driver_number={data_start[0]['driver_number']}&date>={data_start[0]['date_start']}&date<={data_end[0]['date_start']}")

print(f'Here is all the time points record and the cartesian coords:\n\n\n\n\n\n\n{all_location_points}')

# the distance between each point should be pythag!
total_distance_travelled = 0
for i in range(0, (len(all_location_points)-1), 1): # so we dont loop to last point, as this will have no next position which we calculate distance travelled from
    pos_1 = (all_location_points[i]['x'], all_location_points[i]['y'], all_location_points[i]['z'])

    pos_2 = (all_location_points[i+1]['x'], all_location_points[i+1]['y'], all_location_points[i+1]['z'])

    # calculate distance travelled
    travelled_distance = sqrt((pos_1[0]-pos_2[0])**2 + (pos_1[1]-pos_2[1])**2 + (pos_1[2]-pos_2[2])**2)
    total_distance_travelled += travelled_distance

print(f'\n\n\nHere is the total distance travelled:   {total_distance_travelled}')


data = request_and_get_data("sessions?session_key=9161")
print(data)