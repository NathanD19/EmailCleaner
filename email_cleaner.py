import os
from datetime import datetime
from errors_dict import get_errors_dict
import sys
import re

# Welcome
welcome = """
Email Clean And Export

1. Enter a csv file with emails you want to upload.
2. Wait for the process to finish. It will do the following:
    - Removes duplicate emails from using the emails.csv as a base.
    - Cleans up common email mistakes ands removed invalid email combinations
    - Adds new emails to base emails.csv
    - Exports clean emails as a csv file
3. Upload csv files
"""

print(welcome)

# Get Import File
file_to_import = input("Enter your csv file name (Do not include '.csv'): ")

# Check if file exists
try:
    f = open(file_to_import + ".csv")
    print("'" + file_to_import + ".csv' Found!")
    f.close()
except FileNotFoundError:
    print("'" + file_to_import + ".csv' does not exist! Exiting...")
    exit()

exiting_lines = []
new_lines = []

# Open email archive file
with open("emails.csv", "r") as file:
    for existing in file:
        exiting_lines.append(existing.strip("\n"))

# Open emails to upload to mailchip
with open(file_to_import + ".csv", "r") as file:
    for new in file:
        new_lines.append(new.strip("\n"))

# Remove duplicates that appear in upload csv
s1 = set(exiting_lines)
s2 = set(new_lines)
cleaned = list(s2.difference(s1))

print("Removing Duplicates...")

# Fix common email errors
print("Fixing Email Errors...")
fixed_count = 0
i = 0
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

for line in cleaned:
    # Get info after @
    email_split_end = line.split("@", 1)[1]
    email_split_start = line.split("@", 1)[0]
    i += 1
    sys.stdout.write(str(i) + "/" + str(len(cleaned)))
    sys.stdout.flush()
    sys.stdout.write("\r")

    for key in get_errors_dict().keys():
        # Compare Email for Errors
        if key == email_split_end:
            line = email_split_start + "@" + get_errors_dict().get(key)
            fixed_count += 1
            continue

    # Remove invalid emails
    if not EMAIL_REGEX.match(line):
        cleaned.remove(line)

# Export Emails
print("Exporting Emails...")
today = datetime.now()
file_name = today.strftime("%Y-%m-%d_%H-%M-%S") + "_cleaned.csv"
with open(file_name, "w") as out:
    for line in cleaned:
        out.write(line + "\n")

# Append new emails to archive csv
print("Adding " + str(len(cleaned)) + " new emails to archive csv...")
with open("emails.csv", "a") as emails:
    for line in cleaned:
        emails.write(line + "\n")

print(
    "The file '"
    + file_name
    + "' has been generated with cleaned list of emails to import. "
    + str(fixed_count)
    + " Emails Fixed."
)

input("Press any key to exit...")
