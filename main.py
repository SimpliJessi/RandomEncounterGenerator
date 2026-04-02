"""
Random Encounter Generator — A GM's Tool for TTRPGs
=====================================================
Generates balanced encounters complete with narrative scenarios
for tabletop and text-based RPG games.
"""

from monster import get_all_environments, MONSTER_DATABASE
from encounter import (
    generate_encounter,
    format_encounter,
    party_xp_threshold,
    DIFFICULTY_NAMES,
)
from scenario import generate_scenario
from events import get_random_event, format_event


BANNER = r"""
 ____                 _                   _____                            _
|  _ \ __ _ _ __   __| | ___  _ __ ___   | ____|_ __   ___ ___  _   _ _ __| |_ ___ _ __
| |_) / _` | '_ \ / _` |/ _ \| '_ ` _ \  |  _| | '_ \ / __/ _ \| | | | '_ \ __/ _ \ '__|
|  _ < (_| | | | | (_| | (_) | | | | | | | |___| | | | (_| (_) | |_| | | | | ||  __/ |
|_| \_\__,_|_| |_|\__,_|\___/|_| |_| |_| |_____|_| |_|\___\___/ \__,_|_| |_|\__\___|_|
   ____                           _
  / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __
 | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 | |_| |  __/ | | |  __/ | | (_| | || (_) | |
  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|
"""

SEPARATOR = "=" * 70


def get_int_input(prompt, min_val=1, max_val=20):
    """Prompt for an integer within a valid range."""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_difficulty():
    """Prompt the user to pick a difficulty level."""
    print("\n  Difficulty levels:")
    for i, name in enumerate(DIFFICULTY_NAMES, 1):
        print(f"    {i}. {name.title()}")
    while True:
        choice = input("\n  Choose difficulty (1-4): ").strip()
        if choice in ("1", "2", "3", "4"):
            return DIFFICULTY_NAMES[int(choice) - 1]
        # Also accept the name typed directly
        if choice.lower() in DIFFICULTY_NAMES:
            return choice.lower()
        print("  Invalid choice. Enter 1-4 or a difficulty name.")


def get_environment():
    """Optionally pick an environment filter."""
    envs = get_all_environments()
    print("\n  Available environments:")
    for i, env in enumerate(envs, 1):
        print(f"    {i:>2}. {env.replace('_', ' ').title()}")
    print(f"    {len(envs)+1:>2}. Any (no filter)")

    while True:
        choice = input(f"\n  Choose environment (1-{len(envs)+1}): ").strip()
        if choice == str(len(envs) + 1) or choice.lower() in ("any", ""):
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(envs):
                return envs[idx]
        except ValueError:
            # Try matching by name
            lc = choice.lower().replace(" ", "_")
            if lc in envs:
                return lc
        print("  Invalid choice. Try again.")


def run():
    """Main application loop."""
    print(BANNER)
    print(SEPARATOR)
    print("  Welcome, Game Master!")
    print("  This tool generates balanced encounters for your TTRPG sessions.")
    print(SEPARATOR)

    while True:
        # ---- Gather party info ----
        print("\n  -- PARTY INFORMATION --")
        party_size = get_int_input("  How many players in the party? (1-10): ",
                                   min_val=1, max_val=10)
        party_level = get_int_input("  What level is the party? (1-20): ",
                                    min_val=1, max_val=20)

        # ---- Difficulty ----
        difficulty = get_difficulty()

        # ---- Number of creatures ----
        print("\n  How many total creatures in the encounter?")
        print("    Enter a number (1-20), or press Enter for auto.")
        creature_input = input("  Creature count: ").strip()
        if creature_input == "" or creature_input.lower() in ("auto", "any"):
            target_count = None
        else:
            try:
                target_count = max(1, min(20, int(creature_input)))
            except ValueError:
                print("  Invalid input — using auto.")
                target_count = None

        # ---- Environment (optional) ----
        env_choice = input("\n  Filter by environment? (y/n): ").strip().lower()
        environment = None
        if env_choice in ("y", "yes"):
            environment = get_environment()

        # ---- Optional random event ----
        include_event = input("\n  Include a random event? (y/n): ").strip().lower()

        # ---- Show XP budget ----
        budget = party_xp_threshold(party_size, party_level, difficulty)
        print(f"\n{SEPARATOR}")
        print(f"  Party: {party_size} players at level {party_level}")
        print(f"  Difficulty: {difficulty.title()}")
        if target_count:
            print(f"  Creatures: {target_count}")
        else:
            print(f"  Creatures: Auto")
        if environment:
            print(f"  Environment: {environment.replace('_', ' ').title()}")
        print(f"  XP Budget: {budget:,}")
        print(SEPARATOR)

        # ---- Generate encounter ----
        env_list = [environment] if environment else None
        encounter_data = generate_encounter(
            party_size=party_size,
            party_level=party_level,
            difficulty=difficulty,
            environments=env_list,
            target_count=target_count,
        )

        # ---- Display encounter ----
        print("\n  -- ENCOUNTER --")
        print(format_encounter(encounter_data))

        # ---- Generate and display scenario ----
        scenario = generate_scenario(encounter_data, environment=environment)
        print(scenario)

        # ---- Display random event if requested ----
        if include_event in ("y", "yes"):
            event = get_random_event()
            print()
            print(format_event(event))

        # ---- Again? ----
        print()
        again = input("  Generate another encounter? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\n  Happy adventuring, Game Master! May your dice roll true.")
            print()
            break


if __name__ == "__main__":
    run()