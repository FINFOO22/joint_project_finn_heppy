#!/usr/bin/env python



# here is the openf1 datetime string
datetime = "2023-09-16T13:03:35.292000+00:00"

def datetime_conversion(datetime_string: str):
    # "string".split
    split_ = datetime_string.split('T')
    seconds = [float(x) for x in split_[1].split('+')[0].split(':')]
    seconds = (seconds[0]*60*60 + seconds[1]*60 + seconds[2])
    print(f'datetime string: {datetime_string} | equivalent to: {split_[0]} at {seconds} seconds into the day')


datetime_conversion(datetime_string=datetime)