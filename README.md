# Random Encounter Generator

A command-line tool for Game Masters to generate balanced, narrative-rich encounters for tabletop and text-based RPGs.

## Features

- **Party Configuration** — Set party size (1–10 players) and level (1–20)
- **4 Difficulty Tiers** — Easy, Medium, Hard, and Deadly, each with proper XP budgets
- **CR-Balanced Encounters** — Uses standard XP thresholds per player level, encounter multipliers for monster count, and smart allocation across mixed monster groups
- **55+ Monsters** — Database spanning CR 1/8 (Kobolds, Giant Rats) through CR 30 (Tarrasque), with stats, attacks, abilities, and descriptions
- **Creature Count Control** — Specify an exact number of creatures (1–20), or let the generator decide automatically
- **Environment Filtering** — Optionally filter encounters by 16 environments: cave, forest, swamp, dungeon, desert, mountain, coast, urban, ruins, graveyard, tundra, castle, road, grassland, hill, and fey wild
- **Random Events** — Optional mid-encounter twists: traps (pit traps, tripwires, flame jets), environmental hazards (ceiling/floor collapse, flooding, rockslides), weather (fog, lightning, hailstorms), magical effects (wild magic surges, anti-magic zones), and social events (reinforcements, hostage situations, rival parties)
- **Scenario Narratives** — Auto-generated scene-setting text with environment intros, monster-type encounter hooks, and difficulty-flavored atmosphere
- **Replayable** — Each run produces a different randomized encounter with a "generate another?" loop

## Requirements

- Python 3.6+

No external dependencies required.

## Usage

```bash
python main.py
```

The tool will walk you through:

1. **Party size** — How many players?
2. **Party level** — What level is the party?
3. **Difficulty** — Easy, Medium, Hard, or Deadly
4. **Creature count** — Pick an exact number or press Enter for auto
5. **Environment** (optional) — Filter monsters by terrain type
6. **Random event** (optional) — Add a trap, hazard, or twist
7. **Output** — A balanced encounter with monster details, a narrative scenario, and an optional random event

### Example Output

```
======================================================================
  Party: 4 players at level 5
  Difficulty: Hard
  XP Budget: 3,000
======================================================================

  -- ENCOUNTER --
  Difficulty : HARD
  XP Budget  : 3,000
  Raw XP     : 2,250
  Adjusted XP: 3,375

  Monsters:
    1x Owlbear  (CR 3, 700 XP each)
    2x Hobgoblin  (CR 0.5, 100 XP each)
    1x Minotaur  (CR 3, 700 XP each)

======================================================================
  ENCOUNTER SCENARIO
======================================================================

  Setting: Cave

  A vast cavern opens before you, stalactites hanging like jagged teeth
  from the ceiling high above.

  A monstrous predator has made its lair here and views your party as
  its next meal.

  You face an Owlbear — Ferocious bear-owl hybrid with insatiable
  hunger; and 2 Hobgoblins — Disciplined goblinoid soldiers who fight
  in formation; and a Minotaur — Bull-headed brute that charges through
  labyrinthine lairs.

  This is a dangerous fight. One wrong move could mean disaster for
  the party.

======================================================================

======================================================================
  RANDOM EVENT — HAZARD
======================================================================

  Ceiling Collapse

  Cracks spiderweb across the ceiling and chunks of stone come
  crashing down. Dust fills the air.

  Mechanical Effect:
    Each creature in a 15 ft area makes a DC 14 Dexterity saving
    throw or takes 2d8 bludgeoning damage and is knocked prone.

======================================================================
```

## Project Structure

```
RandomEncounterGenerator/
├── main.py        # CLI interface and main application loop
├── monster.py     # Monster class, database (55+ creatures), and query helpers
├── encounter.py   # XP-budget encounter balancer with CR/difficulty math
├── scenario.py    # Narrative scenario writer (intros, hooks, atmosphere)
├── events.py      # Random events: traps, hazards, weather, magical, social
└── README.md
```

## How Encounter Balancing Works

The generator uses standard TTRPG encounter math:

1. **XP Budget** is calculated from party size × per-player threshold for the chosen difficulty
2. **Monster Selection** picks 1–3 monster types from the database, filtered by CR cap and optional environment
3. **Encounter Multiplier** adjusts the effective XP based on total monster count (more monsters = harder than raw XP suggests)
4. **Budget Fitting** iteratively adds or removes monsters to keep adjusted XP within ~20% of the target budget

### Difficulty Thresholds (per player)

| Level | Easy | Medium | Hard | Deadly |
|-------|------|--------|------|--------|
| 1     | 25   | 50     | 75   | 100    |
| 5     | 250  | 500    | 750  | 1,100  |
| 10    | 600  | 1,200  | 1,900| 2,800  |
| 15    | 1,400| 2,800  | 4,300| 6,400  |
| 20    | 2,800| 5,700  | 8,500| 12,700 |

## License

This project is open source. Use it however you like for your games.
