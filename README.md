# Fitbit Heart Rate Extractor
Provides a way to extract Fitbit user's personal intraday heart rate data on a particular date, during a particular time interval with detail level 1 second.
Can only be used when the application registered with Fitbit is of type "Personal". Before running the script, create a Fitbit Developer Account, then register an application with Fitbit. A Fitbit access token then needs to be retrieved, as well as the Fitbit user's id. The user id can easily be found by logging in on the [Fitbit Official Site][0], clicking on "View Profile" and then looking at the resulting URL. For instance, ``https://www.fitbit.com/user/4ABCDE`` would mean the user id is 4ABCDE.

[0]: https://www.fitbit.com/

## Resources
- Consult [Intraday][1] for more information on Fitbit intraday data.
- Consult [Getting Started with the Fitbit APIs][2] for more information on creating a Fitbit Developer Account and Registering an Application.
- Consult [Authorization][3] for more information on how to retrieve a Fitbit access token.

[1]: https://dev.fitbit.com/build/reference/web-api/intraday/
[2]: https://dev.fitbit.com/build/reference/web-api/developer-guide/getting-started/
[3]: https://dev.fitbit.com/build/reference/web-api/developer-guide/authorization/

## Usage

**Step 1** - Store the fitbit access token and the user's id in the variables ```access_token``` and ```user_id``` in ```extractHR.py```

**Step 2** - Run the python script as follows:
```
python extractHR.py <date> <start_time> <end_time>
```
Where,
- ```<date> ```         is in the format ```<YYYY-mm-dd>```, and is no later than today's date
- ``` <start_time```    is in the format ```<HH:MM>```, and is earlier than ```<end_time>```
- ```<end_time>```      is in the format ```<HH:MM>```. If ```<date>``` is today, then the ```<end_time>``` needs to be earlier than the current time

## Output
**Notes**
- After successfully running the script, the user's intraday heart rate data will be saved in a .csv file called ```hr_<date>_<start_time>_<end_time>.csv```
- If there is no intraday heart rate data for the specified date, during the specified time interval, the .csv file will be empty.
- Even though the detail level specified is 1 second, heart rate readings are typically recorded every 5-15 seconds, and or 1-3 seconds when the Fitbit device is in "exercise mode".

**Sample Output:**
- View the file ```hr_2022-03-24_09_30_09_35.csv``` for sample heart rate data, when the Fitbit device in regular mode
- View the file ```hr_2022-02-03_18_30_18_35.csv``` for sample heart rate data, when Fitbit device exercise mode

**Response codes**:
- **200**: request was successful
- **400**: the request could not be satisfied
- **401**: user authentication required

Other response codes can be found [here][4].

[4]: https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/error-messages/
