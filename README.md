# InsightData-Coding-Challenge
Contains solution files for coding challenge given by InsightData

# Table of Contents
1. [Overview](README.md#overview)
2. [Problem Statement](README.md#problem-statement)
3. [Methodology](README.md#methodology)
3. [Testing](README.md#testing)


# Overview

This repository is made for the purpose of presenting participation in coding challenege by InsightData (Data Engineering).
The analysis code is written in Python which use the package `pandas`, `re`, and `datetime`.

# Problem Statement

For this challenge, we're asked to take existing publicly available EDGAR weblogs and assuming that each line represents a single web request for an EDGAR document that would be streamed into your program in real time. Using the data, we need to identify when a user visits, calculate the duration of and number of documents requested during that visit, and then write the output to a file, `sessionization.txt`.

For each log line, we need to output these values:

* IP address of the user exactly as found in log.csv
* date and time of the first webpage request in the session (yyyy-mm-dd hh:mm:ss)
* date and time of the last webpage request in the session (yyyy-mm-dd hh:mm:ss)
* duration of the session in seconds
* count of webpage requests during the session

All other details of the challenge and files used in it can be found at https://github.com/InsightDataScience/edgar-analytics

# Methodology

To solve this challenge, we follow the concept of modularity. We created methods for each and every thing so that the program can be scaled at any point in future.
The following steps are followed to solve the challenge:

* Read the input and output file paths from command line arguments
* Raise an exception if number of arguments are not appropriate
* Read the input files i.e. `log.csv` and `inactivity_period.txt` 
* Raise exception if inactivity_time is not numeric or null or not within the range 1-86400 (1 sec to 24 hrs)
* Create an empty table `active_users` for keeping record of active sessions
* While reading every line from the log file, do the following:
	* Split the line on `,`
	* Validate if columns are in order and define every needed element as descriptive variable
	* Perform checks for corrupt or null data
	* If corrupted data is found then skip and read next line
	* Combine date and time variable as one datetime object
	* check if `active_users` table is not empty
	* If it is not empty then for every row in `active_users` table (if not empty):
		* Check if user is being inactive for more than inactive_time_period
		* If above check returns true then write above output variable in output variable and delete the user from 'active_user` table
		* Else read next row in the table
	* Check if user is there in `active_user` table as active user
	* If it matches, then update the last_acessing_datetime and page_count for that user in `active_user` table
	* If it doesn't match any row in the table then append the user details in the table
* After there are no logs left to read in `log.csv`, check if `active_users` table is not empty
* If it is not empty then for every row in `active_users` table (if not empty):
		* Check if user is being inactive for more than inactive_time_period
		* If above check returns true then write above output variable in output variable and delete the user from 'active_user` table
		* Else read next row in the table
* Close all the opened files

The methods created are as follows:

* PercentileNumericError: This class extends the Exception class and handle the error if percentile is not numeric or is null
* check_null(): This function takes the data to be checked if there are nulls
* chk_time_diff(): This function calculate differece between two datetime objects in seconds
* write_output_data(): This function format the inactive users details in order to write in the output file
* check_active_user(): This function checks if the new log is about the active user or not by checking its presence in `active_users` table
* add_new_user(): This function add the new active user to `active_users` table
* check_pattern(): This function checks if the data is valid by checking the pattern of input
* validate_row(): This function checks if the columns given in log file are in order or not
* main_analytics_function(): This function use the all above functions to read the input, calculate all the needed measures and write them to the output file.


# Testing

### Pre-requisite:

Make sure you have the following installed before testing:

* Python
* pandas (Python package)
* datetime (Python package)
* re (Python package)

Create a new folder `test_n` in `insight_testsuite\tests` folder. Create two more folders as `input` and `output` in the folder `test_n`. Put your version of both the input files (`log.csv` and `inactivity_period.txt`) and output file (`sessionization.txt`) in these folder.

### On Linux:

To test on Linux,

Open the shell and traverse to the path of `insight_testsuite` folder and run the following statement:

	insight_testsuite~$ ./run_tests.sh

On a failed test, the output of `run_tests.sh` should look like:

    [FAIL]: test_n
    [Mon Apr 2 16:28:01 PDT 2018] 0 of 11 tests passed

On success:

    [PASS]: test_n
    [Mon Apr 2 16:25:57 PDT 2018] 11 of 11 tests passed
	
### On Windows:

To test the program on Windows,

Open the command prompt and traverse to the path of `insight_testsuite\tests\test_n` and run the following statement:

	insight_testsuite\tests\test_n> python ../../../src/sessionization.py ./input/log.csv ./input/inactivity_period.csv ./output/sessionization.txt

The output file `sessionization.txt` can be checked in output folder.