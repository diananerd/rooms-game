#!/usr/bin/env python3
"""
Save a mcp-rooms.com chat log to a formatted text file.

Usage:
    python3 scripts/save-chat-log.py <json_file> <output_file> [--title TITLE] [--players PLAYERS]

The JSON file should be the raw output from mcp__rooms__read_channel,
which is a JSON array containing an object with a "text" field that
holds the actual messages JSON string.

Example:
    python3 scripts/save-chat-log.py /path/to/tool-result.json examples/2026-03-28-my-game.txt \
        --title "The Whispering Crypt" \
        --players "Mordecai (DM), Thorin (Fighter), Lyra (Wizard)"
"""

import json
import datetime
import argparse
import sys
import os


def parse_messages(json_file):
    """Parse messages from the rooms read_channel JSON output."""
    with open(json_file) as f:
        data = json.load(f)

    # Handle nested JSON structure from MCP tool results
    if isinstance(data, list) and len(data) > 0 and "text" in data[0]:
        inner = json.loads(data[0]["text"])
        messages = inner.get("messages", [])
    elif isinstance(data, dict) and "messages" in data:
        messages = data["messages"]
    elif isinstance(data, list) and len(data) > 0 and "nick" in data[0]:
        messages = data
    else:
        print(f"Error: unrecognized JSON structure in {json_file}", file=sys.stderr)
        sys.exit(1)

    return messages


def format_log(messages, title=None, channel=None, players=None, extra_headers=None):
    """Format messages into a readable chat log."""
    if not messages:
        return ""

    first_ts = messages[0]["createdAt"]
    last_ts = messages[-1]["createdAt"]
    first_dt = datetime.datetime.fromtimestamp(first_ts / 1000, tz=datetime.timezone.utc)
    last_dt = datetime.datetime.fromtimestamp(last_ts / 1000, tz=datetime.timezone.utc)
    duration = last_dt - first_dt
    duration_min = int(duration.total_seconds() / 60)
    date_str = first_dt.strftime("%Y-%m-%d")

    lines = []

    # Header
    if title:
        lines.append(f"# {title}")
    lines.append(f"# D&D Session — {date_str}")
    if channel:
        lines.append(f"# Channel: {channel} @ mcp-rooms.com")
    if players:
        lines.append(f"# Players: {players}")
    lines.append(f"# Messages: {len(messages)}")
    lines.append(f"# Duration: ~{duration_min} minutes")
    if extra_headers:
        for h in extra_headers:
            lines.append(f"# {h}")
    lines.append("#")
    lines.append("")

    # Messages
    for msg in messages:
        ts = msg["createdAt"]
        dt = datetime.datetime.fromtimestamp(ts / 1000, tz=datetime.timezone.utc)
        time_str = dt.strftime("%H:%M:%S")
        nick = msg["nick"]
        content = msg["content"]

        # Try to parse structured cards (roll, giphy, status, etc.)
        display = content
        try:
            card = json.loads(content)
            if isinstance(card, dict) and "type" in card:
                card_type = card["type"]
                data = card.get("data", {})
                if card_type == "roll":
                    stat = f"{data.get('stat', '')} " if data.get("stat") else ""
                    dc = f" vs DC {data['dc']}" if data.get("dc") else ""
                    result = f" → {data['result']}" if data.get("result") else ""
                    display = f"[ROLL] {stat}{data.get('dice', '?')}: {data.get('rolls', [])} +{data.get('mod', 0)} = {data.get('total', '?')}{dc}{result}"
                elif card_type == "giphy":
                    display = f"[GIF] {data.get('query', '?')} — {data.get('url', '')}"
                elif card_type == "topic":
                    display = f"[TOPIC] {data.get('text', '?')}"
                elif card_type == "status":
                    conds = f" ({', '.join(data['conditions'])})" if data.get("conditions") else ""
                    display = f"[STATUS] {data.get('name', '?')} — HP: {data.get('hp', '?')} AC: {data.get('ac', '?')}{conds}"
                elif card_type == "initiative":
                    turns = " → ".join(t.get("name", "?") for t in data.get("turns", []))
                    display = f"[INITIATIVE] Round {data.get('round', '?')}: {turns}"
                elif card_type == "scoreboard":
                    display = f"[SCOREBOARD] {data.get('title', '?')} — Result: {data.get('result', '?')} — MVP: {data.get('mvp', '?')}"
                elif card_type == "loot":
                    items = ", ".join(data.get("items", []))
                    display = f"[LOOT] {data.get('title', 'Loot')}: {items}"
                else:
                    display = f"[{card_type.upper()}] {json.dumps(data, ensure_ascii=False)}"
        except (json.JSONDecodeError, TypeError, KeyError):
            pass

        lines.append(f"[{time_str}] <{nick}> {display}")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Save a rooms chat log to formatted text")
    parser.add_argument("json_file", help="Path to the JSON file from read_channel")
    parser.add_argument("output_file", help="Path for the output text file")
    parser.add_argument("--title", help="Adventure title for the header")
    parser.add_argument("--channel", help="Channel name")
    parser.add_argument("--players", help="Player list for the header")
    parser.add_argument("--header", action="append", dest="extra_headers",
                        help="Additional header lines (can be used multiple times)")

    args = parser.parse_args()

    messages = parse_messages(args.json_file)
    if not messages:
        print("No messages found.", file=sys.stderr)
        sys.exit(1)

    output = format_log(
        messages,
        title=args.title,
        channel=args.channel,
        players=args.players,
        extra_headers=args.extra_headers,
    )

    os.makedirs(os.path.dirname(os.path.abspath(args.output_file)), exist_ok=True)
    with open(args.output_file, "w") as f:
        f.write(output)

    print(f"Saved {len(messages)} messages to {args.output_file}")


if __name__ == "__main__":
    main()
