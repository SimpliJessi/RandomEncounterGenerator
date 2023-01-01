import json    # library that converts JSON objects into Python lists
import random  # random number generator
import math    # we're using the math.floor method here to round down

size = input("Enter Party Size: ")
level = input("Enter Player Level: ")
eDifficulty = int(level) * int(size)
print(f"Your party has {size} level {level} players.")

with open('./monster.json', 'r') as f:
    # We're pulling the monster.json file in as f, then running the json.load() method on it to convert it to a list
    data = json.load(f)
    # the len() method you're seeing here tells us how many objects (or monsters) are in our list/array
    arrLen = (len(data["angryThings"])-1)
    # the random.randint() method takes 2 arguments (lowNumber, highNumber) and returns a random number between the two
    rolled = random.randint(0, arrLen)
    num = str(rolled)
    # I'm looking for something specific in these arrays:
    # 1) THINK OF THIS AS A RUSSIAN NESTING DOLL, we're going through the layers until we get what we want
    # 2) data is the variable our array is assigned to
    # 3) everything in [brackets] is referring to a position in the array
    # 4) ["angryThings"] is the only object at this level of the array, and everything else is in it
    # 5) [rolled] is the random number returned earlier and this says to return the 1st, 2nd, 3rd, etc monster in the list
    # 6) ["race"] is the name of the attribute I want returned on this object
    encounter = data["angryThings"][rolled]["race"]
    amount = math.floor(eDifficulty / data["angryThings"][rolled]["cr"])

print(f"Your party encounters {amount} {encounter}(s)")

# difficulty = input("How difficult do you want the encounter?")

# print(data["angryThings"])