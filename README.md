# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/ydhikaaa/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/ydhikaaa/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One-page newspaper front page summing up Saturday 21 November 2026 world news: 35 stories across 7 regions, drawn with Python/PIL.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=nmjakjk9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>

# Saturday 21 November 2026: 35 stories, 7 regions — COP31 overtime, Saudi missiles downed, Peru quake

One image that sums up the world's news of Saturday 21 November 2026:
COP31 running into overtime in Antalya with no deal, five Houthi
missiles shot down over Saudi Arabia, and a magnitude 6.7 earthquake
in Peru — 35 verified stories from 7 regions, drawn as a one-page
newspaper front page, with a DATE CHECK box naming the 20-November
stories deliberately left out (including the missile that landed in
Poland).

## How it works

`render.py` draws the front page (`frontpage.png`, 1024x1024) with PIL:
a top strip, a giant serif date headline, an italic lead line, a stats
strip, a region-count bar, thirteen drawn story panels with red banner
labels, numbered kickers, verification badges, a world map with
numbered pins, a numbered ALSO list of 22 more stories with sources,
and a DATE CHECK box. `main.py` (stdlib only) copies `frontpage.png`
to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Both runs of `main.py` produce byte-identical output.
