import csv

from constants import *

with open(DATA_CSV, "r", newline="") as file, open("new.csv", "w", newline="") as new_file:
    reader = csv.DictReader(file)
    writer = csv.DictWriter(new_file, DATA_HEADERS, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for row in reader:
        split = row[CHALLENGE_RATING].split("-")
        if len(split) > 1:
            cr = f"1/{int(split[0])}"
            row[CHALLENGE_RATING] = cr
        writer.writerow(row)
