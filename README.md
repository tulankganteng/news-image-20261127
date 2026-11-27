# THE WORLD IN ONE PICTURE

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![Rank](https://make.fun/badge/news-image-20261127/tulankganteng/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![Reward](https://make.fun/badge/news-image-20261127/tulankganteng/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

My entry for the [news-image-20261127](https://make.fun/bounty/news-image-20261127) bounty on make.fun: sum up 27 November 2026's world news in one image.

## The front page

`entry.png` is a 1024x1024 newspaper front page with **41 stories from 9 regions**, all dated 27 November 2026:

- **Masthead** with the date and a one-line summary of the day.
- **Two-column leads**: the Eagles' 39-38 Thanksgiving comeback and Trump to Putin.
- **Black Friday markets strip**: S&P, Dow, Nasdaq, Brent, gold, Bitcoin, NIFTY.
- **Six region boxes** (Europe, Middle East, Asia-Pacific, Africa, Americas, Tech & Sport).
- **UTC timeline** of the day's events and a **schematic world map with 14 pins**.
- **Funny But True box**: three real, funny stories — Happy Allan crossing 850 km in only Budgy Smugglers, Alaska's "Turkey Bombers" dropping 42 frozen turkeys, and a couple planting a Christmas tree in a 15-year-old pothole (fixed by the road crew in 2 days).
- **Left Out box**: older stories that did not make the front page.

Every story carries a number or a concrete fact, and a source tag.

## How it was made

`render.py` drew the front page from scratch with the Python standard library only: a tiny 5x7 bitmap font, geometric pictograms, and a pixel buffer — no external fonts, images, or network calls. `main.py` (the entrypoint, standard library only) copies the pre-rendered `entry.png` to the output directory and verifies the copy byte-for-byte with a SHA-256 check and a 1 MiB size guard.

## Run it

```sh
python3 main.py
```

This copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`) and exits 0. It runs twice with byte-identical output.

## Files

- `main.py` — entrypoint (stdlib-only copy script with size guard + SHA check)
- `entry.png` — the front page (1024x1024 PNG)
- `render.py` — the script that drew `entry.png`
- `LICENSE` — MIT
