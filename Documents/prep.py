#!/usr/bin/env python3
"""Flatten DCC-EX Sphinx RST into pandoc-friendly RST."""
import re, sys, os, glob, html

DOCS = "/home/claude/rst/docs"

# ---------- 1. harvest substitution definitions from include/*.rst ----------
subs = {}

def strip_html(s):
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()

def _xref_label(target):
    """Turn a Sphinx xref target into readable text."""
    t = target.strip().strip("/")
    if ":" in t:                       # path/to/page:section name
        t = t.split(":", 1)[1]
    else:                              # /path/to/page
        t = t.rsplit("/", 1)[-1]
        t = t.replace("-", " ").replace("_", " ")
    t = t.strip()
    return t[:1].upper() + t[1:] if t else target

def strip_roles(s):
    # :doc:`Label </path>` / :ref:`Label <tgt>`  -> Label
    s = re.sub(r":(?:doc|ref|term|download|numref):`([^<`]*?)\s*<[^>]*>`", r"\1", s)
    # :doc:`/path` / :ref:`page:section` -> readable label
    s = re.sub(r":(?:doc|ref|term|download|numref):`([^`]*)`",
               lambda m: _xref_label(m.group(1)), s)
    # generic :role:`text` -> text
    s = re.sub(r":[a-zA-Z0-9_+:.-]+:`([^`]*)`", r"\1", s)
    s = s.replace("\\ ", "")
    return s.strip()

def harvest(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^\.\. \|([^|]+)\|\s+(\w+)::\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        name, kind, inline = m.group(1), m.group(2), m.group(3)
        # for raw:: the inline arg is the output format, not content
        body = [] if kind == "raw" else ([inline] if inline.strip() else [])
        j = i + 1
        while j < len(lines):
            ln = lines[j]
            if ln.strip() == "":
                if body and not any(l.strip() for l in lines[j:j+2]):
                    break
                body.append("")
                j += 1
                continue
            if ln.startswith((" ", "\t")):
                body.append(ln.strip())
                j += 1
                continue
            break
        text = " ".join(x for x in body if x.strip())
        if kind == "image":
            val = ""                                   # drop badges/logos
        elif kind == "raw":
            val = strip_html(text)
        elif kind == "unicode":
            val = " "
        elif kind == "replace":
            val = strip_roles(text)
        else:
            val = strip_roles(text)
        val = re.sub(r"\s*:(?:alt|scale|class|width|height|target|trim|align)\s*:.*$", "", val).strip()
        subs[name] = val
        i = j

for f in sorted(glob.glob(os.path.join(DOCS, "include", "*.rst"))):
    harvest(f)

subs.setdefault("br", " ")
subs.setdefault("_", " ")
subs.setdefault("hr", "")
subs.setdefault("hr-dashed", "")

SUB_RE = re.compile(r"\|([^|\n]{1,60})\|")
SUBS_CI = {}

def _build_ci():
    for k, v in subs.items():
        SUBS_CI[k.lower()] = v

def apply_subs(text):
    if not SUBS_CI:
        _build_ci()
    def rep(m):
        k = m.group(1).lower()
        if k in SUBS_CI:
            v = SUBS_CI[k]
            return v if v else ""
        return m.group(0)
    prev = None
    for _ in range(3):
        if text == prev:
            break
        prev = text
        text = SUB_RE.sub(rep, text)
    return text

# ---------- 2. clean a page ----------
DROP_DIRECTIVES = ("include", "meta", "raw", "image", "figure", "toctree",
                   "sidebar", "role", "contents", "only", "index")

def clean(path):
    src = open(path, encoding="utf-8").read()
    out, lines = [], src.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^(\s*)\.\.\s+(\w[\w-]*)::", ln)
        if m and m.group(2) in DROP_DIRECTIVES:
            indent = len(m.group(1))
            i += 1
            while i < len(lines) and (lines[i].strip() == "" or
                   len(lines[i]) - len(lines[i].lstrip()) > indent):
                i += 1
            continue
        # substitution definitions
        if re.match(r"^\.\. \|[^|]+\|\s+\w+::", ln):
            i += 1
            while i < len(lines) and (lines[i].strip() == "" or lines[i].startswith((" ", "\t"))):
                i += 1
            continue
        # collapsible / dropdown -> keep content, turn into a note heading
        m2 = re.match(r"^(\s*)\.\.\s+(dropdown|collapse|details)::\s*(.*)$", ln)
        if m2:
            out.append(f"{m2.group(1)}**{m2.group(3).strip() or 'Details'}**")
            i += 1
            continue
        out.append(ln)
        i += 1
    txt = "\n".join(out)
    txt = re.sub(r"^(\s*)\.\.\s+flat-table::", r"\1.. list-table::", txt, flags=re.M)
    txt = re.sub(r":(?:cspan|rspan):`\d+`\s*", "", txt)
    txt = apply_subs(txt)
    txt = strip_roles(txt)
    # sphinx-only options that survive
    txt = re.sub(r"^\s*:(?:alt|scale|class|width|height|align|target|name|trim|open|animate|color|icon|margin):.*$",
                 "", txt, flags=re.M)
    return txt

if __name__ == "__main__":
    sys.stdout.write(clean(sys.argv[1]))
