import csv
import re

from statblock_generate import *

WRI = "WRI"


def find_wri(wri, pattern):
    match = re.match(f"(\w+){pattern}$", wri)
    if not match:
        return None
    return match.group(1)


with open(CSV_NAME, "r") as file:
    reader = csv.DictReader(file)
    with open("new.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, HEADERS, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in reader:
            wri_col = row[WRI]
            split_wri = {"weak": [], "res": [], "immu": []}
            wris = wri_col.split(DELIMITER)
            for wri in wris:
                for pattern in ["weak", "res", "immu"]:
                    match = re.match(f"(\w+){pattern}$", wri)
                    if match:
                        split_wri[pattern].append(match.group(1).lower())

            del row[WRI]
            row[WEAKNESSES] = DELIMITER.join(split_wri["weak"])
            row[RESISTANCES] = DELIMITER.join(split_wri["res"])
            row[IMMUNITIES] = DELIMITER.join(split_wri["immu"])

            writer.writerow(row)
