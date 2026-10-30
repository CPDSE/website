#!/usr/bin/env python3
"""Generate one .ics calendar invitation per FrAIday Bar session.

Source of truth is _data/fraiday_bar.yml. Output goes to assets/calendar/,
one file per session, linked from the programme cards on /people-development/.

Run from the repository root:

    python3 scripts/generate-fraiday-ics.py

Re-run after changing the room, a date, or a title in _data/fraiday_bar.yml.
Output is deterministic, so re-running with no data change produces no git diff.
"""

from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  python3 -m pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_data" / "fraiday_bar.yml"
OUTDIR = ROOT / "assets" / "calendar"

# Fixed so regeneration does not churn the git history.
DTSTAMP = "20260731T000000Z"
PRODID = "-//CPDSE//FrAIday Bar//EN"


def esc(text):
    """Escape per RFC 5545 section 3.3.11."""
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold(line):
    """Fold to <=75 octets per RFC 5545 section 3.1, continuation lines start with a space."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        limit = 75 if not out else 74  # continuation lines lose one octet to the leading space
        if len(cur) + len(b) > limit:
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


def main():
    cfg = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    tz = ZoneInfo(cfg["timezone"])
    sh, sm = (int(x) for x in str(cfg["start_time"]).split(":"))
    eh, em = (int(x) for x in str(cfg["end_time"]).split(":"))

    OUTDIR.mkdir(parents=True, exist_ok=True)
    fmt = lambda dt: dt.astimezone(ZoneInfo("UTC")).strftime("%Y%m%dT%H%M%SZ")

    def vevent(s):
        """Build one VEVENT. Used for both the per-session files and the whole-series
        file, so a session added by either route carries the same UID and calendars
        treat them as one event rather than creating a duplicate."""
        d = s["date"]
        if isinstance(d, str):
            d = datetime.strptime(d, "%Y-%m-%d").date()

        # Local wall-clock time in Copenhagen, converted to UTC. zoneinfo applies
        # the correct CEST/CET offset per date, so DST is never hand-calculated.
        start_local = datetime(d.year, d.month, d.day, sh, sm, tzinfo=tz)
        end_local = datetime(d.year, d.month, d.day, eh, em, tzinfo=tz)
        desc = (
            f"{s['summary']}\n\n"
            f"You leave with: {s['artifact']}\n\n"
            f"FrAIday Bar is CPDSE's hands-on AI community. One hour, one practical "
            f"skill, no ECTS and nothing to prepare - bring a laptop and a real task.\n\n"
            f"Programme and details: {cfg['page_url']}"
        )
        return d, start_local, [
            "BEGIN:VEVENT",
            f"UID:fraiday-bar-{d.isoformat()}@cpdse.dk",
            f"DTSTAMP:{DTSTAMP}",
            "SEQUENCE:0",
            "STATUS:CONFIRMED",
            "TRANSP:OPAQUE",
            f"DTSTART:{fmt(start_local)}",
            f"DTEND:{fmt(end_local)}",
            f"SUMMARY:{esc('FrAIday Bar: ' + s['title'])}",
            f"DESCRIPTION:{esc(desc)}",
            f"LOCATION:{esc(cfg['location'])}",
            f"URL:{cfg['page_url']}",
            f"ORGANIZER;CN={esc(cfg['organiser_name'])}:mailto:{cfg['organiser_email']}",
            "END:VEVENT",
        ]

    def wrap(body, calname=None):
        head = ["BEGIN:VCALENDAR", "VERSION:2.0", f"PRODID:{PRODID}",
                "CALSCALE:GREGORIAN", "METHOD:PUBLISH"]
        if calname:
            head += [f"X-WR-CALNAME:{esc(calname)}"]
        return ("\r\n".join(fold(l) for l in head + body + ["END:VCALENDAR"]) + "\r\n").encode("utf-8")

    written, all_events = [], []
    for s in cfg["sessions"]:
        d, start_local, body = vevent(s)
        all_events += body
        path = OUTDIR / f"fraiday-bar-{d.isoformat()}.ics"
        path.write_bytes(wrap(body))
        written.append((path.relative_to(ROOT), fmt(start_local), s["title"]))

    series = OUTDIR / "fraiday-bar-autumn-2026.ics"
    series.write_bytes(wrap(all_events, calname="FrAIday Bar — autumn 2026"))

    for p, start, title in written:
        print(f"  {start}  {p}   {title}")
    print(f"  {'':16}  {series.relative_to(ROOT)}   ALL {len(written)} SESSIONS")
    print(f"\n{len(written)} per-session invitations + 1 whole-series file "
          f"written to {OUTDIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
