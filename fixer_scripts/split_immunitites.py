import csv

from statblock_generate import *

IMMUNITIES = "Immunities"


CONDITIONS = [
    "blinded",
    "charmed",
    "deafened",
    "frightened",
    "grappled",
    "exhaustion",
    "incapacitated",
    "paralyzed",
    "petrified",
    "poisoned",
    "prone",
    "restrained",
    "stunned",
    "unconscious",
]

DAMAGE_TYPES = [
    "acid",
    "cold",
    "fire",
    "force",
    "lightning",
    "necrotic",
    "poison",
    "psychic",
    "radiant",
    "thunder",
    "bludgeoning",
    "piercing",
    "slashing",
    "nonadamantine",
    "nonmagical",
    "nonsilvered",
]


with open(DATA_CSV, "r") as file:
    reader = csv.DictReader(file)
    with open("new.csv", "w", newline="") as new_file:
        writer = csv.DictWriter(
            new_file, DATA_HEADERS, quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()
        for row in reader:
            immunities = row[IMMUNITIES].strip().split(DELIMITER)
            condition_immunities = []
            damage_immunities = []
            for immunity in immunities:
                if not immunity:
                    continue
                if immunity in CONDITIONS:
                    condition_immunities.append(immunity)
                elif immunity in DAMAGE_TYPES:
                    damage_immunities.append(immunity)
                else:
                    print(
                        f"Weird immunity {immunity} found in row {row[NAME]}, bytes: {immunity.encode()}"
                    )

            del row[IMMUNITIES]
            row[DAMAGE_IMMUNITIES] = DELIMITER.join(damage_immunities)
            row[CONDITION_IMMUNITIES] = DELIMITER.join(condition_immunities)
            writer.writerow(row)
