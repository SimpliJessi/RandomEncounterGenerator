import monster

thisMonster = [vars(monster.mon1), vars(monster.mon2), vars(monster.mon3), vars(monster.mon4)]

size = input("Enter Party Size: ")
level = input("Enter Player Level: ")
eDifficulty = int(level) * int(size)
for i in thisMonster:
    setattr(i, 'number', eDifficulty / i.cr)
print(f"Your party has {size} level {level} players.")

difficulty = input("How difficult do you want the encounter?")

print(thisMonster)