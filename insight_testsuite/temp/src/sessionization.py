# importing required modules
import pandas as pd
from datetime import datetime
import sys
import re


class InactivityNumericError(Exception):
    """ Raised when inactivity time is not numeric """
    pass


class InactivityRangeError(Exception):
    """ Raised when inactivity time is not in range """
    pass

class ColumnLengthError(Exception):
    """ Raised when number of columns is not appropriate """
    pass


def check_null(*args):
    """ Check for null values """

    print("Checking for null values...")
    for val in args:
        if val == "":
            return(True)
    return(False)


def chk_time_diff(now, last):
    """ Calculate difference in seconds """

    print("Calculating time difference...")
    seconds = (now - last).total_seconds()
    return seconds


def write_output_data(file, data):
    """ File the output in the required format """

    print("Formatting output for writing into file.")
    file.write(",".join(data))
    file.write("\n")


def check_active_user(active_users, ip):
    """ Check if the session is active or not """

    r = active_users.loc[(active_users["ip"] == ip)].index.tolist()
    print("Checking if session is still active...")
    return(r)


def add_new_user(active_users, details):
    """ Append the new user encountered into the table """

    print("Adding new user to Dataframe.")
    columns = ["ip", "first_date_time", "last_date_time", "page_count"]
    new_user = pd.Series(details, columns)
    return(active_users.append(new_user, ignore_index=True))


def check_pattern(pattern, string):
    """ Check if valid pattern """

    print("Checking if pattern matches...")
    r = re.compile(pattern)
    if re.match(r, string):
        return(False)
    return(True)


def validate_row(data):
    """ Check if valid rows """

    print("Checking if row validates...")

    # storing all the columns heading in order
    column_order = ["ip", "date", "time", "zone", "cik", "accession",
                    "extention", "code", "size", "idx", "norefer", "noagent",
                    "find", "crawler", "browser"]
    field_index = {k: v for v, k in enumerate(column_order)}

    # check if number of columns are appropriate
    if len(data) != len(column_order):
        return(False)

    # defining descriptive variables
    ip = data[field_index["ip"]]
    date = data[field_index["date"]]
    time = data[field_index["time"]]
    cik = data[field_index["cik"]]
    accession = data[field_index["accession"]]
    extention = data[field_index["extention"]]

    return (ip, date, time, cik, accession, extention)


def main_analytics():
    """ The main function to integrate all above functions """

    # catching the exception
    try:

        # raise exception if system arguments are not equal to 4
        if len(sys.argv) != 4:
            raise(IndexError)

        # reading the path of input and output files
        log_file_path = sys.argv[1]
        inactivity_path = sys.argv[2]
        output_file_path = sys.argv[3]

        # File containing inactivity time
        print("Reading inactivity time")
        inactivity_file = open(inactivity_path, "r")
        inactivity_time = inactivity_file.read().strip()
        inactivity_file.close()

        # raising exception if inactivity time is not numeric
        if not inactivity_time.isdigit() or inactivity_time == "":
            raise(InactivityNumericError)

        # converting inactivity time to int
        inactivity_time = int(inactivity_time)
        print("Data Conversion Done.")
        
        # raising exception if inactivity time is not in range
        if not (inactivity_time >= 1 and inactivity_time <= 86400):
            raise(InactivityRangeError)

        # create empty dataframe for storing active users
        print("Creating empty dataframe for active users")
        cols = ["ip", "first_date_time", "last_date_time", "page_count"]
        active_users = pd.DataFrame([], columns=cols)

        # opening output file
        output_file = open(output_file_path, "w")

        # file containing log data
        with open(log_file_path, "r") as log_file:

            # skipping heading
            next(log_file)

            # reading data line by line
            for line in log_file:

                # split data on ","
                data = line.strip().split(",")

                # check if number of columns are appropriate
                checked_data = validate_row(data)
                if not checked_data:
                    raise(ColumnLengthError)

                # defining descriptive variables
                ip, date, time, cik, accession, extention = checked_data

                # checking for null values
                if check_null(ip, date, time, cik, accession, extention):
                    print("Found null values. Skipping...")
                    continue

                # checking for invalid ip
                if check_pattern(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\w{1,3}$", ip):
                    print("Found invalid ip. Skipping...")
                    continue

                # checking for invalid date
                if check_pattern(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("Found invalid date. Skipping...")
                    continue

                # checking for invalid time
                if check_pattern(r"^\d{2}:\d{2}:\d{2}$", time):
                    print("Found invalid time. Skipping...")
                    continue

                # splitting and converting date & time to datetime object
                date = [int(x.lstrip("0")) if x != "00" else int(x)
                        for x in date.split("-")]
                time = [int(x.lstrip("0")) if x != "00" else int(x)
                        for x in time.split(":")]
                date_time = datetime(date[0], date[1], date[2], time[0],
                                     time[1], time[2])

                # check if there is any active user
                if not active_users.empty:
                    for index, user in active_users.iterrows():
                        last_date = user["last_date_time"]

                        # checking for inactive users
                        if chk_time_diff(date_time, last_date) > \
                                inactivity_time:
                            print("Inactive user found")

                            user_ip = user["ip"]
                            first_date = user["first_date_time"]
                            page_count = user["page_count"]

                            # calculating session time
                            duration = chk_time_diff(last_date, first_date) + 1

                            # writing to output file
                            details = details = [user_ip, str(first_date),
                                                 str(last_date),
                                                 str(int(duration)),
                                                 str(int(page_count))]
                            write_output_data(output_file, details)
                            print("Data written to output file")

                            # delete inactive user from active user dataframe
                            active_users = active_users.drop(index, axis=0)

                # find if it's a active session
                row = check_active_user(active_users, ip)

                if row != []:
                    print("Active session found")
                    row = row[0]

                    # check for back log and skip the result
                    last_date = active_users.loc[row, "last_date_time"]
                    if chk_time_diff(date_time, last_date) < 0:
                        print("Back date found. SKipping...")

                    else:
                        # Update last_datetime & page_count for active session
                        active_users.loc[row, "last_date_time"] = date_time
                        active_users.loc[row, "page_count"] = \
                            active_users.loc[row, "page_count"] + 1

                else:
                    # adding new user to active session
                    print("New session Found")
                    details = [ip, date_time, date_time, 1]
                    active_users = add_new_user(active_users, details)

        # end active session after EOF
        if not active_users.empty:
            for index, user in active_users.iterrows():
                last_date = user["last_date_time"]
                user_ip = user["ip"]
                first_date = user["first_date_time"]
                page_count = user["page_count"]

                # calculating session time
                duration = chk_time_diff(last_date, first_date) + 1

                # writing to output file
                details = [user_ip, str(first_date), str(last_date),
                           str(int(duration)), str(int(page_count))]
                write_output_data(output_file, details)
                print("Data written to output file")

                # delete the inactive user from active user dataframe
                active_users = active_users.drop(index, axis=0)

        # closing output file
        output_file.close()

    # Handling the error related to System args
    except IndexError:
        print("Please provide correct command line arguments")

    # Handling the error related to Input/Output
    except IOError:
        print("Can't file the required files. Verify the path and files")

    # Handling the error related to Inactivity Time
    except InactivityNumericError:
        print("Inactivity Time is not numeric")

    # Handling the error realted to number of columns
    except ColumnLengthError:
        print("Number of Columns is not appropriate")
    
    # Handling error realted to range of Inactivity Time
    except InactivityRangeError:
        print("Inactivity Time is not between 1 to 86400 secs")

if __name__ == "__main__":
    main_analytics()
