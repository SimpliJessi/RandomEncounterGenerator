"""
Monster data model and database for the Random Encounter Generator.
Contains monsters across a wide range of Challenge Ratings with
attributes useful for encounter building and scenario generation.
"""

import random


class Monster:
    """Represents a single monster type with all relevant stats and flavor."""

    def __init__(self, name, cr, monster_type, environments, hp, ac,
                 attacks=None, description="", abilities=None):
        self.name = name
        self.cr = cr
        self.monster_type = monster_type
        self.environments = environments if isinstance(environments, list) else [environments]
        self.hp = hp
        self.ac = ac
        self.attacks = attacks or []
        self.description = description
        self.abilities = abilities or []

    def __repr__(self):
        return (f"Monster(name='{self.name}', CR={self.cr}, "
                f"type='{self.monster_type}', HP={self.hp}, AC={self.ac})")

    def summary(self):
        """Return a formatted summary string for display."""
        lines = [
            f"  {self.name} (CR {self.cr})",
            f"    Type: {self.monster_type.title()} | HP: {self.hp} | AC: {self.ac}",
            f"    Environments: {', '.join(e.title() for e in self.environments)}",
        ]
        if self.attacks:
            lines.append(f"    Attacks: {', '.join(self.attacks)}")
        if self.abilities:
            lines.append(f"    Abilities: {', '.join(self.abilities)}")
        if self.description:
            lines.append(f"    Description: {self.description}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Monster Database — organized by CR
# ---------------------------------------------------------------------------

MONSTER_DATABASE = [
    # ---- CR 1/8 (0.125) ----
    Monster("Kobold", 0.125, "humanoid",
            ["cave", "mountain", "forest", "dungeon"],
            5, 12, ["Dagger", "Sling"],
            "Small, cunning reptilian creatures that rely on traps and numbers.",
            ["Pack Tactics", "Sunlight Sensitivity"]),
    Monster("Giant Rat", 0.125, "beast",
            ["cave", "dungeon", "swamp", "urban"],
            7, 12, ["Bite"],
            "Disease-carrying rodents of unusual size.",
            ["Pack Tactics", "Keen Smell"]),
    Monster("Stirge", 0.125, "beast",
            ["cave", "swamp", "forest", "dungeon"],
            2, 14, ["Blood Drain"],
            "Bat-like parasites that latch onto victims and drain their blood.",
            ["Blood Drain"]),
    Monster("Bandit", 0.125, "humanoid",
            ["forest", "grassland", "hill", "urban", "road"],
            11, 12, ["Scimitar", "Light Crossbow"],
            "Common outlaws and highway robbers looking for easy marks."),

    # ---- CR 1/4 (0.25) ----
    Monster("Goblin", 0.25, "humanoid",
            ["cave", "forest", "hill", "grassland", "dungeon"],
            7, 15, ["Scimitar", "Shortbow"],
            "Small, green-skinned menaces that attack in groups.",
            ["Nimble Escape"]),
    Monster("Skeleton", 0.25, "undead",
            ["dungeon", "cave", "graveyard", "ruins"],
            13, 13, ["Shortsword", "Shortbow"],
            "Animated bones bound by dark necromantic energy."),
    Monster("Zombie", 0.25, "undead",
            ["dungeon", "graveyard", "swamp", "ruins"],
            22, 8, ["Slam"],
            "Shambling corpses that refuse to stay dead.",
            ["Undead Fortitude"]),
    Monster("Wolf", 0.25, "beast",
            ["forest", "grassland", "hill", "mountain", "tundra"],
            11, 13, ["Bite"],
            "Pack predators that coordinate their attacks.",
            ["Pack Tactics", "Keen Hearing and Smell"]),
    Monster("Giant Centipede", 0.25, "beast",
            ["cave", "dungeon", "swamp", "forest"],
            4, 13, ["Bite (poison)"],
            "Massive arthropod with venomous mandibles."),
    Monster("Pixie", 0.25, "fey",
            ["forest", "fey_wild"],
            1, 15, ["None (spellcaster)"],
            "Tiny mischievous fey with innate spellcasting.",
            ["Invisibility", "Druidcraft", "Confusion"]),

    # ---- CR 1/2 (0.5) ----
    Monster("Orc", 0.5, "humanoid",
            ["cave", "mountain", "grassland", "hill", "dungeon"],
            15, 13, ["Greataxe", "Javelin"],
            "Brutish warriors driven by conquest and bloodlust.",
            ["Aggressive"]),
    Monster("Hobgoblin", 0.5, "humanoid",
            ["cave", "grassland", "dungeon", "hill"],
            11, 18, ["Longsword", "Longbow"],
            "Disciplined goblinoid soldiers who fight in formation.",
            ["Martial Advantage"]),
    Monster("Shadow", 0.5, "undead",
            ["dungeon", "graveyard", "ruins", "cave"],
            16, 12, ["Strength Drain"],
            "Dark incorporeal undead that sap the life from the living.",
            ["Amorphous", "Shadow Stealth", "Strength Drain"]),
    Monster("Gnoll", 0.5, "humanoid",
            ["grassland", "hill", "forest", "desert"],
            22, 15, ["Spear", "Bite", "Longbow"],
            "Hyena-headed marauders that revel in slaughter.",
            ["Rampage"]),
    Monster("Swarm of Insects", 0.5, "beast",
            ["cave", "swamp", "forest", "dungeon"],
            22, 12, ["Bites"],
            "A writhing mass of biting, stinging bugs.",
            ["Swarm"]),

    # ---- CR 1 ----
    Monster("Bugbear", 1, "humanoid",
            ["cave", "forest", "dungeon", "mountain"],
            27, 16, ["Morningstar", "Javelin"],
            "Hulking goblinoid ambush predators.",
            ["Surprise Attack", "Brute"]),
    Monster("Ghoul", 1, "undead",
            ["dungeon", "graveyard", "ruins", "cave"],
            22, 12, ["Bite", "Claws (paralyze)"],
            "Ravenous undead that feast on the flesh of the living.",
            ["Paralyzing Touch"]),
    Monster("Giant Spider", 1, "beast",
            ["cave", "dungeon", "forest", "swamp"],
            26, 14, ["Bite (poison)", "Web"],
            "Horse-sized arachnids that spin webs to trap prey.",
            ["Spider Climb", "Web Sense", "Web Walker"]),
    Monster("Dire Wolf", 1, "beast",
            ["forest", "hill", "mountain", "tundra"],
            37, 14, ["Bite"],
            "Enormous wolves that knock down and savage their prey.",
            ["Pack Tactics", "Keen Hearing and Smell"]),
    Monster("Animated Armor", 1, "construct",
            ["dungeon", "ruins", "castle"],
            33, 18, ["Slam"],
            "A suit of armor animated by magic to guard a location.",
            ["Antimagic Susceptibility", "False Appearance"]),
    Monster("Harpy", 1, "monstrosity",
            ["mountain", "hill", "forest", "coast"],
            38, 11, ["Claws", "Club"],
            "Winged creature with an enchanting, deadly song.",
            ["Luring Song"]),

    # ---- CR 2 ----
    Monster("Ogre", 2, "giant",
            ["cave", "hill", "mountain", "forest", "swamp"],
            59, 11, ["Greatclub", "Javelin"],
            "Dim-witted but immensely strong brutes.",
            []),
    Monster("Ghast", 2, "undead",
            ["dungeon", "graveyard", "ruins", "cave"],
            36, 13, ["Bite", "Claws (paralyze)"],
            "A more powerful, stench-emitting variant of the ghoul.",
            ["Stench", "Paralyzing Touch", "Turning Defiance"]),
    Monster("Ankheg", 2, "monstrosity",
            ["grassland", "forest", "hill"],
            39, 14, ["Bite", "Acid Spray"],
            "Burrowing insectoid ambush predators with acid spit.",
            ["Acid Spray"]),
    Monster("Mimic", 2, "monstrosity",
            ["dungeon", "cave", "ruins", "castle"],
            58, 12, ["Pseudopod", "Bite"],
            "Shape-shifting creature that disguises itself as objects.",
            ["Shapechanger", "Adhesive", "False Appearance"]),
    Monster("Gargoyle", 2, "elemental",
            ["mountain", "urban", "castle", "ruins"],
            52, 15, ["Bite", "Claws"],
            "Stone creatures that perch motionless until prey draws near.",
            ["False Appearance"]),
    Monster("Ettercap", 2, "monstrosity",
            ["forest", "cave", "swamp"],
            44, 13, ["Bite (poison)", "Claws", "Web"],
            "Spider-loving creatures that set web traps for travelers.",
            ["Spider Climb", "Web Sense", "Web Walker"]),

    # ---- CR 3 ----
    Monster("Owlbear", 3, "monstrosity",
            ["forest", "hill", "cave"],
            59, 13, ["Beak", "Claws"],
            "Ferocious bear-owl hybrid with insatiable hunger.",
            ["Keen Sight and Smell"]),
    Monster("Werewolf", 3, "humanoid",
            ["forest", "hill", "urban", "mountain"],
            58, 12, ["Bite (lycanthropy)", "Claws"],
            "A cursed shapechanger that transforms under the moon.",
            ["Shapechanger", "Damage Immunity (nonmagical)"]),
    Monster("Minotaur", 3, "monstrosity",
            ["dungeon", "cave", "ruins"],
            76, 14, ["Greataxe", "Gore"],
            "Bull-headed brute that charges through labyrinthine lairs.",
            ["Charge", "Labyrinthine Recall", "Reckless"]),
    Monster("Phase Spider", 3, "monstrosity",
            ["dungeon", "cave", "forest"],
            32, 13, ["Bite (poison)"],
            "A spider that shifts between the material and ethereal planes.",
            ["Ethereal Jaunt", "Spider Climb"]),
    Monster("Wight", 3, "undead",
            ["dungeon", "graveyard", "ruins", "cave", "tundra"],
            45, 14, ["Longsword", "Longbow", "Life Drain"],
            "An undead warrior animated by hatred of the living.",
            ["Life Drain", "Sunlight Sensitivity"]),

    # ---- CR 4 ----
    Monster("Ettin", 4, "giant",
            ["hill", "mountain", "cave"],
            85, 12, ["Battleaxe", "Morningstar"],
            "A two-headed giant — each head with its own personality.",
            ["Two Heads", "Wakeful"]),
    Monster("Ghost", 4, "undead",
            ["dungeon", "graveyard", "ruins", "castle", "swamp"],
            45, 11, ["Withering Touch"],
            "A tormented spirit bound to the mortal world.",
            ["Etherealness", "Horrifying Visage", "Possession"]),
    Monster("Banshee", 4, "undead",
            ["forest", "ruins", "swamp", "graveyard"],
            58, 12, ["Corrupting Touch"],
            "The wailing spirit of a fallen elf maiden.",
            ["Wail", "Horrifying Visage", "Incorporeal Movement"]),
    Monster("Lamia", 4, "monstrosity",
            ["desert", "ruins"],
            97, 13, ["Claws", "Dagger", "Intoxicating Touch"],
            "A lion-bodied temptress that lures the unwary to ruin.",
            ["Innate Spellcasting", "Intoxicating Touch"]),

    # ---- CR 5 ----
    Monster("Troll", 5, "giant",
            ["cave", "mountain", "swamp", "forest"],
            84, 15, ["Bite", "Claws"],
            "Lanky, regenerating green-skinned brutes vulnerable to fire.",
            ["Regeneration", "Keen Smell"]),
    Monster("Bulette", 5, "monstrosity",
            ["grassland", "hill", "mountain"],
            94, 17, ["Bite", "Deadly Leap"],
            "A massive armored predator that burrows and leaps from the earth.",
            ["Standing Leap"]),
    Monster("Salamander", 5, "elemental",
            ["cave", "mountain", "dungeon"],
            90, 15, ["Spear", "Tail"],
            "Fiery serpentine creatures from the Elemental Plane of Fire.",
            ["Heated Body", "Heated Weapons"]),
    Monster("Hill Giant", 5, "giant",
            ["hill", "mountain", "grassland", "forest"],
            105, 13, ["Greatclub", "Rock"],
            "Enormous, gluttonous giants that eat anything they can catch.",
            []),
    Monster("Wraith", 5, "undead",
            ["dungeon", "graveyard", "ruins"],
            67, 13, ["Life Drain"],
            "A powerful incorporeal undead born of dark emotion.",
            ["Incorporeal Movement", "Life Drain", "Create Specter"]),

    # ---- CR 6 ----
    Monster("Chimera", 6, "monstrosity",
            ["mountain", "hill", "grassland"],
            114, 14, ["Bite", "Horns", "Claws", "Fire Breath"],
            "A three-headed beast: lion, dragon, and goat.",
            ["Fire Breath"]),
    Monster("Cyclops", 6, "giant",
            ["cave", "coast", "mountain", "grassland"],
            138, 14, ["Greatclub", "Rock"],
            "One-eyed giant with poor depth perception but great strength.",
            ["Poor Depth Perception"]),
    Monster("Wyvern", 6, "dragon",
            ["mountain", "hill", "coast", "grassland"],
            110, 13, ["Bite", "Claws", "Stinger (poison)"],
            "A two-legged dragon-kin with a venomous tail stinger.",
            []),
    Monster("Drider", 6, "monstrosity",
            ["dungeon", "cave"],
            123, 19, ["Longsword", "Longbow", "Bite"],
            "A cursed drow transformed into a spider-centaur hybrid.",
            ["Fey Ancestry", "Innate Spellcasting", "Spider Climb"]),

    # ---- CR 7 ----
    Monster("Stone Giant", 7, "giant",
            ["mountain", "cave", "hill"],
            126, 17, ["Greatclub", "Rock"],
            "Artistic, reclusive giants who hurl boulders with precision.",
            ["Stone Camouflage"]),
    Monster("Young Black Dragon", 7, "dragon",
            ["swamp", "cave", "dungeon"],
            127, 18, ["Bite", "Claws", "Acid Breath"],
            "A young dragon with a cruel temperament and acid breath.",
            ["Amphibious", "Acid Breath"]),
    Monster("Oni", 7, "giant",
            ["forest", "urban", "mountain"],
            110, 16, ["Glaive", "Claw"],
            "Shape-shifting ogre mages that prey on humanoids.",
            ["Innate Spellcasting", "Shapechanger", "Regeneration"]),
    Monster("Shield Guardian", 7, "construct",
            ["dungeon", "castle", "ruins"],
            142, 17, ["Fist"],
            "A magically bound construct that protects its master.",
            ["Bound", "Regeneration", "Shield", "Spell Storing"]),

    # ---- CR 8 ----
    Monster("Frost Giant", 8, "giant",
            ["tundra", "mountain", "cave"],
            138, 15, ["Greataxe", "Rock"],
            "Viking-like giants who dwell in frozen wastes.",
            []),
    Monster("Assassin", 8, "humanoid",
            ["urban", "dungeon", "forest", "road"],
            78, 15, ["Shortsword (poison)", "Light Crossbow (poison)"],
            "A deadly professional killer skilled in poison.",
            ["Assassinate", "Evasion", "Sneak Attack"]),
    Monster("Hydra", 8, "monstrosity",
            ["swamp", "cave", "coast"],
            172, 15, ["Bite (x5)"],
            "A multi-headed serpent that grows two heads for each one severed.",
            ["Multiple Heads", "Reactive Heads", "Wakeful"]),
    Monster("Young Green Dragon", 8, "dragon",
            ["forest", "swamp"],
            136, 18, ["Bite", "Claws", "Poison Breath"],
            "A cunning young dragon that delights in manipulation.",
            ["Amphibious", "Poison Breath"]),

    # ---- CR 9 ----
    Monster("Fire Giant", 9, "giant",
            ["mountain", "cave", "dungeon"],
            162, 18, ["Greatsword", "Rock"],
            "Militaristic giants who forge weapons in volcanic fortresses.",
            []),
    Monster("Treant", 9, "plant",
            ["forest"],
            138, 16, ["Slam", "Rock"],
            "Ancient, awakened tree guardians of the deep forest.",
            ["Animate Trees", "False Appearance", "Siege Monster"]),
    Monster("Young Blue Dragon", 9, "dragon",
            ["desert", "coast", "mountain"],
            152, 18, ["Bite", "Claws", "Lightning Breath"],
            "A vain young dragon that lurks beneath desert sands.",
            ["Lightning Breath"]),
    Monster("Bone Devil", 9, "fiend",
            ["dungeon", "ruins"],
            142, 19, ["Claws", "Sting (poison)"],
            "A skeletal fiend that enforces infernal contracts.",
            ["Devil's Sight", "Magic Resistance"]),

    # ---- CR 10 ----
    Monster("Young Red Dragon", 10, "dragon",
            ["mountain", "cave", "hill"],
            178, 18, ["Bite", "Claws", "Fire Breath"],
            "An arrogant and destructive young dragon of terrible power.",
            ["Fire Breath"]),
    Monster("Stone Golem", 10, "construct",
            ["dungeon", "castle", "ruins"],
            178, 17, ["Slam", "Slow"],
            "A massive stone automaton animated by powerful magic.",
            ["Immutable Form", "Magic Resistance", "Magic Weapons"]),
    Monster("Aboleth", 10, "aberration",
            ["cave", "dungeon", "coast"],
            135, 17, ["Tentacle", "Tail", "Enslave"],
            "An ancient aquatic horror with psionic domination powers.",
            ["Amphibious", "Mucous Cloud", "Probing Telepathy", "Enslave"]),

    # ---- CR 11 ----
    Monster("Roc", 11, "monstrosity",
            ["mountain", "coast"],
            248, 15, ["Beak", "Talons"],
            "A gargantuan bird of prey that can carry off elephants.",
            ["Keen Sight"]),
    Monster("Djinni", 11, "elemental",
            ["desert", "mountain", "coast"],
            161, 17, ["Scimitar", "Whirlwind"],
            "Noble elemental beings of air with vast magical power.",
            ["Innate Spellcasting", "Elemental Demise"]),
    Monster("Horned Devil", 11, "fiend",
            ["dungeon", "ruins", "mountain"],
            178, 18, ["Fork", "Tail", "Hurl Flame"],
            "A fearsome winged devil armed with an infernal fork.",
            ["Devil's Sight", "Magic Resistance"]),

    # ---- CR 13 ----
    Monster("Adult White Dragon", 13, "dragon",
            ["tundra", "mountain", "cave"],
            200, 18, ["Bite", "Claws", "Tail", "Cold Breath"],
            "A savage adult dragon that hunts in frozen wastelands.",
            ["Cold Breath", "Frightful Presence", "Ice Walk"]),
    Monster("Beholder", 13, "aberration",
            ["cave", "dungeon"],
            180, 18, ["Bite", "Eye Rays"],
            "A floating sphere of eyes with devastating magical eye rays.",
            ["Antimagic Cone", "Eye Rays"]),
    Monster("Storm Giant", 13, "giant",
            ["mountain", "coast", "cave"],
            230, 16, ["Greatsword", "Rock", "Lightning Strike"],
            "The wisest and most powerful of the true giants.",
            ["Amphibious", "Innate Spellcasting", "Lightning Strike"]),

    # ---- CR 15 ----
    Monster("Adult Green Dragon", 15, "dragon",
            ["forest", "swamp"],
            207, 19, ["Bite", "Claws", "Tail", "Poison Breath"],
            "A scheming adult dragon that delights in corruption.",
            ["Poison Breath", "Frightful Presence", "Legendary Actions"]),
    Monster("Purple Worm", 15, "monstrosity",
            ["cave", "dungeon", "desert"],
            247, 18, ["Bite", "Tail Stinger (poison)"],
            "A titanic burrowing worm that swallows creatures whole.",
            ["Tunneler"]),
    Monster("Mummy Lord", 15, "undead",
            ["desert", "dungeon", "ruins"],
            97, 17, ["Rotting Fist"],
            "A mummy empowered by dark gods with dread sorcery.",
            ["Spellcasting", "Rejuvenation", "Legendary Actions"]),

    # ---- CR 17 ----
    Monster("Adult Red Dragon", 17, "dragon",
            ["mountain", "cave", "hill"],
            256, 19, ["Bite", "Claws", "Tail", "Fire Breath"],
            "The most fearsome and greedy of the chromatic dragons.",
            ["Fire Breath", "Frightful Presence", "Legendary Actions"]),
    Monster("Death Knight", 17, "undead",
            ["dungeon", "ruins", "graveyard"],
            180, 20, ["Longsword", "Hellfire Orb"],
            "A fallen paladin cursed to serve in undeath.",
            ["Spellcasting", "Marshal Undead", "Hellfire Orb"]),

    # ---- CR 20 ----
    Monster("Ancient White Dragon", 20, "dragon",
            ["tundra", "mountain", "cave"],
            333, 20, ["Bite", "Claws", "Tail", "Cold Breath"],
            "A millennia-old dragon of terrible power and primal fury.",
            ["Cold Breath", "Frightful Presence", "Legendary Actions"]),
    Monster("Pit Fiend", 20, "fiend",
            ["dungeon", "ruins"],
            300, 19, ["Bite", "Claws", "Mace", "Tail"],
            "The generals of the Nine Hells — supreme in infernal might.",
            ["Fear Aura", "Magic Resistance", "Innate Spellcasting"]),

    # ---- CR 21+ ----
    Monster("Lich", 21, "undead",
            ["dungeon", "ruins", "castle"],
            135, 17, ["Paralyzing Touch"],
            "An undead archmage who achieved immortality through a phylactery.",
            ["Legendary Actions", "Spellcasting", "Rejuvenation"]),
    Monster("Ancient Black Dragon", 21, "dragon",
            ["swamp", "cave"],
            367, 22, ["Bite", "Claws", "Tail", "Acid Breath"],
            "An ancient swamp dragon vicious beyond measure.",
            ["Acid Breath", "Frightful Presence", "Legendary Actions"]),
    Monster("Ancient Red Dragon", 24, "dragon",
            ["mountain", "cave"],
            546, 22, ["Bite", "Claws", "Tail", "Fire Breath"],
            "The apex predator of the world — an ancient red wyrm.",
            ["Fire Breath", "Frightful Presence", "Legendary Actions"]),
    Monster("Tarrasque", 30, "monstrosity",
            ["any"],
            676, 25, ["Bite", "Claws", "Horns", "Tail", "Swallow"],
            "The most feared monster in existence — a force of nature.",
            ["Legendary Resistance", "Magic Resistance", "Reflective Carapace",
             "Siege Monster", "Frightful Presence"]),
]


def get_all_environments():
    """Return a sorted set of all unique environments in the database."""
    envs = set()
    for m in MONSTER_DATABASE:
        for e in m.environments:
            if e != "any":
                envs.add(e)
    return sorted(envs)


def get_monsters_by_cr(cr):
    """Return all monsters matching a specific CR."""
    return [m for m in MONSTER_DATABASE if m.cr == cr]


def get_monsters_by_environment(environment):
    """Return all monsters found in a given environment."""
    env = environment.lower()
    return [m for m in MONSTER_DATABASE if env in m.environments]


def get_monsters_in_cr_range(cr_min, cr_max):
    """Return all monsters within a CR range (inclusive)."""
    return [m for m in MONSTER_DATABASE if cr_min <= m.cr <= cr_max]


def filter_monsters(cr_min=0, cr_max=30, environments=None, monster_types=None):
    """Filter monsters by CR range, environments, and/or type."""
    results = MONSTER_DATABASE
    results = [m for m in results if cr_min <= m.cr <= cr_max]
    if environments:
        env_set = {e.lower() for e in environments}
        results = [m for m in results if env_set & set(m.environments)]
    if monster_types:
        type_set = {t.lower() for t in monster_types}
        results = [m for m in results if m.monster_type.lower() in type_set]
    return results
