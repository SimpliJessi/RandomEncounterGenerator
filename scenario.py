"""
Scenario Writer for the Random Encounter Generator.

Generates narrative descriptions for encounters based on the monsters,
environment, and difficulty. Provides GMs with a ready-to-read scene
they can present to players.
"""

import random


# ---------------------------------------------------------------------------
# Environment descriptions
# ---------------------------------------------------------------------------

ENVIRONMENT_INTROS = {
    "cave": [
        "Deep within a winding cave system, the air is damp and the only light comes from faintly glowing fungi clinging to the walls.",
        "The tunnel narrows ahead, and the sound of dripping water echoes off the stone. Shadows dance at the edge of your torchlight.",
        "A vast cavern opens before you, stalactites hanging like jagged teeth from the ceiling high above.",
        "The cave smells of mildew and something else — something alive. Claw marks score the walls.",
    ],
    "forest": [
        "The canopy overhead is so thick that only thin shafts of light reach the forest floor. The undergrowth rustles with unseen movement.",
        "Ancient trees tower around you, their gnarled roots erupting from the mossy ground. The forest is unnervingly quiet.",
        "A narrow game trail winds through dense woodland. Broken branches and disturbed earth suggest something large passed this way recently.",
        "Mist clings to the forest floor as twilight settles in. The calls of night creatures begin to fill the air.",
    ],
    "mountain": [
        "The rocky mountain path clings to a sheer cliff face. Wind howls through the crags, and loose stones skitter into the void below.",
        "You reach a high mountain plateau strewn with boulders. The thin air carries a faint, acrid scent.",
        "Snow dusts the jagged peaks above as you traverse a narrow mountain pass. Something watches from the rocks above.",
        "A mountain cave mouth yawns open beside the trail, warm air rising from its depths despite the freezing wind.",
    ],
    "swamp": [
        "Murky water rises to your knees as you wade through the swamp. The stench of decay hangs heavy in the humid air.",
        "Dead trees jut from the brackish water like skeletal fingers. Bubbles break the surface nearby — too large to be natural.",
        "A thick fog blankets the marshland, limiting visibility to a few dozen feet. Strange lights flicker in the distance.",
        "The ground squelches with every step, threatening to swallow your boots. Insects swarm in clouds around your head.",
    ],
    "dungeon": [
        "The dungeon corridor stretches ahead, its stone walls lined with rusty sconces and faded tapestries. The air smells of dust and old death.",
        "You push open a heavy iron door and enter a wide chamber. Broken furniture and scattered bones suggest this room was once occupied.",
        "Torchlight reveals ancient runes carved into the dungeon walls. Something has scratched over them with desperate, frantic marks.",
        "The floor is slick with moisture. Ahead, the passageway splits into three directions, each disappearing into darkness.",
    ],
    "grassland": [
        "Tall grass ripples in the wind across the open plains. The horizon is vast and empty — but you sense you are not alone.",
        "A gentle hill rises ahead, and atop it you spot the remains of an old campfire. The embers are still warm.",
        "The grasslands stretch endlessly under a wide sky. A distant rumble — thunder, or something else — rolls across the plain.",
        "Wildflowers dot the meadow, but the beauty is deceptive. Trampled earth and dark stains in the grass tell a different story.",
    ],
    "hill": [
        "Rolling hills spread before you, dotted with scraggly bushes and weathered standing stones.",
        "From the hilltop you can see for miles — and you can see the dust cloud rising from whatever is headed your way.",
        "A ring of ancient stones crowns the hilltop. The air inside the circle feels heavy, charged with old magic.",
        "The hillside is pockmarked with burrow entrances. Some are disturbingly large.",
    ],
    "desert": [
        "Sand dunes stretch to the horizon under a merciless sun. Heat shimmers blur your vision.",
        "A ruined oasis lies ahead — the water has dried up, but something still lurks among the crumbling walls.",
        "The desert wind shifts the sands, briefly revealing bleached bones and the corner of a buried structure.",
        "Night falls over the desert and the temperature plummets. Strange sounds carry on the cold wind.",
    ],
    "coast": [
        "Waves crash against the rocky shore. Sea caves dot the cliff face, dark mouths open to the tide.",
        "A wrecked ship lies half-submerged in the shallows, its hull cracked open. Movement stirs within.",
        "The beach is littered with driftwood and debris. Tracks in the wet sand lead toward a sea cave.",
        "Salt spray stings your face as you walk the coastal path. The surf below is unusually violent.",
    ],
    "urban": [
        "The city alley is narrow and dark, hemmed in by leaning buildings. A flickering lantern is the only light.",
        "The marketplace has long since closed for the night. Empty stalls cast long shadows in the moonlight.",
        "You hear a scream from a side street, cut short. The city watch is nowhere to be seen.",
        "An abandoned warehouse looms ahead. The door hangs ajar, and faint sounds of movement come from within.",
    ],
    "ruins": [
        "Crumbling stone walls are all that remain of what was once a grand structure. Vines and moss claim what time has not.",
        "The ruins are eerily silent. Faded murals on the walls depict scenes of a forgotten civilization.",
        "Rubble chokes the entrance to the ruined temple. Beyond it, something glints in the gloom.",
        "Broken columns and shattered archways line what was once a great hall. The floor is littered with debris — and bones.",
    ],
    "graveyard": [
        "Fog rolls between the crooked headstones. An iron gate creaks open in the wind behind you.",
        "The graveyard is old — many of the markers are worn smooth and unreadable. Fresh dig marks scar one plot.",
        "A mausoleum stands at the center of the cemetery, its heavy door slightly ajar. Cold air drifts from within.",
        "The moon casts long shadows through the graveyard. You hear the scrape of stone on stone from somewhere nearby.",
    ],
    "tundra": [
        "An endless expanse of frozen wasteland stretches before you. The wind cuts through your clothing like a blade.",
        "Snow crunches underfoot as you cross the tundra. Ahead, dark shapes move against the white landscape.",
        "A blizzard howls around you, reducing visibility to mere feet. Something is moving in the whiteout.",
        "The frozen ground is cracked and uneven. Steam rises from a fissure ahead, and with it, a sulfurous stench.",
    ],
    "castle": [
        "The castle's great hall is cold and dark. Tattered banners hang from the vaulted ceiling.",
        "You ascend a spiral staircase within the castle tower. The higher you climb, the more the stones tremble.",
        "The castle courtyard is overgrown and littered with the rusted remains of weapons and armor.",
        "Moonlight streams through a shattered stained-glass window into the castle's chapel. The pews have been overturned.",
    ],
    "road": [
        "The trade road stretches through open country. An overturned wagon blocks the path ahead.",
        "You round a bend in the road and find a makeshift barricade of felled trees. This is an ambush point.",
        "The road passes through a narrow ravine. The walls on either side would make perfect cover for attackers.",
        "A crossroads lies ahead, marked by a weathered signpost. Something is nailed to it — a warning.",
    ],
    "fey_wild": [
        "The colors here are wrong — too vivid, too saturated. The air hums with unseen magic.",
        "Flowers that shouldn't exist bloom in impossible patterns. The trees seem to lean in, listening.",
        "A ring of mushrooms marks the border of a fey crossing. Beyond it, reality bends.",
        "Laughter echoes from nowhere and everywhere. The path you walked moments ago has vanished behind you.",
    ],
}

# Fallback for environments not explicitly listed
DEFAULT_INTROS = [
    "The terrain ahead shifts and changes. You sense danger lurking nearby.",
    "Something is wrong. The air feels charged with tension, and you ready your weapons.",
    "The landscape around you feels unfamiliar and threatening. You are not alone.",
]


# ---------------------------------------------------------------------------
# Encounter hooks — why the party encounters these creatures
# ---------------------------------------------------------------------------

ENCOUNTER_HOOKS = {
    "humanoid": [
        "A raiding party has set up an ambush along the path, targeting travelers for supplies and coin.",
        "These creatures have been terrorizing a nearby settlement. The locals have put out a plea for help.",
        "A war band is on the march, and your party has stumbled into their territory.",
        "Scouts have been sent ahead to investigate intruders — you. They do not look friendly.",
        "A territorial dispute between factions has spilled into violence, and you're caught in the middle.",
    ],
    "undead": [
        "A dark ritual has raised the dead from their rest. They shamble toward you with hollow eyes.",
        "The ground trembles and bony hands claw through the earth. Something has disturbed the dead.",
        "An ancient curse has bound these spirits to this place. They attack anyone who draws near.",
        "A necromancer's failed experiment has unleashed these horrors. They are mindless and hungry.",
        "These undead guard something — a tomb, a relic, a passage. They will not let you pass.",
    ],
    "beast": [
        "A pack of predators has caught your scent and is closing in from multiple directions.",
        "These creatures are starving and desperate — they attack anything that moves.",
        "You've stumbled too close to a nest. The creatures rush to defend their young.",
        "A territorial beast blocks the only path forward. It will not back down.",
        "Unnatural behavior drives these beasts to attack — something is influencing them.",
    ],
    "monstrosity": [
        "A monstrous predator has made its lair here and views your party as its next meal.",
        "Rumors of a terrible beast have plagued this region. You've just found it — or it found you.",
        "The creature charges from concealment, driven by rage and hunger.",
        "This monstrosity was conjured or created long ago. It still follows its last command: destroy intruders.",
        "A bounty has been placed on this creature. It won't be collected easily.",
    ],
    "dragon": [
        "The dragon descends from the sky with a thunderous roar, drawn by the glint of your equipment.",
        "You've entered the dragon's territory, and it demands tribute — or your lives.",
        "A young dragon has been driven from its lair by a rival and is in a foul temper.",
        "The dragon has been terrorizing the region. Today, it turns its attention to you.",
        "Ancient and cunning, the dragon has been expecting you. It speaks before it strikes.",
    ],
    "giant": [
        "The earth shakes with heavy footsteps. A towering figure looms over the landscape ahead.",
        "Giants have claimed this area as their own. They hurl boulders first and ask questions never.",
        "A giant foraging party spots you and decides you'd make a fine snack.",
        "The giant is enraged — someone has stolen from its hoard, and you look like likely suspects.",
        "A giant demands a toll for passage through its domain. The price is unreasonable.",
    ],
    "elemental": [
        "A rift between planes has torn open, and elemental fury pours through.",
        "The elemental creature was bound here as a guardian. Your presence has triggered it.",
        "Raw elemental energy crackles in the air as a living manifestation of the elements takes shape.",
        "A sorcerer's lost elemental servant, freed from its bindings, lashes out at everything nearby.",
    ],
    "fiend": [
        "A crack in reality has let an infernal creature slip into the mortal world. It reeks of brimstone.",
        "The fiend was summoned by a foolish warlock who lost control. Now it hunts freely.",
        "A portal to the lower planes flickers nearby. The fiend emerged from it moments ago.",
        "The fiend has been stalking your party, waiting for the right moment to strike.",
    ],
    "construct": [
        "Ancient magical guardians activate as you enter the chamber, stone eyes glowing with eldritch light.",
        "A construct left behind by its creator still faithfully guards its post — against you.",
        "The mechanical creature whirs to life, its programming clear: eliminate all trespassers.",
    ],
    "aberration": [
        "Reality warps around you as an alien presence makes itself known. Nothing about this creature is natural.",
        "A being from the Far Realm has breached the boundary between worlds. Madness radiates from it.",
        "The aberration has lurked here for eons, and your intrusion has disturbed its dark meditation.",
    ],
    "fey": [
        "Mischievous laughter rings through the air as fey creatures materialize around you.",
        "You've wandered into fey territory. The inhabitants are not pleased — and their pranks are deadly.",
        "A fey creature appears, offering a deal. But nothing in the Feywild comes without a twisted cost.",
    ],
    "plant": [
        "What you took for ordinary vegetation stirs and rises, revealing its true, hostile nature.",
        "The ancient guardian of this grove awakens. It considers your presence a threat to its domain.",
        "Roots and vines writhe with unnatural life, lashing out at anything that comes too close.",
    ],
}

DEFAULT_HOOKS = [
    "The creatures attack without warning, driven by instinct or malice.",
    "You've wandered into hostile territory. The inhabitants do not welcome visitors.",
    "Something draws these creatures to you — fate, magic, or sheer bad luck.",
]


# ---------------------------------------------------------------------------
# Combat atmosphere lines
# ---------------------------------------------------------------------------

DIFFICULTY_FLAVOR = {
    "easy": [
        "This should be a manageable fight — a chance for the party to flex their skills.",
        "The opposition is relatively minor, but carelessness could still draw blood.",
        "A straightforward skirmish. Confident adventurers should handle this without breaking a sweat.",
    ],
    "medium": [
        "A fair fight that will test the party's abilities. Expect to use some resources.",
        "This encounter will challenge the group but should be survivable with good tactics.",
        "The odds are roughly even. Victory will require coordination and smart play.",
    ],
    "hard": [
        "This is a dangerous fight. One wrong move could mean disaster for the party.",
        "The odds are stacked against you. This fight will drain your resources and your nerve.",
        "A brutal encounter that could easily go sideways. Retreat is not cowardice — it's wisdom.",
    ],
    "deadly": [
        "This encounter could be the last thing the party ever faces. Proceed with extreme caution.",
        "The air itself seems to thicken with dread. This fight could kill one or more party members.",
        "A truly lethal encounter. The party will need every trick, spell, and ounce of courage to survive.",
    ],
}


# ---------------------------------------------------------------------------
# Scenario generator
# ---------------------------------------------------------------------------

def generate_scenario(encounter_data, environment=None):
    """
    Build a narrative scenario description for an encounter.

    Parameters
    ----------
    encounter_data : dict
        Output from encounter.generate_encounter()
    environment : str or None
        The environment to set the scene in. If None, one is chosen
        from the monsters' environment lists.

    Returns
    -------
    str
        A multi-paragraph narrative scenario.
    """
    if encounter_data is None:
        return "No encounter data provided."

    monsters = encounter_data["monsters"]
    difficulty = encounter_data["difficulty"]

    # Determine environment
    if environment is None:
        all_envs = set()
        for m, _ in monsters:
            all_envs.update(m.environments)
        all_envs.discard("any")
        environment = random.choice(list(all_envs)) if all_envs else "dungeon"

    # Pick intro
    intros = ENVIRONMENT_INTROS.get(environment, DEFAULT_INTROS)
    intro = random.choice(intros)

    # Pick hook based on dominant monster type
    type_counts = {}
    for m, count in monsters:
        t = m.monster_type
        type_counts[t] = type_counts.get(t, 0) + count
    dominant_type = max(type_counts, key=type_counts.get)
    hooks = ENCOUNTER_HOOKS.get(dominant_type, DEFAULT_HOOKS)
    hook = random.choice(hooks)

    # Difficulty flavor
    flavors = DIFFICULTY_FLAVOR.get(difficulty, DIFFICULTY_FLAVOR["medium"])
    flavor = random.choice(flavors)

    # Build monster appearance description
    monster_lines = []
    for m, count in monsters:
        desc = m.description.rstrip(".")
        if count == 1:
            monster_lines.append(f"a {m.name} — {desc}")
        else:
            monster_lines.append(f"{count} {m.name}s — {desc}")

    monster_desc = "You face " + "; and ".join(monster_lines) + "."

    # Compose the full scenario
    scenario = f"""
{'='*70}
  ENCOUNTER SCENARIO
{'='*70}

  Setting: {environment.replace('_', ' ').title()}

  {intro}

  {hook}

  {monster_desc}

  {flavor}

{'='*70}"""

    return scenario
