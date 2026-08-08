# substack

**Tuner** — a radio-dial spinner that hands me one Substack topic at a time, pulled only from things I have actually built, shipped, quit, posted, or argued about.

Sound taken from [unprompted.cool](https://www.unprompted.cool/): spin a thoughtful topic, then talk.

## Two modes

| Mode | What you get |
|------|--------------|
| **Off the cuff** | The topic, one provocation, and a 60-second timer. Speak it out loud. |
| **Deep cut** | A three-beat outline, the part only I can write, and an opening line to steal. |

36 topics across eight strands — shipping, agents, internet, school, leading, craft, discipline, money. Draw order is a shuffle bag, so nothing repeats until the pool is empty. Strand chips narrow the pool. `space` respins.

## Run it

```bash
open index.html
```

That is the whole thing — one self-contained file, no build step to view, no network calls.

## Edit it

All content and behavior lives in `src/page.html`. The topic pool is the `TOPICS` array near the top of the script:

```js
{
  strand: "shipping",
  title: "The project I abandoned at ninety percent",
  premise: "...",     // the one-line frame
  cuff: "...",        // the off-the-cuff provocation
  beats: ["...", "...", "..."],
  honest: "...",      // the part only I can write
  opener: "..."       // a first line to steal
}
```

After editing, rebuild:

```bash
python3 tools/build.py
```

That inlines the fonts and writes both outputs:

- `index.html` — standalone page
- `build/artifact.html` — head-less fragment for republishing as a Claude artifact

## Fonts

Anthropic Serif, inlined as base64 `@font-face` rules because the artifact CSP blocks external font hosts. `tools/build.py` reads the `.otf` files from `~/Library/Fonts`, so anyone cloning this needs those installed locally to rebuild — the committed `index.html` already carries them.

## Design

White ground, Claude orange (`#D97757`) on the dial and headings, deeper burnt orange (`#A83E1C`) for large text so contrast holds on white. Light and dark both defined at token level, including the un-stamped system-default state.
