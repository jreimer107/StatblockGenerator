import csv
from sys import argv
import pyperclip
from varname import nameof

TEMPLATE = "___\n\
> ## %s\n\
>*%s %s, %s*\n\
> ___\n\
> - **Armor Class** %s\n\
> - **Hit Points** %s\n\
> - **Speed** %s\n\
>___\n\
>|STR|Dex|Con|INT|Wis|Cha|\n\
>|:---:|:---:|:---:|:---:|:---:|:---:|\n\
>|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|\n\
>___\n\
> - **Saving Throws** %s\n\
> - **Skills** %s\n\
> - **Damage Vulnerabilities** damage_vulnerabilities\n\
> - **Damage Resistances** Resistances\n\
> - **Damage Immunities** Damage_Immunities\n\
> - **Condition Immunities** Condition_Immunities\n\
> - **Senses** %s\n\
> - **Languages** %s\n\
> - **Challenge** %s (%s XP)\n\
> ___\n\
>\n\
> ### Actions\n\
> ***Multiattack.*** The Creature Name makes Number and type of attacks\n\
>\n\
> ***Ability Description.*** *Attack Style:* Attack Bonus to hit, Reach/Range, one target. *Hit:* Damage Damage Type damage\n\
>\n\
> ***General Ability Description.*** General Attack Description"

ABILITY_MODIFIERS = ["-5", "-5", "-4", "-4", "-3", "-3", "-2", "-2", "-1", "-1", "+0", "+0", "+1", "+1",
                     "+2", "+2", "+3", "+3", "+4", "+4", "+5", "+5", "+6", "+6", "+7", "+7", "+8", "+8", "+9", "+9", "+10"]
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
    "30": "155,000"
}


def get_mod(stat: str) -> str:
    return (ABILITY_MODIFIERS[int(stat)])

def get_saving_throw(nicename, value, proficiency):
    print(locals())
    return "%s +%s" % (nicename, int(get_mod(value)) + proficiency)

def get_saving_throws(throws: str, Str, Dex, Con, Int, Wis, Cha) -> str:
    modifiers = locals();
    proficiency = 4
    saving_throws = [];
    for throw in throws.split(", "):
        saving_throws.append(get_saving_throw(throw, modifiers[throw], proficiency))

    return ", ".join(saving_throws)


def main():
    target_monster = None
    if len(argv) >= 2:
        target_monster = argv[1]
    else:
        target_monster = input("Enter a monster name: ")

    reader = None
    try:
        reader = csv.reader(open("monsterData.csv", "r"))
    except FileNotFoundError:
        print("ERROR: CSV not found.")
        exit(1)

    for row in reader:
        if row[0] == target_monster:
            name, size, monster_type, align, ac, hp, speeds, Str, Dex, Con, Int, Wis, Cha, saving_throws, skills, wri, senses, languages, cr, additional, font, additional_info, author = row
            formatted_string = TEMPLATE % (name, size, monster_type, align, ac, hp, speeds, 
                Str, get_mod(Str), Dex, get_mod(Dex), Con, get_mod(Con), Int, get_mod(Int), Wis, get_mod(Wis), Cha, get_mod(Cha), 
                get_saving_throws(saving_throws, Str, Dex, Con, Int, Wis, Cha),
                skills, senses, languages, cr, XP_BY_CR[cr])

            print(formatted_string)
            pyperclip.copy(formatted_string)
            return


print("Monster not found.")

if __name__ == "__main__":
    main()
