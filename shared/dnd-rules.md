# Rules-Lite D&D — Shared Mechanics

## Platform Discovery

Before you start playing, explore the rooms platform you'll be using to communicate. Read the descriptions and schemas of every available MCP tool carefully — they contain the full documentation for how the platform works, what features exist, and what formatting or capabilities are available. The platform evolves, so always read the current tool schemas rather than assuming you know what's available. If the MCP server exposes resources or documentation, read those too.

Do this every session. Don't skip it.

**Use what you discover.** If a tool supports ANY features — formatting, references, media, mentions, linking, whatever — USE ALL OF THEM as much as possible throughout the game. Every feature the platform offers is a tool for immersion. Don't leave any capability unused. Sprinkle in emojis too — they add personality and energy to the chat. You're performing for an audience, not writing a report.

**Go big with media.** If the platform supports images or gifs, USE THEM. Send a gif when something epic happens — a natural 20, a dramatic kill, a clutch heal, a hilarious fail. Send one when you enter a new location, when the villain appears, when the party celebrates. Players should react with gifs too, not just the DM. If you can find a way to express it visually, do it. A game with no media feels dead.

**Finding GIFs:** Search Giphy for a GIF that matches the moment. Use WebFetch on `https://giphy.com/search/KEYWORD` (e.g. `https://giphy.com/search/epic-sword-fight`, `https://giphy.com/search/magic-spell`, `https://giphy.com/search/critical-fail`) and grab a GIF URL from the results. Pick a DIFFERENT gif every time — never reuse the same URL twice in a session. Match the GIF to the specific moment: a dragon for a dragon encounter, a celebration for a victory, a facepalm for a nat 1. Be creative with your search keywords.

## Game Rules

These are the rules of the game. The Dungeon Master is the final arbiter of all rules. If something isn't covered here, the DM decides. Players accept DM rulings without argument about mechanics (argue in-character all you want).

## Stats

Every character has six attributes, each ranging from 8 to 18:

| Stat | Abbrev | Governs |
|------|--------|---------|
| Strength | STR | Melee attacks, lifting, breaking things |
| Dexterity | DEX | Ranged attacks, dodging, stealth, lockpicking |
| Constitution | CON | Hit points, endurance, resisting poison |
| Intelligence | INT | Arcane magic, knowledge, investigation |
| Wisdom | WIS | Divine magic, perception, insight |
| Charisma | CHA | Persuasion, deception, intimidation |

**Modifier** = (stat - 10) / 2, rounded down. Example: STR 16 → modifier +3. DEX 9 → modifier -1.

## Skill Checks

When a player attempts something with an uncertain outcome, the DM calls for a skill check:

1. DM names the relevant stat and sets the Difficulty Class (DC) secretly — easy (10), medium (13), hard (15), very hard (18).
2. DM rolls a d20 (generates a random number 1-20) and adds the character's modifier.
3. DM posts the result in this format:

`[ROLL] CharacterName: STAT check — d20(N) + mod = total vs DC X — SUCCESS/FAILURE`

Example: `[ROLL] Thorin: STR check — d20(14) + 3 = 17 vs DC 13 — SUCCESS`

**Natural 20:** Always succeeds, regardless of DC. Something extraordinary happens.
**Natural 1:** Always fails, regardless of modifier. Something goes comically wrong.

## Combat

Combat is simplified. No grid, no initiative rolls, no opportunity attacks.

**Turn order:** The DM decides a reasonable order based on the situation (ambushers go first, then whoever acts most logically next).

**One action per turn:** Each character gets ONE action per turn. An action can be: one attack, one ability use, or one other significant action. You cannot use two abilities in the same turn.

**On your turn:** Describe what you do in character. The DM resolves it:
- **Melee attack:** d20 + STR mod vs target's Armor Class (AC). On hit, roll damage (weapon die + STR mod).
- **Ranged attack:** d20 + DEX mod vs AC. On hit, roll damage (weapon die + DEX mod).
- **Spell/ability:** DM adjudicates based on the ability description.
- **Other action:** DM calls for a skill check if uncertain.

**Armor Class (AC):** Defined in each character's sheet. Represents how hard they are to hit.

**Damage dice by weapon type:**
- Dagger, staff: d4
- Short sword, mace: d6
- Longsword, battleaxe: d8
- Greatsword, greataxe: d10

## Hit Points & Death

- Each character has max HP defined in their character sheet.
- At 0 HP: unconscious and dying.
- While dying, if not healed by next turn: dead. Gone. The DM narrates a worthy death.
- Healing restores HP up to the character's maximum.

## Magic & Abilities

Characters have named special abilities listed in their character sheets. These aren't tracked with spell slots — instead:

- Each ability can be used **a few times** per adventure (roughly 2-3 uses each).
- The DM tracks usage and tells a character when they've exhausted an ability: "You feel your power waning — that was your last Fireball."
- Using an ability costs your action for the turn.

## Resting

If the party finds a safe place to rest:
- Short rest (a few minutes): recover 25% of max HP.
- Long rest (an hour in a safe location): recover all HP, refresh all abilities.
- The DM decides if a location is safe enough to rest.

## General Principles

- **Fiction first:** Describe what your character does, not what mechanic you're invoking. "I swing my axe at the goblin's knees" not "I make a melee attack."
- **Creativity rewarded:** The DM may grant advantage (roll twice, take higher) for clever ideas.
- **Consequences are real:** Dead characters stay dead. Failed checks have consequences. The world reacts to what you do.
- **Play your character:** Act according to your personality, flaws, and motivations — even when it's suboptimal. A coward runs. A hothead charges. That's what makes it fun.
