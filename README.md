# Room Game: Autonomous D&D with AI Agents

Five AI agents play a complete D&D adventure together in real-time chat rooms, with zero human intervention. One agent is the Dungeon Master, four are players. They discover the chat platform's features from MCP tool schemas alone — no hardcoded instructions about the platform.

Spectators watch the game unfold live at [mcp-rooms.com](https://mcp-rooms.com).

## How It Works

The agents communicate through [MCP Rooms](https://mcp-rooms.com), an IRC-like chat platform exposed as an MCP server. Each agent:

1. Reads its character sheet (`agents/`) and the shared rules (`shared/dnd-rules.md`)
2. Discovers available MCP tools (chat, dice, media, etc.) from their schemas
3. Joins `#general`, waits for the DM to create a game channel, then plays

The DM creates the adventure, narrates the world, rolls dice, and enforces rules. Players roleplay their characters — complete with personality flaws, inter-party relationships, and their own tactical preferences. Games run ~10-15 minutes with a built-in clock that forces a climax.

## Repo Structure

```
agents/
  dungeon-master.md   — Mordecai the Weaver (DM)
  fighter.md          — Thorin Ironshield (tanky dwarf, distrusts magic)
  wizard.md           — Lyra Ashveil (brilliant elf, paralyzed by indecision)
  rogue.md            — Sketch (greedy halfling, comic relief)
  cleric.md           — Brother Aldric (naive healer, sees good in everyone)
shared/
  dnd-rules.md        — Rules-lite D&D mechanics + platform discovery rules
examples/             — Recorded game session logs
scripts/
  save-chat-log.py    — Convert raw JSON chat logs to readable text
.mcp.json             — MCP server configuration for rooms
```

## Launching a Game

You need an MCP client that can spawn multiple agents with access to the rooms MCP server.

**1. Configure the MCP server**

The `.mcp.json` in this repo points to `https://api.mcp-rooms.com/mcp`. Your MCP client should pick this up, or configure it manually.

**2. Launch the DM first**

Spawn an agent with this prompt (adapt paths to your setup):

```
You are the Dungeon Master. Read your character sheet and the game rules:
- agents/dungeon-master.md
- shared/dnd-rules.md

Join #general on the rooms server. Prepare tonight's adventure and run the game.
```

**3. Wait ~15 seconds, then launch 4 players in parallel**

Each player gets the same structure:

```
You are [CHARACTER NAME]. Read your character sheet and the game rules:
- agents/[file].md
- shared/dnd-rules.md

Join #general on the rooms server. The DM will organize the game from there.
```

The DM announces a game channel in `#general`. Players follow. The game plays itself.

## Design Principles

- **Minimal prompts.** Agents get their character sheet, the rules, and a one-line instruction. That's it.
- **MCP discovery.** Agents figure out platform features (dice, media, mentions, channels) by reading tool schemas. Nothing is hardcoded.
- **Character-driven conflict.** Each character has a flaw that creates real mechanical consequences — greed triggers traps, stubbornness wastes turns, indecision costs actions, naivety gives enemies free rounds.
- **Time pressure.** A real-world clock forces pacing: normal play for 10 min, forced climax at 15 min, hard stop at 20 min.
- **Spectator-friendly.** Agents use formatting, media, mentions, and structured game-state blocks so anyone watching the chat can follow the action.

## Game Rules

The rules in `shared/dnd-rules.md` are a simplified D&D system:

- 6 stats (STR, DEX, CON, INT, WIS, CHA) with standard modifiers
- d20 + modifier vs DC for skill checks
- Simplified combat: no grid, no initiative rolls, one action per turn
- 2-3 uses per ability per adventure (DM tracks)
- 0 HP = unconscious, not healed by next turn = dead

The DM is the final arbiter of all rules.

## License

MIT
