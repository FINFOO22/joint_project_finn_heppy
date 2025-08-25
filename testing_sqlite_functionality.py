#!/usr/bin/env python
# from argparse import ArgumentParser, Namespace
import sqlite3




# testing SQLite, a built in python package fro small - medium databases.
# following a tutorial - https://www.youtube.com/watch?v=pd-0G0MigUA - 08082025
def speed_dist_calc(value):
    dist_1 = (sum((value[1])*10)/len(value[1]))/100 # current values in decimetres so converting to centimetres AND divide by 100 to convert to metres!
    speed_1 = (dist_1/1000)/((sum(value[0])/len(value[0]))/3600) # /3600 to convert to hours, as speed going to measure in km/hr
    return speed_1, dist_1




def update_database(track_id: int, speed_data: dict, session_keys: list, st_speeds: list):
    conn = sqlite3.connect('aerofoil_optimization.db')
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE track_info (
                track_id integer,
                session_keys text,
                length real,
                mean_speed real,
                s1_length real,
                mean_speed_s1 real,
                s2_length real,
                mean_speed_s2 real,
                s3_length real,
                mean_speed_s3 real,
                UB_speed real,
                LB_speed real
                );""")
    except sqlite3.OperationalError:
        print('The track_info relational table is already present.\n')

    # calculate values input
    for key, value in speed_data.items():
        if key == 1:
            speed_1, dist_1 = speed_dist_calc(value=value)
        elif key == 2:
            speed_2, dist_2 = speed_dist_calc(value=value)
        elif key == 3:
            speed_3, dist_3 = speed_dist_calc(value=value)
        elif key == 'complete':
            speed, dist = speed_dist_calc(value=value)
        
    st_speed = sum(st_speeds)/(len(st_speeds))
    session_keys_used = '-'.join(session_keys)
    lb_speed = st_speed-speed


# Once the db is made, re running this will cause an error.
# I am not entirely sure how our system will run, 
# if it is run locally we would need this first section in a try and except clause so for people running the application for the first time will have their databse made.

# stack overflow example inserting records:
# https://stackoverflow.com/questions/37384874/how-to-insert-data-in-only-few-column-leaving-other-columns-empty-or-as-they-are
    c.execute("""
        INSERT INTO track_info 
        (
            track_id,
            session_keys,
            length,
            mean_speed,
            s1_length,
            mean_speed_s1,
            s2_length,
            mean_speed_s2,
            s3_length,
            mean_speed_s3,
            UB_speed,
            LB_speed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        track_id,
        session_keys_used,
        dist,
        speed,
        dist_1,
        speed_1,
        dist_2,
        speed_2,
        dist_3,
        speed_3,
        st_speed,
        lb_speed
    ))

    c.execute("""SELECT * 
              FROM track_info 
              WHERE track_id= ?""", (track_id,))
    results = c.fetchall()
    print(f'Here is your list of information of track_id = {track_id}:\n\n{results}')









# Selecting rows from the table (this is where our SQL db comes in - we search our database FIRST for the available information the user requests)
# if there is none available, we go through the API rewquest route via openf1 and meteo
#c.execute("""SELECT * 
#          FROM track_info 
#          WHERE track_id=69""")
#results = c.fetchall()
#print(f'Here is your list of information of track_id = 69:\n\n{results}')
# this will return a list (or an empty list if nothing avaible from your select statement)


#conn.commit() # commits the current transaction 
#conn.close() # good practise to close the connection to the database