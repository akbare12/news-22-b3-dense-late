# The World in One Day — Sunday 22 November 2026

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b3-dense-late/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b3-dense-late/reward.svg)](https://make.fun/bounty/news-image-20261122)

A dense newspaper front page summing up the world's news of **Sunday 22 November 2026** in one image: 34 stories, 13 illustration panels, a pinned world map, an explicit verification legend (CONFIRMED / OFFICIAL / REPORTED / CLAIM), a big-number strip, a UTC timeline and a date-check footer. Lead story: two supertankers hit mines near the Strait of Hormuz (first reported 17:13 UTC, the day's latest wire).

## How it works

`draw.py` renders `entry.png` (1024×1024) with Pillow on the build machine. `main.py` (Python 3.13, standard library only) copies `entry.png` to `/output/entry.png` and verifies size + sha256 of the copy.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Entry for the [news-image-20261122](https://make.fun/bounty/news-image-20261122) bounty on make.fun.
