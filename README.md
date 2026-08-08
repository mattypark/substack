# substack

**Tuner** — spin a dial, get one Substack topic. Nothing else on the page.

1,014 prompts. Click the scale or press `space` to respin. Toggle dark/white in the top-left; the orange stays orange.

Sound taken from [unprompted.cool](https://www.unprompted.cool/).

## Run it

```bash
open index.html
```

One self-contained file. No build step to view, no network calls.

## Edit it

- `src/topics.js` — the pool. One string per line, grouped by strand in comments. Add lines anywhere.
- `src/page.html` — layout and behavior.

Rebuild after either:

```bash
python3 tools/build.py
```

Writes `index.html` (standalone) and `build/artifact.html` (head-less fragment for republishing as a Claude artifact).

## Fonts

Anthropic Serif, inlined as base64 `@font-face` rules — the artifact CSP blocks external font hosts. `tools/build.py` reads the `.otf` files from `~/Library/Fonts`, so rebuilding needs them installed; the committed `index.html` already carries them.
