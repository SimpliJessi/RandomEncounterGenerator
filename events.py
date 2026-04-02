"""
Random Events module for the Random Encounter Generator.

Provides optional mid-encounter events such as environmental hazards,
traps, weather shifts, and other twists a GM can layer on top of combat.
Each event includes a name, description, and mechanical effect.
"""

import random


class RandomEvent:
    """A single random event that can occur during an encounter."""

    def __init__(self, name, description, effect, event_type):
        self.name = name
        self.description = description
        self.effect = effect
        self.event_type = event_type  # trap, hazard, weather, magical, social

    def __repr__(self):
        return f"RandomEvent('{self.name}', type='{self.event_type}')"


# ---------------------------------------------------------------------------
# Event Database
# ---------------------------------------------------------------------------

RANDOM_EVENTS = [
    # ---- Traps ----
    RandomEvent(
        "Pit Trap",
        "The ground gives way beneath a party member's feet, revealing a "
        "concealed pit lined with sharpened stakes.",
        "DC 13 Dexterity saving throw or fall 10 ft, taking 1d6 bludgeoning "
        "damage + 2d6 piercing damage from the stakes.",
        "trap"),
    RandomEvent(
        "Tripwire Crossbow",
        "A thin wire stretches across the path at ankle height. A click "
        "sounds as a hidden crossbow fires.",
        "DC 12 Perception to spot. If triggered: +8 to hit, 1d10+2 piercing "
        "damage to the triggering creature.",
        "trap"),
    RandomEvent(
        "Poison Dart Wall",
        "Tiny holes line the corridor walls. A pressure plate activates a "
        "volley of poison-tipped darts.",
        "DC 14 Dexterity saving throw. On fail: 1d4 piercing + 2d6 poison "
        "damage. On success: half damage.",
        "trap"),
    RandomEvent(
        "Swinging Blade",
        "A massive blade swings down from a concealed slot in the ceiling, "
        "slicing through the air at chest height.",
        "DC 13 Dexterity saving throw or take 3d6 slashing damage. "
        "On success: half damage.",
        "trap"),
    RandomEvent(
        "Net Trap",
        "A weighted net drops from above, entangling anyone underneath.",
        "DC 12 Dexterity saving throw or become restrained. DC 14 Strength "
        "check or slashing damage to the net (AC 10, 5 HP) to escape.",
        "trap"),
    RandomEvent(
        "Alarm Glyph",
        "A faintly glowing rune on the floor flares with light when "
        "stepped on, alerting every creature in the area.",
        "All enemies within 300 ft are alerted. Surprised creatures can no "
        "longer be surprised. Reinforcements may arrive in 1d4 rounds.",
        "trap"),
    RandomEvent(
        "Flame Jet",
        "Nozzles hidden in the walls blast gouts of fire across the room.",
        "DC 14 Dexterity saving throw or take 3d6 fire damage. "
        "On success: half damage. Flammable objects ignite.",
        "trap"),
    RandomEvent(
        "Bear Trap",
        "A rusted iron bear trap snaps shut on a party member's leg.",
        "DC 12 Perception to spot. If triggered: 1d8 piercing damage and "
        "the creature's speed becomes 0 until freed (DC 13 Strength).",
        "trap"),

    # ---- Environmental Hazards ----
    RandomEvent(
        "Ceiling Collapse",
        "Cracks spiderweb across the ceiling and chunks of stone come "
        "crashing down. Dust fills the air.",
        "Each creature in a 15 ft area makes a DC 14 Dexterity saving throw "
        "or takes 2d8 bludgeoning damage and is knocked prone.",
        "hazard"),
    RandomEvent(
        "Floor Collapse",
        "The floor cracks and buckles, opening a jagged chasm across "
        "the ground.",
        "DC 13 Dexterity saving throw or fall 20 ft, taking 2d6 bludgeoning "
        "damage. The gap is 10 ft wide — DC 12 Athletics to jump across.",
        "hazard"),
    RandomEvent(
        "Flooding",
        "Water surges into the area from a broken wall or underground "
        "spring, rapidly rising around everyone's ankles... then knees.",
        "The area becomes difficult terrain. After 3 rounds the water is "
        "3 ft deep — Small creatures must swim (DC 10 Athletics).",
        "hazard"),
    RandomEvent(
        "Rockslide",
        "A rumble from above signals a cascade of rocks and debris "
        "tumbling down the slope toward the party.",
        "DC 14 Dexterity saving throw or take 3d6 bludgeoning damage "
        "and be buried (restrained, DC 14 Strength to escape).",
        "hazard"),
    RandomEvent(
        "Sinkhole",
        "The earth suddenly gives way, pulling everything in a 10 ft "
        "radius downward into loose sand and gravel.",
        "DC 13 Strength saving throw or sink waist-deep (restrained). "
        "Each round: DC 13 Strength to pull free or sink further.",
        "hazard"),
    RandomEvent(
        "Toxic Spores",
        "Clusters of strange fungi burst open, releasing clouds of "
        "choking green spores into the air.",
        "Each creature within 15 ft makes a DC 13 Constitution saving "
        "throw or is poisoned for 1 minute. Repeat save each turn.",
        "hazard"),
    RandomEvent(
        "Unstable Ground",
        "The ground here is unstable — cracked ice, rotting wood flooring, "
        "or rain-softened earth threatens to give way.",
        "Difficult terrain. Any creature that Dashes must make a DC 12 "
        "Dexterity saving throw or fall prone.",
        "hazard"),
    RandomEvent(
        "Lava Fissure",
        "A crack splits the ground and molten rock bubbles up, casting "
        "an orange glow and brutal heat across the area.",
        "Any creature within 5 ft of the fissure takes 2d6 fire damage "
        "at the start of its turn. The fissure is 5 ft wide.",
        "hazard"),

    # ---- Weather Events ----
    RandomEvent(
        "Sudden Fog",
        "A thick, unnatural fog rolls in, reducing visibility to almost "
        "nothing in seconds.",
        "The area becomes heavily obscured. All attack rolls have "
        "disadvantage. Lasts 1d4+1 rounds.",
        "weather"),
    RandomEvent(
        "Lightning Strike",
        "Dark clouds gather with unnatural speed. A bolt of lightning "
        "slams into the ground near the combatants.",
        "One random creature makes a DC 15 Dexterity saving throw or "
        "takes 4d6 lightning damage. On success: half damage.",
        "weather"),
    RandomEvent(
        "Hailstorm",
        "Chunks of ice the size of fists begin pelting down from the sky.",
        "All creatures in the open take 1d4 bludgeoning damage at the "
        "start of each turn. Concentration checks required (DC 10).",
        "weather"),
    RandomEvent(
        "Gale-Force Wind",
        "A howling wind tears through the area, strong enough to stagger "
        "even the sturdiest warrior.",
        "Ranged attack rolls have disadvantage. Small creatures must make "
        "a DC 12 Strength save at the start of their turn or be pushed 10 ft.",
        "weather"),
    RandomEvent(
        "Earthquake Tremor",
        "The ground shakes violently. Cracks form, objects topple, and "
        "combatants struggle to keep their footing.",
        "DC 12 Dexterity saving throw or fall prone. Concentration checks "
        "at DC 12. Lasts 1 round, may recur on a d6 roll of 1-2.",
        "weather"),

    # ---- Magical Events ----
    RandomEvent(
        "Wild Magic Surge",
        "The weave of magic in this area is unstable. A surge of raw "
        "arcane energy erupts unpredictably.",
        "Roll on the Wild Magic Surge table, or: a random creature "
        "within 30 ft glows brightly (no stealth) for 1 minute.",
        "magical"),
    RandomEvent(
        "Anti-Magic Zone",
        "A shimmering field of null-magic flickers into existence, "
        "suppressing all magical effects within its bounds.",
        "A 20 ft radius sphere suppresses all magic for 1d4 rounds. "
        "Spells, magic items, and magical abilities do not function inside.",
        "magical"),
    RandomEvent(
        "Gravity Shift",
        "Gravity lurches sideways — or upward — sending loose objects "
        "and unsuspecting creatures tumbling.",
        "DC 14 Strength saving throw or be flung 15 ft in a random "
        "direction, taking 1d6 bludgeoning damage. Lasts 1 round.",
        "magical"),
    RandomEvent(
        "Arcane Explosion",
        "A dormant magical rune or artifact detonates, sending a "
        "shockwave of force energy through the area.",
        "All creatures within 20 ft make a DC 14 Constitution saving "
        "throw or take 3d6 force damage and are pushed 10 ft.",
        "magical"),
    RandomEvent(
        "Time Stutter",
        "Time skips and stutters. For a brief moment, some creatures "
        "freeze in place while others move freely.",
        "Roll initiative again. The top half of the order gains an extra "
        "turn this round; the bottom half loses their next turn.",
        "magical"),
    RandomEvent(
        "Illusory Terrain",
        "The environment shifts — walls appear where there are none, "
        "or the floor seems to vanish entirely.",
        "DC 15 Intelligence (Investigation) to disbelieve. Until then, "
        "the creature treats the illusion as real and acts accordingly.",
        "magical"),
    RandomEvent(
        "Haunting Whispers",
        "Ghostly voices fill the air, murmuring dark secrets and sowing "
        "doubt in the minds of all who hear them.",
        "DC 13 Wisdom saving throw or become frightened of the nearest "
        "enemy for 1 round. Creatures immune to charm are unaffected.",
        "magical"),

    # ---- Social / Situational Events ----
    RandomEvent(
        "Reinforcements Arrive",
        "A horn sounds in the distance. More enemies pour in from a "
        "side passage, doorway, or over the hill.",
        "1d4 additional creatures of the same type as the weakest enemy "
        "in the encounter arrive at the start of the next round.",
        "social"),
    RandomEvent(
        "Hostage Situation",
        "The enemies grab a bystander — a merchant, child, or fellow "
        "adventurer — and hold a blade to their throat.",
        "Attacking the hostage-holder has disadvantage. The hostage has "
        "AC 10 and 10 HP. If freed: grateful NPC, possible reward.",
        "social"),
    RandomEvent(
        "Enemy Surrender",
        "One of the enemies throws down its weapon and begs for mercy, "
        "offering information in exchange for its life.",
        "The GM decides what intel the creature has: enemy numbers, "
        "a hidden passage, treasure location, or a warning of danger ahead.",
        "social"),
    RandomEvent(
        "Bystander Interference",
        "A panicked civilian, stray animal, or oblivious merchant "
        "stumbles into the middle of the fight.",
        "The bystander occupies a space and moves randomly each round. "
        "Area effects risk hitting them. May provide useful distraction.",
        "social"),
    RandomEvent(
        "Rival Party",
        "Another group of adventurers appears on the scene, drawn by "
        "the sounds of combat. Their intentions are unclear.",
        "The rival party (3-4 NPCs) may help, hinder, or compete for "
        "loot. Roll a d6: 1-2 hostile, 3-4 neutral, 5-6 friendly.",
        "social"),
    RandomEvent(
        "Collapsing Structure",
        "A nearby wall, pillar, or archway groans and starts to give way. "
        "Someone could push it onto the enemies — or get crushed.",
        "As an action, a creature can push the structure (DC 14 Strength). "
        "Creatures in a 10 ft line take 4d6 bludgeoning damage (DC 13 Dex save halves).",
        "social"),
]

# Grouped by type for optional filtering
EVENT_TYPES = ["trap", "hazard", "weather", "magical", "social"]


def get_random_event(event_type=None):
    """
    Pick a random event. Optionally filter by event type.

    Parameters
    ----------
    event_type : str or None
        One of 'trap', 'hazard', 'weather', 'magical', 'social'.
        If None, picks from all events.

    Returns
    -------
    RandomEvent
    """
    pool = RANDOM_EVENTS
    if event_type and event_type.lower() in EVENT_TYPES:
        pool = [e for e in RANDOM_EVENTS if e.event_type == event_type.lower()]
    return random.choice(pool)


def format_event(event):
    """Return a formatted string for displaying a random event."""
    lines = [
        f"{'='*70}",
        f"  RANDOM EVENT — {event.event_type.upper()}",
        f"{'='*70}",
        f"",
        f"  {event.name}",
        f"",
        f"  {event.description}",
        f"",
        f"  Mechanical Effect:",
        f"    {event.effect}",
        f"",
        f"{'='*70}",
    ]
    return "\n".join(lines)
