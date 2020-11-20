import csv
import re

reader = csv.reader(open("Monster Spreadsheet (D&D5e).csv", "r"))

with open("new.csv", "w", newline='') as file:
    writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        speeds = row[6].split(", ")
        for i in range(len(speeds)):
            speed = speeds[i]
            m = re.match("(\d+)\s+(\w+)", speed)
            if m:
                speed = m.group(2) + " " + m.group(1)

            speed += " ft."
            speeds[i] = speed
        row[6] = ", ".join(speeds)
        # if len(speeds) > 1:
        #     row[6] = '"' + row[6] + '"'
        # file.write(",".join(row) + "\n")
        writer.writerow(row)


