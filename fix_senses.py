import csv

from statblock_generate import *

with open(DATA_CSV, "r") as file:
    reader = csv.DictReader(file)
    with open("new.csv", "w", newline="") as new_file:
        writer = csv.DictWriter(new_file, DATA_HEADERS, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in reader:
            senses = row[SENSES]
            if senses:
                senses = senses.split(DELIMITER)
                for i in range(len(senses)):
                    senses[i] = senses[i].lower() + " ft."
                senses = DELIMITER.join(senses)
                row[SENSES] = senses
            writer.writerow(row)