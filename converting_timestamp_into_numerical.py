#!/usr/bin/env python



# here is the openf1 datetime string
# datetime = "2023-09-16T13:03:35.292000+00:00"

def datetime_conversion(datetime_string: str):
    # "string".split
    split_ = datetime_string.split('T')
    seconds = [float(x) for x in split_[1].split('+')[0].split(':')]
    seconds = (seconds[0]*60*60 + seconds[1]*60 + seconds[2])
    # print(f'datetime string: {datetime_string} | equivalent to: {split_[0]} at {seconds} seconds into the day')
    return split_[0], seconds

# date, time = datetime_conversion(datetime_string=datetime)


def datetime_un_conversion(time_seconds_float: float, date: str):
    pass
    time = ':'.join([('0' + str(x)) if x < 10 else str(x) for x in [int(time_seconds_float/3600), int((time_seconds_float%3600)/60), ((time_seconds_float%3600)%60)]])

    datetime = 'T'.join([date, time])
    return datetime

    #print(f'Here is the datetime: {datetime}')

# datetime_un_conversion(time_seconds_float=time, date=date)