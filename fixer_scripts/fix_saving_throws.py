import csv

COLUMN_INDEX = 13
CSV_NAME = "monsterData.csv"

reader = csv.reader(open(CSV_NAME, "r"))

with open("new.csv", "w", newline='') as file:
    writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        row[COLUMN_INDEX] = ", ".join(map(lambda x: x.capitalize(), row[COLUMN_INDEX].split(", ")))
        writer.writerow(row)