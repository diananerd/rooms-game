#!/usr/bin/env python3
"""
Cryptographically random dice roller for D&D games.

Solves the LLM dice bias problem: LLMs generate "random" d20 rolls that
average 14.6 instead of 10.5, with zero failures. This script uses
os.urandom() for true uniform distribution.

Usage as CLI:
    python3 scripts/roll-dice.py                  # roll 1d20
    python3 scripts/roll-dice.py 4                # roll 4d20
    python3 scripts/roll-dice.py 2 8              # roll 2d8
    python3 scripts/roll-dice.py 1 20 --mod 3     # roll 1d20+3
    python3 scripts/roll-dice.py --batch 10       # roll 10 separate d20s, one per line

Usage from Python:
    from roll_dice import roll, roll_d20
    roll_d20()           # -> 14
    roll_d20(mod=3)      # -> {'roll': 14, 'mod': 3, 'total': 17}
    roll(2, 8)           # -> {'rolls': [5, 3], 'total': 8}
"""

import secrets
import argparse
import json
import sys


def roll_die(sides=20):
    """Roll a single die with uniform distribution using crypto-random."""
    return secrets.randbelow(sides) + 1


def roll(count=1, sides=20, mod=0):
    """Roll count dice of given sides, return individual rolls and total."""
    rolls = [roll_die(sides) for _ in range(count)]
    total = sum(rolls) + mod
    return {
        "rolls": rolls,
        "sides": sides,
        "mod": mod,
        "total": total,
        "notation": f"{count}d{sides}" + (f"+{mod}" if mod > 0 else f"{mod}" if mod < 0 else ""),
    }


def roll_d20(mod=0):
    """Roll a single d20, return the raw roll and modified total."""
    r = roll_die(20)
    result = {
        "roll": r,
        "mod": mod,
        "total": r + mod,
        "nat20": r == 20,
        "nat1": r == 1,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Roll dice with true randomness")
    parser.add_argument("count", nargs="?", type=int, default=1, help="Number of dice")
    parser.add_argument("sides", nargs="?", type=int, default=20, help="Sides per die")
    parser.add_argument("--mod", type=int, default=0, help="Modifier to add")
    parser.add_argument("--batch", type=int, default=0,
                        help="Roll this many separate d20s")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.batch > 0:
        results = [roll_d20(mod=args.mod) for _ in range(args.batch)]
        if args.json:
            print(json.dumps(results))
        else:
            for r in results:
                nat = " (NAT 20!)" if r["nat20"] else " (NAT 1!)" if r["nat1"] else ""
                if args.mod:
                    print(f"d20({r['roll']}) + {args.mod} = {r['total']}{nat}")
                else:
                    print(f"d20({r['roll']}){nat}")
    else:
        result = roll(args.count, args.sides, args.mod)
        if args.json:
            print(json.dumps(result))
        else:
            rolls_str = ", ".join(str(r) for r in result["rolls"])
            print(f"{result['notation']}: [{rolls_str}] = {result['total']}")


if __name__ == "__main__":
    main()
