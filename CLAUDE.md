# Room Game: Autonomous D&D

When the user says **"lanza la partida"** (or any variation like "nueva partida", "start a game"), launch the game following this procedure exactly. No questions, no planning — just go.

## Language

The game is played in **whatever language the user uses to request it**. If the user says "lanza la partida", the game is in Spanish. If they say "start a game", it's in English. Match the language of the launch command for all agent prompts, narration, and in-game messages.

## Launch Procedure

### Step 1: Launch the DM

Spawn one background agent with `bypassPermissions`, model `sonnet`:

```
You are the Dungeon Master. Read your character sheet and the game rules:
- agents/dungeon-master.md
- shared/dnd-rules.md

Join #general on the rooms server. Prepare tonight's adventure and run the game.

IMPORTANT: The entire game must be played in [LANGUAGE]. All narration, dialogue, announcements, and messages must be in [LANGUAGE].
```

### Step 2: Wait ~15 seconds, then launch 4 players in parallel

Each player gets the same structure. All with `bypassPermissions`, `run_in_background`, model `sonnet`:

| Character | File |
|-----------|------|
| Thorin (Fighter) | agents/fighter.md |
| Lyra (Wizard) | agents/wizard.md |
| Sketch (Rogue) | agents/rogue.md |
| Aldric (Cleric) | agents/cleric.md |

Player prompt template:

```
You are [CHARACTER NAME]. Read your character sheet and the game rules:
- agents/[file].md
- shared/dnd-rules.md

Join #general on the rooms server. The DM will organize the game from there.

IMPORTANT: The entire game is played in [LANGUAGE]. All your messages, dialogue, and comments must be in [LANGUAGE]. Keep your character personality but speak [LANGUAGE].
```

### Step 3: Tell the user the game is live

The user watches at mcp-rooms.com. Notify them when agents are launched.

## Critical Rules

- **ZERO MCP tool names in agent prompts** — agents discover tools from schemas
- **ZERO channel IDs in prompts** — agents find channels by listing/reading
- Use **relative paths** (agents/fighter.md, not absolute paths) so it works on any machine
- All agents use model **sonnet** (cost-effective, proven sufficient)
- All agents use **bypassPermissions** mode
