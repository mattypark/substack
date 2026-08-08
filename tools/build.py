#!/usr/bin/env python3
"""Build Tuner.

Inlines Anthropic Serif as base64 @font-face rules (the Claude artifact CSP
blocks external font hosts, and GitHub Pages should not depend on one either),
then emits two files from the single source fragment in src/page.html:

  index.html          standalone page — open it directly or serve it
  build/artifact.html fragment for republishing as a Claude artifact
                      (no doctype/head — the artifact host supplies those)

Fonts are read from ~/Library/Fonts. Run this after editing src/page.html.
"""

import base64
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "page.html"
FONT_DIR = pathlib.Path.home() / "Library" / "Fonts"

FACES = [
    ("AnthropicSerif-Display-Light-Static.otf", "Anthropic Display", 300, "normal"),
    ("AnthropicSerif-Text-Regular-Static.otf", "Anthropic Text", 400, "normal"),
    ("AnthropicSerif-Text-RegularItalic-Static.otf", "Anthropic Text", 400, "italic"),
    ("AnthropicSerif-Text-Semibold-Static.otf", "Anthropic Text", 600, "normal"),
]

DOC_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A radio-dial spinner for Substack topics drawn from things I have actually built, shipped, quit, or argued about.">
"""

DOC_TAIL = """
</body>
</html>
"""


def font_css() -> str:
    missing = [name for name, *_ in FACES if not (FONT_DIR / name).is_file()]
    if missing:
        print(f"error: fonts not found in {FONT_DIR}:", file=sys.stderr)
        for name in missing:
            print(f"  {name}", file=sys.stderr)
        print("install Anthropic Serif, or point FONT_DIR at the files.", file=sys.stderr)
        raise SystemExit(1)

    blocks = []
    for name, family, weight, style in FACES:
        encoded = base64.b64encode((FONT_DIR / name).read_bytes()).decode()
        blocks.append(
            "@font-face {\n"
            f'  font-family: "{family}";\n'
            f"  font-weight: {weight};\n"
            f"  font-style: {style};\n"
            "  font-display: swap;\n"
            f'  src: url(data:font/otf;base64,{encoded}) format("opentype");\n'
            "}"
        )
    return "\n".join(blocks)


def main() -> None:
    fragment = SRC.read_text().replace("__FONTS__", font_css())

    artifact = ROOT / "build" / "artifact.html"
    artifact.parent.mkdir(exist_ok=True)
    artifact.write_text(fragment)

    # The fragment opens with <title>…</title>, which belongs in <head>.
    title_end = fragment.index("</title>") + len("</title>")
    head_extra, body = fragment[:title_end], fragment[title_end:]
    standalone = f"{DOC_HEAD}{head_extra}\n</head>\n<body>{body}{DOC_TAIL}"

    index = ROOT / "index.html"
    index.write_text(standalone)

    for path in (index, artifact):
        print(f"wrote {path.relative_to(ROOT)}  {path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
