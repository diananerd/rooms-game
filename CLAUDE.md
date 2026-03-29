# Room Game: Autonomous D&D

When the user says **"lanza la partida"** (or any variation like "nueva partida", "start a game"), launch the game following this procedure exactly. No questions, no planning — just go.

## Language

Default language is **Spanish**. All prompts, narration, and messages must be in Spanish unless the user explicitly requests another language.

## Launch Procedure

### Step 1: Launch the DM

Spawn one background agent with `bypassPermissions`, model `sonnet`:

```
Eres el Dungeon Master. Lee tu hoja de personaje y las reglas del juego:
- agents/dungeon-master.md
- shared/dnd-rules.md

Únete a #general en el servidor de rooms. Prepara la aventura de esta noche y dirige la partida.

IMPORTANTE: Toda la partida debe jugarse EN ESPAÑOL. Toda la narración, diálogos, anuncios y mensajes en los canales deben ser en español.
```

### Step 2: Wait ~15 seconds, then launch 4 players in parallel

Each player gets the same structure. All with `bypassPermissions`, `run_in_background`, model `sonnet`:

| Character | File | Prompt name |
|-----------|------|-------------|
| Thorin (Guerrero) | agents/fighter.md | Thorin, el Guerrero |
| Lyra (Maga) | agents/wizard.md | Lyra, la Maga |
| Sketch (Pícaro) | agents/rogue.md | Sketch, el Pícaro |
| Aldric (Clérigo) | agents/cleric.md | Aldric, el Clérigo |

Player prompt template:

```
Eres [NOMBRE]. Lee tu hoja de personaje y las reglas del juego:
- agents/[file].md
- shared/dnd-rules.md

Únete a #general en el servidor de rooms. El DM organizará la partida desde ahí.

IMPORTANTE: Toda la partida se juega EN ESPAÑOL. Todos tus mensajes, diálogos y comentarios deben ser en español. Mantén tu personalidad de personaje pero habla español.
```

### Step 3: Tell the user the game is live

The user watches at mcp-rooms.com. Notify them when agents are launched.

## Critical Rules

- **ZERO MCP tool names in agent prompts** — agents discover tools from schemas
- **ZERO channel IDs in prompts** — agents find channels by listing/reading
- Use **relative paths** (agents/fighter.md, not absolute paths) so it works on any machine
- All agents use model **sonnet** (cost-effective, proven sufficient)
- All agents use **bypassPermissions** mode
