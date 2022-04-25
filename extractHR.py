import requests
import json
import csv
import sys
import datetime


# This Python script retrieves a Fitbit user's personal heart rate data
# on the specified [date], during a specified time interval, from
# [start-time] to [end-time] with detail level 1 sec. It then writes
# the intraday heart rate data to a .csv file. 

# To run the script, an access token is required as well as the 
# Fitbit user's id, which need to be stored in the variables
# access_token and user_id in STEP 2: EXTRACT HEART RATE DATA. 

# This script assumes that the application 
# registered with Fitbit is of type "Personal".
# Consult https://dev.fitbit.com/build/reference/web-api/developer-guide/getting-started/
# for more information on registering an application with Fitbit.

# 3 command line arguments are taken as input: [date] [start-time] [end-time]
# NOTE: the order of the arguments matters
#    [date]         is in YYYY-mm-dd format, no later than today's date
#    [start-time]   is in HH:MM format, and strictly earlier than [end-time]
#    [end-time]     is in HH:MM format. If [date] is today, 
#                   then [end-time] is strictly earlier than current time

# Primary Reference [1]
#  Title: Python Fitbit API Tutorial Writing Heart Rate Data to an Excel File
#  Author: red2fire2
#  Date: May 28, 2020
#  Availability: https://www.youtube.com/watch?v=X0RDQWbJw9I&t=190s

# Abbreviations: hr =  heart rate


# ----- STEP 1: VALIDATE COMMAND LINE ARGUMENTS --------


class IncorrectNumberOfArguments(TypeError):
    # raised when incorrect number of command line arguments provided
    pass

# Check number of command line arguments
# Reference [2]: https://datatest.readthedocs.io/en/stable/how-to/date-time-str.html
if(len(sys.argv) != 4):
    raise IncorrectNumberOfArguments("Three arguments are expected: [date] [start-time] [end-time]")
 
# Store command line args
date = sys.argv[1]
start_time = sys.argv[2]
end_time = sys.argv[3]
    
# Check the format of the date
try:
    datetime.datetime.strptime(date, "%Y-%m-%d")
except ValueError:
    print("Incorrect format for [date]. The format should be YYYY-mm-dd. Please try again.")
    exit()

# Check whether [date] is later than today's date
# in which case, exit the program
today_date = datetime.datetime.today().strftime("%Y-%m-%d")
if (date > today_date):
    raise ValueError("The [date] cannot be later than today's date.")


# Check whether start, end times are valid
#  References:
#  [4] https://www.adamsmith.haus/python/answers/how-to-validate-a-date-string-format-in-python
#  [2] https://datatest.readthedocs.io/en/stable/how-to/date-time-str.html

try:
    datetime.datetime.strptime(start_time, "%H:%M")
except ValueError:
    print("Invalid [start-time]. Format should be HH:MM. Please try again.")
    exit()

try:
    datetime.datetime.strptime(end_time, "%H:%M")
except ValueError:
    print("Invalid [end-time]. Format should be HH:MM. Please try again.")
    exit()


# Check whether [start-time] earlier than [end-time]
t1 = datetime.datetime.strptime(start_time,"%H:%M")
t2 = datetime.datetime.strptime(end_time,"%H:%M")

if t1 >= t2:
    print("[start-time] needs to be earlier than [end-time].")
    exit()

# If [date] is today's date, check that [end-time] < current time
if date == today_date:
    curr_time = datetime.datetime.today().strftime("%H:%M")
    curr_time = datetime.datetime.strptime(curr_time, "%H:%M")
    if t2 > curr_time:
        raise ValueError("If you are trying to obtain heart rate data from today, then the [end-time] needs to be earlier than the current time.")



#------ STEP 2 EXTRACT HEART RATE DATA -----------------

# Store access token and user id
access_token ='ACCESS TOKEN GOES HERE'
user_id = 'USER ID GOES HERE'


# Make a GET request
#  Other JSON URLs can be found here: 
#  https://blog.coupler.io/fitbit-data-export/#Data_that_you_can_export_via_Fitbit_API
hr_request = requests.get('https://api.fitbit.com/1/user/'+ user_id +'/activities/heart/date/' + date  + '/1d/1sec/time/' + start_time + '/' + end_time + '.json', headers={'Authorization': 'Bearer ' + access_token})

# Print status code
print(hr_request.status_code)

# Store intraday heart data
intraday_hr_data = hr_request.json()['activities-heart-intraday']['dataset']

# Write intraday heart rate data to a csv file
with open("hr_"+ date + '_'  + start_time + '_' + end_time + ".csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in intraday_hr_data:
        # print(line['value'])
        writer.writerow(line.values())

