from datetime import datetime

date_string = "17/07/2023"
datetime_string = "2023-07-17 13:51:35"

# Convert the date string to datetime object
date_object = datetime.strptime(date_string, "%d/%m/%Y")

# Convert the datetime string to datetime object
datetime_object = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
# Compare the dates
if date_object.date() == datetime_object.date():
    print("The dates are equal.")
else:
    print("The dates are not equal.")
