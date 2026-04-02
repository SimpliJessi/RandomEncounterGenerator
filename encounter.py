"""
Encounter balancing engine for the Random Encounter Generator.

Uses XP-budget thresholds per player level and party size to build
encounters at four difficulty tiers: Easy, Medium, Hard, and Deadly.
"""

import random
import math
from monster import Monster, MONSTER_DATABASE, filter_monsters

# ---------------------------------------------------------------------------
# XP values by Challenge Rating
# ---------------------------------------------------------------------------

CR_TO_XP = {
    0:      10,
    0.125:  25,
    0.25:   50,
    0.5:    100,
    1:      200,
    2:      450,
    3:      700,
    4:      1100,
    5:      1800,
    6:      2300,
    7:      2900,
    8:      3900,
    9:      5000,
    10:     5900,
    11:     7200,
    12:     8400,
    13:     10000,
    14:     11500,
    15:     13000,
    16:     15000,
    17:     18000,
    18:     20000,
    19:     22000,
    20:     25000,
    21:     33000,
    22:     41000,
    23:     50000,
    24:     62000,
    25:     75000,
    26:     90000,
    27:     105000,
    28:     120000,
    29:     135000,
    30:     155000,
}

# ---------------------------------------------------------------------------
# XP thresholds per player level  (Easy, Medium, Hard, Deadly)
# ---------------------------------------------------------------------------

LEVEL_THRESHOLDS = {
    1:  (25,   50,   75,   100),
    2:  (50,   100,  150,  200),
    3:  (75,   150,  225,  400),
    4:  (125,  250,  375,  500),
    5:  (250,  500,  750,  1100),
    6:  (300,  600,  900,  1400),
    7:  (350,  750,  1100, 1700),
    8:  (450,  900,  1400, 2100),
    9:  (550,  1100, 1600, 2400),
    10: (600,  1200, 1900, 2800),
    11: (800,  1600, 2400, 3600),
    12: (1000, 2000, 3000, 4500),
    13: (1100, 2200, 3400, 5100),
    14: (1250, 2500, 3800, 5700),
    15: (1400, 2800, 4300, 6400),
    16: (1600, 3200, 4800, 7200),
    17: (2000, 3900, 5900, 8800),
    18: (2100, 4200, 6300, 9500),
    19: (2400, 4900, 7300, 10900),
    20: (2800, 5700, 8500, 12700),
}

DIFFICULTY_NAMES = ["easy", "medium", "hard", "deadly"]
DIFFICULTY_INDEX = {name: i for i, name in enumerate(DIFFICULTY_NAMES)}

# ---------------------------------------------------------------------------
# Encounter multipliers based on number of monsters
# ---------------------------------------------------------------------------

def _encounter_multiplier(monster_count, party_size):
    """
    Return the XP multiplier based on the number of monsters
    and the size of the party (fewer than 3 or more than 5 shifts
    the bracket by one step).
    """
    brackets = [
        (1,  1.0),
        (2,  1.5),
        (3,  2.0),   # 3-6
        (7,  2.5),   # 7-10
        (11, 3.0),   # 11-14
        (15, 4.0),   # 15+
    ]

    multiplier = 1.0
    for threshold, mult in reversed(brackets):
        if monster_count >= threshold:
            multiplier = mult
            break

    # Shift for small / large parties
    if party_size < 3:
        idx = [b[1] for b in brackets].index(multiplier)
        idx = min(idx + 1, len(brackets) - 1)
        multiplier = brackets[idx][1]
    elif party_size >= 6:
        idx = [b[1] for b in brackets].index(multiplier)
        idx = max(idx - 1, 0)
        multiplier = brackets[idx][1]

    return multiplier


# ---------------------------------------------------------------------------
# Core budget helpers
# ---------------------------------------------------------------------------

def party_xp_threshold(party_size, party_level, difficulty):
    """Return the total XP budget for the party at a given difficulty."""
    if party_level < 1:
        party_level = 1
    if party_level > 20:
        party_level = 20
    idx = DIFFICULTY_INDEX.get(difficulty.lower(), 1)
    per_player = LEVEL_THRESHOLDS[party_level][idx]
    return per_player * party_size


def xp_for_cr(cr):
    """Return XP value for a given challenge rating."""
    return CR_TO_XP.get(cr, 0)


def adjusted_xp(monsters, party_size):
    """
    Given a list of (Monster, count) tuples, return the adjusted XP
    (raw XP × encounter multiplier).
    """
    total_count = sum(count for _, count in monsters)
    raw_xp = sum(xp_for_cr(m.cr) * count for m, count in monsters)
    multiplier = _encounter_multiplier(total_count, party_size)
    return int(raw_xp * multiplier), raw_xp


def max_cr_for_party(party_level, party_size):
    """
    Heuristic: cap the individual monster CR so one creature isn't
    overwhelmingly above party capability. Keeps solo monsters
    reasonably within Deadly range.
    """
    budget = party_xp_threshold(party_size, party_level, "deadly")
    for cr in sorted(CR_TO_XP.keys(), reverse=True):
        if CR_TO_XP[cr] <= budget:
            return cr
    return 0


# ---------------------------------------------------------------------------
# Encounter generation
# ---------------------------------------------------------------------------

def generate_encounter(party_size, party_level, difficulty="medium",
                       environments=None, monster_types=None,
                       max_monster_types=3, target_count=None):
    """
    Build a balanced encounter for the given party.

    Parameters
    ----------
    target_count : int or None
        If set, the encounter will contain exactly this many total
        creatures (or as close as possible while staying balanced).

    Returns a dict with:
        monsters    - list of (Monster, count) tuples
        raw_xp      - unadjusted XP total
        adjusted_xp - adjusted XP total (with multiplier)
        budget      - the XP budget for the chosen difficulty
        difficulty  - difficulty label
    """
    budget = party_xp_threshold(party_size, party_level, difficulty)
    cr_cap = max_cr_for_party(party_level, party_size)

    # Determine usable CR range
    cr_floor = 0
    candidates = filter_monsters(cr_min=cr_floor, cr_max=cr_cap,
                                  environments=environments,
                                  monster_types=monster_types)
    if not candidates:
        # Fall back to full database within CR range
        candidates = [m for m in MONSTER_DATABASE if m.cr <= cr_cap]

    if not candidates:
        return None  # nothing fits at all

    # Filter out monsters whose solo XP already exceeds the budget
    affordable = [m for m in candidates if xp_for_cr(m.cr) <= budget]
    if not affordable:
        affordable = [min(candidates, key=lambda m: xp_for_cr(m.cr))]

    # -----------------------------------------------------------------
    # Fixed creature count mode
    # -----------------------------------------------------------------
    if target_count is not None:
        encounter = _generate_fixed_count(affordable, target_count,
                                          budget, party_size,
                                          max_monster_types)
    else:
        # -----------------------------------------------------------------
        # Auto mode (original behaviour)
        # -----------------------------------------------------------------
        # Decide encounter style: solo big monster, or a group
        strong_candidates = [m for m in affordable
                             if budget * 0.6 <= xp_for_cr(m.cr) <= budget]
        use_solo = strong_candidates and random.random() < 0.25

        if use_solo:
            chosen = random.choice(strong_candidates)
            encounter = [(chosen, 1)]
        else:
            num_types = random.randint(1, min(max_monster_types, len(affordable)))
            chosen_types = random.sample(affordable, num_types)
            chosen_types.sort(key=lambda m: xp_for_cr(m.cr), reverse=True)

            encounter = []
            remaining_budget = budget

            for i, monster in enumerate(chosen_types):
                xp_val = xp_for_cr(monster.cr)
                if xp_val == 0:
                    continue

                if i == len(chosen_types) - 1:
                    share = remaining_budget
                else:
                    share = remaining_budget // (len(chosen_types) - i)

                count = max(1, share // xp_val)

                test_encounter = encounter + [(monster, count)]
                adj, _ = adjusted_xp(test_encounter, party_size)
                while adj > budget * 1.25 and count > 1:
                    count -= 1
                    test_encounter = encounter + [(monster, count)]
                    adj, _ = adjusted_xp(test_encounter, party_size)

                test_encounter = encounter + [(monster, count)]
                adj, _ = adjusted_xp(test_encounter, party_size)
                if adj > budget * 2.0 and len(encounter) > 0:
                    continue

                encounter.append((monster, count))
                remaining_budget -= xp_val * count

            if encounter:
                adj_total, _ = adjusted_xp(encounter, party_size)
                if adj_total < budget * 0.7:
                    cheapest_idx = min(range(len(encounter)),
                                       key=lambda i: xp_for_cr(encounter[i][0].cr))
                    m, c = encounter[cheapest_idx]
                    xp_val = xp_for_cr(m.cr)
                    while True:
                        test = list(encounter)
                        test[cheapest_idx] = (m, c + 1)
                        adj, _ = adjusted_xp(test, party_size)
                        if adj > budget * 1.15:
                            break
                        c += 1
                    encounter[cheapest_idx] = (m, c)

        # Final adjustment pass — trim if we overshot
        if encounter:
            adj_total, raw_total = adjusted_xp(encounter, party_size)
            iterations = 0
            while adj_total > budget * 1.2 and iterations < 30:
                encounter.sort(key=lambda pair: (-pair[1], xp_for_cr(pair[0].cr)))
                m, c = encounter[0]
                if c > 1:
                    encounter[0] = (m, c - 1)
                else:
                    encounter.pop(0)
                if not encounter:
                    break
                adj_total, raw_total = adjusted_xp(encounter, party_size)
                iterations += 1

    # Make sure we have at least one monster
    if not encounter:
        best = None
        best_diff = float('inf')
        for m in affordable:
            xp_val = xp_for_cr(m.cr)
            for count in range(1, max(2, budget // max(xp_val, 1) + 1)):
                test_adj, _ = adjusted_xp([(m, count)], party_size)
                diff = abs(test_adj - budget)
                if test_adj <= budget * 1.3 and diff < best_diff:
                    best_diff = diff
                    best = (m, count)
        if best:
            encounter = [best]
        else:
            encounter = [(affordable[0], 1)]

    adj_total, raw_total = adjusted_xp(encounter, party_size)

    return {
        "monsters": encounter,
        "raw_xp": raw_total,
        "adjusted_xp": adj_total,
        "budget": budget,
        "difficulty": difficulty,
    }


def _generate_fixed_count(affordable, target_count, budget, party_size,
                          max_monster_types):
    """
    Build an encounter with exactly *target_count* total creatures
    while staying as close to the XP budget as possible.
    """
    # Ideal raw XP per monster (accounting for the encounter multiplier)
    multiplier = _encounter_multiplier(target_count, party_size)
    ideal_raw = budget / multiplier  # total raw XP we can spend
    per_creature_target = ideal_raw / target_count

    # Find the CR whose XP is closest to the per-creature target
    sorted_affordable = sorted(affordable, key=lambda m: xp_for_cr(m.cr))

    # Pick 1-3 monster types whose XP values are close to per_creature_target
    close_monsters = sorted(
        affordable,
        key=lambda m: abs(xp_for_cr(m.cr) - per_creature_target)
    )

    # Take the top candidates (up to max_monster_types distinct types)
    seen_names = set()
    chosen_types = []
    for m in close_monsters:
        if m.name not in seen_names:
            chosen_types.append(m)
            seen_names.add(m.name)
        if len(chosen_types) >= max_monster_types:
            break

    if not chosen_types:
        chosen_types = [random.choice(affordable)]

    # Distribute target_count across chosen types
    num_types = min(len(chosen_types), target_count)
    chosen_types = chosen_types[:num_types]
    random.shuffle(chosen_types)

    encounter = []
    remaining = target_count

    for i, monster in enumerate(chosen_types):
        if i == len(chosen_types) - 1:
            count = remaining  # last type gets whatever is left
        else:
            count = max(1, remaining // (len(chosen_types) - i))
            # Add a little randomness to the split
            variance = max(0, count // 3)
            if variance > 0:
                count = random.randint(max(1, count - variance),
                                       count + variance)
            count = min(count, remaining - (len(chosen_types) - i - 1))
            count = max(1, count)
        encounter.append((monster, count))
        remaining -= count

    # Verify total count
    total = sum(c for _, c in encounter)
    if total != target_count:
        # Adjust the last entry
        m, c = encounter[-1]
        encounter[-1] = (m, c + (target_count - total))

    return encounter


def format_encounter(encounter_data):
    """Return a nicely formatted string describing the encounter."""
    if encounter_data is None:
        return "  No encounter could be generated with the given parameters."

    lines = []
    diff = encounter_data["difficulty"].upper()
    lines.append(f"  Difficulty : {diff}")
    lines.append(f"  XP Budget  : {encounter_data['budget']:,}")
    lines.append(f"  Raw XP     : {encounter_data['raw_xp']:,}")
    lines.append(f"  Adjusted XP: {encounter_data['adjusted_xp']:,}")
    lines.append("")
    lines.append("  Monsters:")
    for monster, count in encounter_data["monsters"]:
        xp = xp_for_cr(monster.cr)
        lines.append(f"    {count}x {monster.name}  (CR {monster.cr}, "
                      f"{xp:,} XP each)")
    lines.append("")
    lines.append("  Monster Details:")
    for monster, count in encounter_data["monsters"]:
        lines.append(monster.summary())

    return "\n".join(lines)
