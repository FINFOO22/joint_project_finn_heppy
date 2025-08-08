#!/usr/bin/env python



# testing SQLite, a built in python package fro small - medium databases.
# following a tutorial - https://www.youtube.com/watch?v=pd-0G0MigUA - 08082025
import sqlite3

conn = sqlite3.connect('aerofoil_optimization.db')

c = conn.cursor()

try:
    c.execute("""CREATE TABLE track_info (
            track_id integer,
            length real,
            mean_speed integer,
            mean_speed_s1 integer,
            mean_speed_s2 integer,
            mean_speed_s3 integer,
            UB_speed integer,
            LB_speed integer
            );""")
except sqlite3.OperationalError:
    print('The database is already present.\n')

# Once the db is made, re running this will cause an error.
# I am not entirely sure how our system will run, 
# if it is run locally we would need this first section in a try and except clause so for people running the application for the first time will have their databse made.

# stack overflow example inserting records:
# https://stackoverflow.com/questions/37384874/how-to-insert-data-in-only-few-column-leaving-other-columns-empty-or-as-they-are
c.execute("""INSERT INTO 
          track_info 
          (track_id, UB_speed)
          VALUES
          (69, 420);
          """)

# Selecting rows from the table (this is where our SQL db comes in - we search our database FIRST for the available information the user requests)
# if there is none available, we go through the API rewquest route via openf1 and meteo
c.execute("""SELECT * 
          FROM track_info 
          WHERE track_id=69""")
results = c.fetchall()
print(f'Here is your list of information of track_id = 69:\n\n{results}')
# this will return a list (or an empty list if nothing avaible from your select statement)


conn.commit() # commits the current transaction 
conn.close() # good practise to close the connection to the database