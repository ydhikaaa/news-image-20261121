# Saturday 21 November 2026: 36 stories, 7 regions

One image that sums up the world's news of Saturday 21 November 2026:
Russian missiles landing in Poland, Trump's post-Asia press conference,
COP31 running into overtime in Antalya, Cyclone Akvan hitting India,
and the Ashes opening at Perth — 36 verified stories from 7 regions,
drawn as a one-page newspaper front page.

## How it works

`render.py` draws the front page (`frontpage.png`, 1024x1024) with PIL:
masthead, giant date headline, lead stories, four drawn visual panels,
a stats strip, a region-count bar, a world map with numbered pins, and
36 numbered stories with sources. `main.py` (stdlib only) copies
`frontpage.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Both runs of `main.py` produce byte-identical output.
