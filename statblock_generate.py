import csv
from argparse import ArgumentParser
from fractions import Fraction
from constants import *

import pyperclip

FEATURES_LIST = {}

args = None
monster_data = {}

def fix_cr(data: dict):
    data[CHALLENGE_RATING] = Fraction(data[CHALLENGE_RATING])


def set_proficiency(data):
    cr = data[CHALLENGE_RATING]
    data[PROFICIENCY_BONUS] = PROFICIENCY_BY_CR[cr]


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

    skills = None
    if data[SKILLS]:
        skills = data[SKILLS].split(DELIMITER)
        proficiency = data[PROFICIENCY_BONUS]
        formatted_skills = []
        for skill in skills:
            stat = SKILL_MAP[skill]
            modifier = int(get_mod(data[stat]))
            formatted_skills.append(f"{skill} +{modifier + proficiency}")

        ret += f"> - **Skills** {DELIMITER.join(formatted_skills)}\n"

    if data[WEAKNESSES]:
        ret += f"> - **Damage Vulnerabilities** {data[WEAKNESSES]}\n"

    resistances = data[RESISTANCES]
    if resistances:
        ret += f"> - **Damage Resistances** {resistances}\n"

    damage_immunities = data[DAMAGE_IMMUNITIES]
    if damage_immunities:
        ret += f"> - **Damage Immunities** {damage_immunities}\n"

    condition_immunities = data[CONDITION_IMMUNITIES]
    if condition_immunities:
        ret += f"> - **Condition Immunities** {condition_immunities}\n"

    passive_perception = 10 + int(get_mod(data[WISDOM]))
    if skills and PERCEPTION in skills:
        passive_perception += proficiency
    passive_perception = f"passive Perception {passive_perception}"
    senses = data[SENSES]
    if senses:
        senses = DELIMITER.join([senses, passive_perception])
    else:
        senses = passive_perception
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

    creature_name = row[NAME]
    formatted_features = []
    for feature in features:
        if feature not in FEATURES_LIST:
            print(f"Feature {feature} not in feature table.")
            formatted_features.append(f"> ***{feature}.***")
            continue

        description: str = FEATURES_LIST[feature][DESCRIPTION]
        description = description.replace("$", creature_name.lower())
        formatted_features.append(f"> ***{feature}.*** {description}")
    return "\n>\n".join(formatted_features)


def format_data(row):
    strength = row[STRENGTH]
    dexterity = row[DEXTERITY]
    constitution = row[CONSTITUTION]
    intelligence = row[INTELLIGENCE]
    wisdom = row[WISDOM]
    charisma = row[CHARISMA]

    return TEMPLATE % (
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


def preprocess_data(data: dict):
    fix_cr(data)
    set_proficiency(data)


def parse_args():
    global args

    parser = ArgumentParser(
        prog="Generate Stat Block",
        description="Given a monster/NPC name, generates a GMBinder stat block. Prints the stat block and copies it to clipboard.",
    )
    parser.add_argument("monster_name", type=str, help="The monster's name.", nargs="?")
    args = parser.parse_args()


def fuzzy_monster_search(query: str):
    query_parts = query.split()
    close_results = []
    best_matching = 0
    for monster_name in monster_data:
        # Find the number of words matching the query
        monster_parts = monster_name.split()
        matching_parts = 0
        for query_part in query_parts:
            if query_part in monster_parts:
                matching_parts += 1
        
        # If the number of matching words is equal to or better than our best, record it.
        if matching_parts == 0:
            continue
        elif matching_parts == best_matching:
            close_results.append(monster_name)
        elif matching_parts > best_matching:
            close_results = [monster_name]
            best_matching = matching_parts
    
    if not len(close_results):
        print("No similar monsters found, try again.")
        return

    print("Similar monsters found:")
    for i in range(len(close_results)):
        print(f"{i}\t{close_results[i]}")

    try:
        selection = int(input("Select a monster index. "))
    except ValueError:
        print("Bad input.")
        return

    if not selection:
        print("Nothing selected.")
        return

    if selection not in range(len(close_results)):
        print("Bad input.")
        return

    selected_monster = close_results[selection]
    return selected_monster

def get_target_monster():
    # Consume arg
    target_monster = args.monster_name
    args.monster_name = None
        
    if not target_monster:
        target_monster = input("Enter a monster name: ")

    if not target_monster:
        print("Nothing entered, exiting.")
        exit()
    elif target_monster not in monster_data:
        target_monster = fuzzy_monster_search(target_monster)

    return target_monster


def load_moster_data():
    try:
        with open(DATA_CSV, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                monster_data[row[NAME]] = row
    except FileNotFoundError:
        print("ERROR: CSV not found.")
        exit()

def get_monster_data(target_monster: str) -> dict:
    global monster_data

    if target_monster in monster_data:
        return monster_data[target_monster]
    print("Monster not found.")


def main():
    parse_args()
    load_moster_data()

    target_monster_data = None
    while not target_monster_data:
        target_monster = get_target_monster()
        target_monster_data = get_monster_data(target_monster)

    preprocess_data(target_monster_data)
    formatted_string = format_data(target_monster_data)
    print(formatted_string)
    pyperclip.copy(formatted_string)


if __name__ == "__main__":
    main()
