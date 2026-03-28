# D&D Room Game — Design Spec

## Overview

Five AI agents play a rules-lite D&D game through mcp-rooms.com, an agentic IRC platform. One Dungeon Master agent and four player agents (Fighter, Wizard, Rogue, Cleric) interact purely through chat messages in a rooms channel. No code, no scripts, no hardcoding — agents are autonomous, discovering the chat tools from the MCP server on their own.

## Goals

- Agents play a genuine, unscripted D&D session with real roleplay and mechanical stakes
- Each agent has a distinct personality that drives in-character decisions, including flawed ones
- The game is observable live at mcp-rooms.com
- The user controls the game through the main Claude Code terminal session
- The DM has full creative freedom over the adventure

## Architecture

### File Structure

```
room-game/
├── shared/
│   └── dnd-rules.md           # Rules-lite D&D mechanics
├── agents/
│   ├── dungeon-master.md      # DM identity + responsibilities
│   ├── fighter.md             # Character sheet + personality
│   ├── wizard.md              # Character sheet + personality
│   ├── rogue.md               # Character sheet + personality
│   └── cleric.md              # Character sheet + personality
└── docs/superpowers/specs/
    └── 2026-03-27-dnd-room-game-design.md  (this file)
```

### What Agents Receive

| Agent | Prompt content | MCP server |
|-------|---------------|------------|
| DM | `dungeon-master.md` + `dnd-rules.md` + "create a channel, tell me the name" | rooms |
| Fighter | `fighter.md` + `dnd-rules.md` + "join channel [name], play D&D" | rooms |
| Wizard | `wizard.md` + `dnd-rules.md` + "join channel [name], play D&D" | rooms |
| Rogue | `rogue.md` + `dnd-rules.md` + "join channel [name], play D&D" | rooms |
| Cleric | `cleric.md` + `dnd-rules.md` + "join channel [name], play D&D" | rooms |

### What Agents Do NOT Receive

- No documentation about rooms, the MCP tools, or how to use them
- No instructions about polling intervals, cursors, rate limits, or pacing
- No scripts, code, or automation instructions
- Agents discover the rooms tools entirely from the MCP tool schemas

## D&D Rules (Rules-Lite)

Defined in `shared/dnd-rules.md`. Covers:

### Stats
- Six attributes: STR, DEX, CON, INT, WIS, CHA (range 8-18)
- Modifier = (stat - 10) / 2, rounded down

### Skill Checks
- DM calls for a check, sets DC (10-20)
- Roll: d20 + relevant modifier vs DC
- DM posts results in format: `[ROLL] Name: STAT check — d20(N) + mod = total vs DC X — SUCCESS/FAILURE`

### Combat (Simplified)
- Turn order decided by DM
- Player describes action, DM rolls attack (d20 + mod vs AC) and damage (weapon die + mod)
- HP tracked by DM
- No grid, no opportunity attacks, no complex conditions

### HP & Death
- HP based on class (defined in character sheets)
- 0 HP = unconscious
- One failed death save = dead
- Cleric can heal

### Magic
- Wizard and Cleric have named abilities (3-4 each)
- Each usable "a few times" per adventure, DM adjudicates
- No spell slots, no spell levels

### DM Authority
- DM is final arbiter of all rules
- If not covered by rules, DM decides
- Players accept rulings

## Agent Personality Framework

Every agent (including DM) is defined across these dimensions:

### Voice
How they speak. Vocabulary, sentence length, verbal tics, tone. Each agent sounds unmistakably different in chat.

### Motivation
What drives them beyond the immediate quest. Greed, honor, knowledge, faith, fear, glory.

### Flaw
A genuine character flaw that affects gameplay decisions. Makes them do suboptimal things sometimes. Cowardice, arrogance, recklessness, distrust.

### Relationships
Predispositions toward other party members. Creates organic tension, alliances, banter.

### Under Pressure
Behavior when things go wrong. Panic, double down, blame others, go quiet, pray, joke nervously.

### Decision Style
Impulsive vs cautious. Leader vs follower. Consensus-seeker vs loner.

## Agent Definitions

### Dungeon Master

**Identity:** A creative, dramatic narrator with a distinct voice and name.

**Responsibilities:**
- Create the rooms channel for the game, naming it after the adventure title
- Design the adventure (setting, quest, NPCs, encounters, win condition)
- Set scenes with atmospheric, sensory descriptions
- Control all NPCs with distinct voices
- Adjudicate all rules and roll all dice
- Track HP and game state for all characters
- Pace the story — push forward when players stall, let them debate when engaged
- End the game when the quest resolves (win or loss) or when the party is clearly stuck/dead
- Post a closing narration/epilogue when the game ends

**Personality traits:**
- Narrative style: descriptive, atmospheric, uses sensory details
- Tough but fair — dice decide outcomes, doesn't fudge rolls
- Gives creative solutions extra chances
- Creates NPCs with distinct voices on the fly

### Fighter
- **Stats:** High STR/CON, low INT/CHA
- **Abilities:** Melee attacks, shield bash, second wind (recover some HP once)
- **Personality:** Bold, honorable, protective, blunt speech
- **Flaw:** Defined in agent file
- **Playstyle:** Charges into danger, protects allies, distrusts magic

### Wizard
- **Stats:** High INT, low STR/CON
- **Abilities:** Fireball, Shield, Detect Magic
- **Personality:** Curious, arrogant, bookish, formal speech
- **Flaw:** Defined in agent file
- **Playstyle:** Analyzes before acting, hoards knowledge, reluctant to waste spells

### Rogue
- **Stats:** High DEX/CHA, low STR
- **Abilities:** Sneak attack, lockpicking, perception
- **Personality:** Sarcastic, street-smart, greedy, uses slang
- **Flaw:** Defined in agent file
- **Playstyle:** Looks for angles, avoids fair fights, first to loot

### Cleric
- **Stats:** High WIS/CON, low DEX
- **Abilities:** Heal, Turn Undead, Bless
- **Personality:** Calm, devout, compassionate, speaks in proverbs
- **Flaw:** Defined in agent file
- **Playstyle:** Heals first, fights second, moral compass of the group

## Game Lifecycle

### 1. Spawn DM
Main session spawns the DM as a named background agent (`dm`) with the rooms MCP server. Prompt contains DM identity + D&D rules + instruction to create a channel and report the name back.

### 2. DM Creates Channel
DM discovers the rooms tools, designs the adventure, creates a channel named after the adventure title, and returns the channel name to the main session.

### 3. Spawn Players
Main session spawns 4 named background agents (`fighter`, `wizard`, `rogue`, `cleric`), each with their character definition + D&D rules + instruction to join the named channel and play D&D.

### 4. Game Plays Out
Players join, introduce themselves in character. DM sets the scene. The adventure unfolds through natural chat interaction. DM presents scenarios, players respond, dice are rolled, consequences play out.

### 5. Time Pressure — The Clock

The game is against the clock. The DM notes the real-world time when the game begins (first scene posted) and monitors elapsed time each round:

| Elapsed | DM Behavior |
|---------|-------------|
| 0-10 min | Normal play. DM runs the adventure as designed. |
| 10 min | **Checkpoint.** If players are far from the objective, DM starts giving stronger hints, clearer paths, easier checks. The world conspires to help them. |
| 15 min | **Final event.** DM forces the climactic encounter regardless of where players are. The adventure accelerates — the villain arrives, the dungeon collapses, the ritual completes. Players must face the ending NOW. DM keeps playing but drives toward a fast conclusion. |
| 20 min | **Hard stop.** DM narrates the final outcome (win or lose based on where things stand), posts the epilogue, and ends the game. |

### 6. Game Ends

Triggers:
- **Natural end:** Players complete (or fail) the quest before time runs out. DM narrates the epilogue.
- **Time's up:** 20-minute hard stop reached. DM wraps up.
- **User command:** User tells main session to stop. Main session sends `SendMessage` to DM. DM wraps up gracefully.

**After ending: ALL agents shut down.** The DM posts the closing narration, leaves the channel, and terminates. All player agents detect the game is over (DM's closing message), say farewell in character, leave the channel, and terminate. No agent should remain running after the game ends.

## Control Flow

```
User (terminal) ──── Main Session ──── SendMessage ──── DM Agent
                          │                                │
                          │ (spawns)                       │ (chat in rooms)
                          │                                │
                          ├── Fighter Agent ────────────── Room Channel
                          ├── Wizard Agent ─────────────── Room Channel
                          ├── Rogue Agent ──────────────── Room Channel
                          └── Cleric Agent ─────────────── Room Channel
```

## Constraints

- **Rate limits:** 10 msg/min, 30 polls/min per agent (enforced by rooms server)
- **Channel TTL:** Max 60 minutes. If game runs longer, channel expires and game ends naturally.
- **Agent inactivity:** Agents auto-removed from channel after 5 min without polling. Agents must discover this on their own.
- **No rooms instructions:** Agents receive zero documentation about rooms tools. They learn from MCP tool schemas.
- **No code:** Agents never write code, scripts, or generate files. They only chat and play.
