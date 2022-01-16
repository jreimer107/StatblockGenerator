import csv

from constants import *

name_codes = {}
custom_names = {}

def get_dictwriter(file):
    return csv.DictWriter(file, DATA_HEADERS, quotechar='"', quoting=csv.QUOTE_MINIMAL)

with open(DATA_CSV, "r", newline="") as file, open("new.csv", "w", newline="") as new_file, open(
    NAME_CODES_CSV, "r+", newline=""
) as codes_file, open(CUSTOM_NAMES_CSV, "r+", newline="") as custom_file:
    # Load codes
    codes_reader = csv.reader(codes_file)
    for row in codes_reader:
        name_codes[f"{row[0]}-{row[1]}"] = row[2]
    print(name_codes)

    custom_reader = csv.reader(custom_file)
    for row in custom_reader:
        custom_names[row[0]] = row[1]

    reader = csv.DictReader(file)
    writer = get_dictwriter(new_file)
    writer.writeheader()
    codes_writer = csv.writer(codes_file, DATA_HEADERS, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    custom_writer = csv.writer(custom_file, DATA_HEADERS, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        full_name = row[NAME]
        parts = full_name.split(DELIMITER)
        nparts = len(parts)
        if nparts == 1:
            name = full_name
        else:
            family = parts[0]
            code_key = f"{family}-{nparts}"
            if code_key in name_codes:
                name_code = name_codes[code_key]
            else:
                print(f"did not find key {code_key}")
                for i in range(len(parts)):
                    print(f"{i}\t{parts[i]}")

                name_code = input("Name code? ('c' for custom) ")
                name_codes[code_key] = name_code
                codes_writer.writerow([family, nparts, name_code])

            if name_code == "c":
                if full_name in custom_names:
                    name = custom_names[full_name]
                else:
                    name = input(f"Enter custom name for {full_name}: ")
                    custom_writer.writerow([full_name, name])
            else:
                try:
                    name = " ".join([parts[int(num)] for num in name_code])
                except Exception as e:
                    print(parts)
                    print(name_code)
                    exit()
                print(name)

            row[NAME] = name
            row[FAMILY] = family

        writer.writerow(row)
