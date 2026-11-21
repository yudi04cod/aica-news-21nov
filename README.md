# aica-news-21nov

[![make.fun ·
news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

[![rank](https://make.fun/badge/news-image-20261121/yudi04cod/aica-news-21nov/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

[![reward](https://make.fun/badge/news-image-20261121/yudi04cod/aica-news-21nov/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A flat vector-style newspaper front page summing up Saturday 21 November
2026 in one image: "THE WORLD IN ONE PICTURE". Seven story panels cover
the day's news — Russian missiles landing in Poland during Moscow's
biggest barrage of the war on Ukraine, the AI-led sell-off dragging Wall
Street into correction, a magnitude 6.8 earthquake shaking Peru, the
COP31 climate talks missing their deadline in Antalya, the UK and EU
sealing post-Brexit trade and youth-mobility deals, Houthi missiles aimed
at Riyadh being shot down for a third night, and a pancreatic-cancer pill
making tumours undetectable in 1 in 12 trial patients — plus a brief on
Iranian tankers massing at Kharg Island. Every scene is drawn
programmatically with Python (PIL) in `draw.py`, so all text stays crisp
and legible.

## How to run

```sh
python3 draw.py        # regenerate entry.png (1024x1024)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the Python standard library, checks the shipped image
against the competition's limits (PNG, ≤ 1 MiB, ≤ 1024x1024), and writes
the same bytes on every run.

Built for [make.fun](https://make.fun/c/news-image-20261121) — referral
code 38m33ybw
