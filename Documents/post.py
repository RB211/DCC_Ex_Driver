#!/usr/bin/env python3
"""Re-expand the run-on parameter blocks produced by |br| collapsing."""
import re, sys

# leading blockquote markers, if any, are carried onto every line we emit
PREFIX = re.compile(r"^((?:>\s*)*)(.*)$")
LIST = re.compile(r"^(?:>\s*)*\s*- ")
ESC = re.compile(r"\\<|\\>")


def split_markers(body):
    """Split on the "\\>" markers that start a new parameter entry.

    A "\\>" that closes an escaped "\\<...\\>" pair is literal protocol syntax
    ("<H id state>", "<t >", "<1 MAIN>") and must survive intact, so pairs are
    tracked and only an unmatched "\\>" counts. A marker must also be
    whitespace-delimited, as it was in the |br|-separated original.
    """
    parts, last, depth = [], 0, 0
    for m in ESC.finditer(body):
        if m.group(0) == "\\<":
            depth += 1
            continue
        if depth:                       # closes an escaped \<...\> pair
            depth -= 1
            continue
        before, after = body[:m.start()], body[m.end():]
        if before.strip() and not before[-1:].isspace():
            continue
        if after and not after[:1].isspace():
            continue
        parts.append(body[last:m.start()])
        last = m.end()
    parts.append(body[last:])
    return parts


def fix_line(ln):
    m = PREFIX.match(ln)
    quote, body = m.group(1).rstrip(), m.group(2)
    if "\\>" not in body and "•" not in body:
        return ln
    chunks = split_markers(body)
    if len(chunks) == 1 and "•" not in body:
        return ln                       # every "\>" was an escaped bracket
    pad = quote + " " if quote else ""

    rows = []
    head, rest = chunks[0], chunks[1:]
    if head.strip():
        rows.append(pad + head.strip())
    rows.extend(pad + "- " + c.strip() for c in rest)

    # each "•" starts a nested option under the entry it appears in
    out = []
    for row in rows:
        if "•" not in row:
            out.append(row)
            continue
        segs = [s.strip() for s in row.split("•")]
        out.append(segs[0].rstrip())
        out.extend(pad + "  - " + s for s in segs[1:] if s)

    # trailing spaces would become markdown hard-breaks and swallow the list
    out = [r.rstrip() for r in out]
    return "\n".join(r for r in out if r.strip() not in ("", ">", "-", "> -", ">   -"))


def blank_before_lists(lines):
    """pandoc needs a blank line before a list that follows a paragraph."""
    out = []
    for ln in lines:
        if LIST.match(ln) and out:
            prev = out[-1]
            pm = PREFIX.match(prev)
            if pm.group(2).strip() and not LIST.match(prev):
                out[-1] = prev.rstrip()          # drop the hard-break spaces
                out.append(pm.group(1).rstrip())
        out.append(ln)
    return out


src = open(sys.argv[1], encoding="utf-8").read().split("\n")
lines = "\n".join(fix_line(l) for l in src).split("\n")
sys.stdout.write("\n".join(blank_before_lists(lines)))
