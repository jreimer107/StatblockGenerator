import csv
from sys import argv
import pyperclip

ABILITY_MODIFIERS = ["-5", "-5", "-4", "-4", "-3", "-3", "-2", "-2", "-1", "-1", "+0", "+0", "+1", "+1", "+2", "+2", "+3", "+3", "+4", "+4", "+5", "+5", "+6", "+6", "+7", "+7", "+8", "+8", "+9", "+9", "+10"]

def get_mod(stat: str) -> str:
    return (ABILITY_MODIFIERS[int(stat)])

target_monster = None
if len(argv) >= 2:
    target_monster = argv[1]
else:
    target_monster = input("Enter a monster name: ")

reader = csv.reader(open("Monster Spreadsheet (D&D5e).csv", "r"))
for row in reader:
    if row[0] == target_monster:
        name, size, monster_type, align, ac, hp, speeds, strength, dex, con, intel, wis, cha, saving_throws, skills, wri, senses, languages, cr, additional, font, additional_info, author = row;
        
        formatted_string = "___\n\
> ## %s\n\
>*%s %s, %s*\n\
> ___\n\
> - **Armor Class** %s\n\
> - **Hit Points** %s\n\
> - **Speed** %s\n\
>___\n\
>|STR|DEX|CON|INT|WIS|CHA|\n\
>|:---:|:---:|:---:|:---:|:---:|:---:|\n\
>|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|%s (%s)|\n\
>___\n\
> - **Saving Throws** %s\n\
> - **Skills** %s\n\
> - **Damage Vulnerabilities** damage_vulnerabilities\n\
> - **Damage Resistances** Resistances\n\
> - **Damage Immunities** Damage_Immunities\n\
> - **Condition Immunities** condition_Immunities\n\
> - **Senses** %s\n\
> - **Languages** %s\n\
> - **Challenge** %s and XP\n\
> ___\n\
>\n\
> ### Actions\n\
> ***Multiattack.*** The Creature Name makes Number and type of attacks\n\
>\n\
> ***Ability Description.*** *Attack Style:* Attack Bonus to hit, Reach/Range, one target. *Hit:* Damage Damage Type damage\n\
>\n\
> ***General Ability Description.*** General Attack Description" % (name, size, monster_type, align, ac, hp, speeds, strength, get_mod(strength), dex, get_mod(dex), con, get_mod(con), intel, get_mod(intel), wis, get_mod(wis), cha, get_mod(cha), saving_throws, skills, senses, languages, cr)

        print(formatted_string)
        pyperclip.copy(formatted_string)

        exit()

print("Monster not found.")

