DATA_CSV = "monsterData.csv"
FEATURES_CSV = "Creature Features.csv"
NAME_CODES_CSV = "Name Codes.csv"
CUSTOM_NAMES_CSV = "Custom Names.csv"
DELIMITER = ", "

TEMPLATE = """___
> ## %s
> *%s %s, %s*
> ___
> - **Armor Class** %s
> - **Hit Points** %s
> - **Speed** %s
>___
>|STR|DEX|CON|INT|WIS|CHA|
>|:---:|:---:|:---:|:---:|:---:|:---:|
>|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|
>___
%s
> - **Challenge** %s (%s XP)
> ___
>
%s
> ### Actions
> ***Multiattack.*** The Creature Name makes Number and type of attacks
>
> ***Ability Description.*** *Attack Style:* Attack Bonus to hit, Reach/Range, one target. *Hit:* Damage Damage Type damage
>
> ***General Ability Description.*** General Attack Description
"""

# Data Headers
NAME = "Name"
FAMILY = "Family"
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
FEATURES = "Features"
SOURCE = "Source"

DATA_HEADERS = [
    NAME,
    FAMILY,
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
    FEATURES,
    SOURCE,
]

# Feature headers
DESCRIPTION = "Description"

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
