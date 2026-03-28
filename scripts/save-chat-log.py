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
        lines.append(f"[{time_str}] <{nick}> {content}")

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
