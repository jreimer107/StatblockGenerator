import csv
from argparse import ArgumentParser
from fractions import Fraction
from constants import *

import pyperclip

FEATURES_LIST = {}


def fix_cr(data: dict):
    data[CHALLENGE_RATING] = Fraction(data[CHALLENGE_RATING])


def get_mod(stat: str) -> str:
    return ABILITY_MODIFIERS[int(stat)]


def get_saving_throw(nicename, value, proficiency):
    return "%s +%s" % (nicename, int(get_mod(value)) + proficiency)


def get_saving_throws(data: dict) -> str:
    throws = data[SAVING_THROWS]
    if not throws:
        return ""

    saving_throws = []
    proficiency = PROFICIENCY_BY_CR[data[CHALLENGE_RATING]]
    for throw in throws.split(", "):
        modifier = data[throw.upper()]
        saving_throws.append(get_saving_throw(throw, modifier, proficiency))

    return ", ".join(saving_throws)


def get_detail_block(data: dict):
    # > - **Saving Throws** %s
    # > - **Skills** %s
    # > - **Damage Vulnerabilities** damage_vulnerabilities
    # > - **Damage Resistances** Resistances
    # > - **Damage Immunities** Damage_Immunities
    # > - **Condition Immunities** Condition_Immunities
    # > - **Senses** %s
    # > - **Languages** %s
    ret = ""
    saving_throws = get_saving_throws(data)
    if saving_throws:
        ret += f"> - **Saving Throws** {saving_throws}\n"

    if data[WEAKNESSES]:
        ret += f"> - **Damage Vulnerabilities** {data[WEAKNESSES]}\n"

    resistances = data[RESISTANCES]
    if resistances:
        ret += f"> - **Damage Resistances** {resistances}\n"

    damage_immunities = data[DAMAGE_IMMUNITIES]
    if damage_immunities:
        ret += f"> - **Damage Immunities** {damage_immunities}\n"

    condition_immunitites = data[CONDITION_IMMUNITIES]
    if condition_immunitites:
        ret += f"> - **Condition Immunities** {condition_immunitites}\n"

    passive_perception = f"passive Perception {10 + int(get_mod(data[WISDOM]))}"
    senses = DELIMITER.join([data[SENSES], passive_perception])
    ret += f"> - **Senses** {senses}\n"

    languages = data[LANGUAGES]
    ret += "> - **Languages** "
    if languages:
        ret += f"{languages}"
    else:
        ret += "--"

    return ret


def build_features_list():
    global FEATURES_LIST

    with open(FEATURES_CSV, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            FEATURES_LIST[row[NAME]] = row


def get_feature_block(row: dict) -> str:
    features = row[FEATURES]
    if not features:
        return ""

    features = features.split(DELIMITER)
    if not len(FEATURES_LIST):
        build_features_list()
        print(len(FEATURES_LIST))

    ret = ""
    creature_name = row[NAME]
    for feature in features:
        if feature not in FEATURES_LIST:
            print(f"Feature {feature} not in feature table.")
            ret += f"> ***{feature}.***\n>"
            continue

        description: str = FEATURES_LIST[feature][DESCRIPTION]
        description = description.replace("$", creature_name.lower())
        ret += f"> ***{feature}.*** {description}\n>"

    return ret


def format_data(row):
    strength = row[STRENGTH]
    dexterity = row[DEXTERITY]
    constitution = row[CONSTITUTION]
    intelligence = row[INTELLIGENCE]
    wisdom = row[WISDOM]
    charisma = row[CHARISMA]

    formatted_string = TEMPLATE % (
        row[NAME],
        row[SIZE],
        row[TYPE],
        row[ALIGNMENT],
        row[ARMOR_CLASS],
        row[HIT_POINTS],
        row[SPEEDS],
        strength,
        get_mod(strength),
        dexterity,
        get_mod(dexterity),
        constitution,
        get_mod(constitution),
        intelligence,
        get_mod(intelligence),
        wisdom,
        get_mod(wisdom),
        charisma,
        get_mod(charisma),
        get_detail_block(row),
        row[CHALLENGE_RATING],
        XP_BY_CR[row[CHALLENGE_RATING]],
        get_feature_block(row),
    )
    return formatted_string


def main():
    parser = ArgumentParser(
        prog="Generate Stat Block",
        description="Given a monster/NPC name, generates a GMBinder stat block. Prints the stat block and copies it to clipboard.",
    )
    parser.add_argument("monster_name", type=str, help="The monster's name.")
    args = parser.parse_args()

    target_monster = args.monster_name
    if not target_monster:
        target_monster = input("Enter a monster name: ")

    data_row = None
    try:
        with open(DATA_CSV, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[NAME] == target_monster:
                    data_row = row
                    break
    except FileNotFoundError:
        print("ERROR: CSV not found.")
        return

    if not data_row:
        print("Monster not found.")
        return

    fix_cr(row)
    formatted_string = format_data(row)
    print(formatted_string)
    pyperclip.copy(formatted_string)


if __name__ == "__main__":
    main()
