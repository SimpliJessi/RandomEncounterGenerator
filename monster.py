class Monster():
    def __init__(self, race):
        self.race = race


mon1 = Monster('goblin')

setattr(mon1, 'race', 'Goblin')
setattr(mon1, 'cr', 1/8)
setattr(mon1, 'type', 'humanoid')
setattr(mon1, 'environment', 'Hill Cave Grasslands Mountains'.split())

mon2 = Monster('orc')

setattr(mon2, 'race', 'Orc')
setattr(mon2, 'cr', 1/2)
setattr(mon2, 'type', 'humanoid')
setattr(mon2, 'environment', 'Hill Cave Grasslands Mountains'.split())

mon3 = Monster('troll')

setattr(mon3, 'race', 'Troll')
setattr(mon3, 'cr', 1/2)
setattr(mon3, 'type', 'humanoid')
setattr(mon3, 'environment', 'Hill Cave Grasslands Mountains'.split())

mon4 = Monster('dragon')

setattr(mon4, 'race', 'Dragon')
setattr(mon4, 'cr', 20)
setattr(mon4, 'type', 'dragon')
setattr(mon4, 'environment', 'Mountains'.split())

monster = [vars(mon1), vars(mon2), vars(mon3), vars(mon4)]

print(*monster, sep = "\n")
