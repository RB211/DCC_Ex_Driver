#!/bin/bash
set -e
cd /home/claude
mkdir -p out parts
DOCS=/home/claude/rst/docs
REV=$(cd rst && git log -1 --format='%ad' --date=short)
SHA=$(cd rst && git log -1 --format='%h')

# order: overview -> syntax -> full command set -> throttle guide -> exrail -> diagnostics
FILES=(
"throttles/protocols.rst|Protocols Overview: WiThrottle Server, Web Server, DCC-EX Native"
"reference/software/withrottle-vs-native-commands.rst|WiThrottle Protocol vs DCC-EX Native Commands"
"reference/developers/api.rst|DCC-EX Native API Reference (syntax and parsing rules)"
"throttles/tech-reference.rst|Technical Reference for Throttle Developers"
"reference/software/command-summary-consolidated.rst|DCC-EX Native Commands Summary Reference"
"exrail/exrail-command-reference.rst|EXRAIL Command Reference"
"ex-fastclock/cs-commands.rst|EX-FastClock Command Station Commands"
"reference/tools/diagnostic-d-command.rst|Diagnostics <D> Command"
"reference/tools/diagnostic-d-ack-command.rst|Diagnostics <D ACK> Command"
)

cat > out/dccex-native-protocol.md <<EOF
---
title: "DCC-EX Native Command Protocol -- Consolidated Reference"
subtitle: "Compiled from the official DCC-EX documentation (rev $SHA, $REV)"
date: "$(date +%Y-%m-%d)"
---

# About This Document

This is an offline compilation of the DCC-EX EX-CommandStation **native command
protocol** documentation, assembled from the official DCC-EX documentation
source (\`github.com/DCC-EX/dcc-ex.github.io\`, branch \`sphinx\`, commit \`$SHA\`,
dated $REV). Content is (c) the DCC-EX team and is licensed GPL-3.0.

Source pages included:

EOF

for entry in "${FILES[@]}"; do
  f="${entry%%|*}"
  echo "* \`docs/$f\`" >> out/dccex-native-protocol.md
done

cat >> out/dccex-native-protocol.md <<'EOF'

Canonical online versions live at <https://dcc-ex.com/>. Note that DCC-EX
maintains a newer auto-generated command page at
<https://dcc-ex.com/mkdocs-test/reference/serial-commands/> which may list
commands added after this snapshot.

\newpage

EOF

for entry in "${FILES[@]}"; do
  f="${entry%%|*}"
  title="${entry##*|}"
  base=$(echo "$f" | tr '/' '_' | sed 's/\.rst$//')
  echo ">>> $f"
  python3 prep.py "$DOCS/$f" > "parts/$base.rst"
  pandoc -f rst -t gfm --wrap=none "parts/$base.rst" -o "parts/$base.md" 2>>out/pandoc-warnings.log
  {
    echo ""
    echo "\\newpage"
    echo ""
    cat "parts/$base.md"
    echo ""
  } >> out/dccex-native-protocol.md
done

wc -c out/dccex-native-protocol.md

# restore list structure lost when |br| collapsed, and fix a glyph DejaVu Serif lacks
python3 post.py out/dccex-native-protocol.md | sed 's/✓/Yes/g' > out/_t.md
mv out/_t.md out/dccex-native-protocol.md

pandoc out/dccex-native-protocol.md \
  -o out/DCC-EX-Native-Protocol-Reference.pdf \
  --pdf-engine=xelatex --toc --toc-depth=3 --number-sections \
  -V geometry:"margin=0.75in" -V fontsize=10pt -V colorlinks=true \
  -V linkcolor=RoyalBlue -V urlcolor=RoyalBlue \
  -V mainfont="DejaVu Serif" -V sansfont="DejaVu Sans" -V monofont="DejaVu Sans Mono" \
  -V monofontoptions="Scale=0.82" -V documentclass=report 2>&1 | grep -iE "missing char|error" | head
