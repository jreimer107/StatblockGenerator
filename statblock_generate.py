import csv
from argparse import ArgumentParser

import pyperclip

CSV_NAME = "monsterData.csv"
DELIMITER = ", "

TEMPLATE = """___
> ## %s
> *%s %s, %s*
> ___
> - **Armor Class** %s
> - **Hit Points** %s
> - **Speed** %s
>___n
>|STR|Dex|Con|INT|Wis|Cha|
>|:---:|:---:|:---:|:---:|:---:|:---:|
>|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|
>___
%s
> - **Challenge** %s (%s XP)
> ___
>
> ### Actions
> ***Multiattack.*** The Creature Name makes Number and type of attacks
>
> ***Ability Description.*** *Attack Style:* Attack Bonus to hit, Reach/Range, one target. *Hit:* Damage Damage Type damage
>
> ***General Ability Description.*** General Attack Description
"""

NAME = "Name"
SIZE = "Size"
TYPE = "Type"
ALIGNMENT = "Align."
ARMOR_CLASS = "AC"
HIT_POINTS = "HP"
SPEEDS = "Speeds"
STRENGTH = "STR"
DEXTERITY = "DEX"
CONSTITUTION = "CON"
INTELLIGENCE = "INT"
WISDOM = "WIS"
CHARISMA = "CHA"
SAVING_THROWS = "Sav. throws"
SKILLS = "Skills"
WEAKNESSES = "Weaknesses"
RESISTANCES = "Resistances"
DAMAGE_IMMUNITIES = "Damage Immunities"
CONDITION_IMMUNITIES = "Condition Immunities"
SENSES = "Senses"
LANGUAGES = "Languages"
CHALLENGE_RATING = "CR"
ADDITIONAL = "Additional"
SOURCE = "Source"

HEADERS = [
    NAME,
    SIZE,
    TYPE,
    ALIGNMENT,
    ARMOR_CLASS,
    HIT_POINTS,
    SPEEDS,
    STRENGTH,
    DEXTERITY,
    CONSTITUTION,
    INTELLIGENCE,
    WISDOM,
    CHARISMA,
    SAVING_THROWS,
    SKILLS,
    WEAKNESSES,
    RESISTANCES,
    DAMAGE_IMMUNITIES,
    CONDITION_IMMUNITIES,
    SENSES,
    LANGUAGES,
    CHALLENGE_RATING,
    ADDITIONAL,
    SOURCE,
]

STATS = [STRENGTH, DEXTERITY, CONSTITUTION, INTELLIGENCE, WISDOM, CHARISMA]

ABILITY_MODIFIERS = [
    "-5",
    "-5",
    "-4",
    "-4",
    "-3",
    "-3",
    "-2",
    "-2",
    "-1",
    "-1",
    "+0",
    "+0",
    "+1",
    "+1",
    "+2",
    "+2",
    "+3",
    "+3",
    "+4",
    "+4",
    "+5",
    "+5",
    "+6",
    "+6",
    "+7",
    "+7",
    "+8",
    "+8",
    "+9",
    "+9",
    "+10",
]

XP_BY_CR = {
    "0": "10",
    "1/8": "25",
    "1/4": "50",
    "1/2": "100",
    "1": "200",
    "2": "450",
    "3": "700",
    "4": "1,100",
    "5": "1,800",
    "6": "2,300",
    "7": "2,900",
    "8": "3,900",
    "9": "5,000",
    "10": "5,900",
    "11": "7,200",
    "12": "8,400",
    "13": "10,000",
    "14": "11,500",
    "15": "13,000",
    "16": "15,000",
    "17": "18,000",
    "18": "20,000",
    "19": "22,000",
    "20": "25,000",
    "21": "33,000",
    "22": "41,000",
    "23": "50,000",
    "24": "62,000",
    "25": "75,000",
    "26": "90,000",
    "27": "105,000",
    "28": "120,000",
    "29": "135,000",
    "30": "155,000",
}

proficiency = 4


def get_mod(stat: str) -> str:
    return ABILITY_MODIFIERS[int(stat)]


def get_saving_throw(nicename, value, proficiency):
    return "%s +%s" % (nicename, int(get_mod(value)) + proficiency)


def get_saving_throws(data: dict) -> str:
    throws = data[SAVING_THROWS]
    if not throws:
        return ""

    saving_throws = []
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
        with open(CSV_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[NAME] == target_monster:
                    data_row = row
                    break
    except FileNotFoundError:
        print("ERROR: CSV not found.")
        exit(1)

    if not data_row:
        print("Monster not found.")
        return

    formatted_string = format_data(row)
    print(formatted_string)
    pyperclip.copy(formatted_string)


if __name__ == "__main__":
    main()
