# baseball-field-viz

A Python library for drawing baseball fields and spray charts from [Statcast](https://baseballsavant.mlb.com/) data.

Companion to [savant-extras](https://github.com/yasumorishima/savant-extras) — together they provide a seamless MLB analysis pipeline.

## Installation

```bash
pip install baseball-field-viz
```

## Why this library?

pybaseball's built-in `spraychart()` doesn't support overlaying heatmaps (e.g. seaborn `kdeplot`). This library gives you a matplotlib `Axes` object directly, so you can layer any plot on top.

```python
from baseball_field_viz import draw_field
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 10))
draw_field(ax)
sns.kdeplot(data=df_t, x="x", y="y", ax=ax, cmap="Reds", fill=True, alpha=0.6)
```

## Quick Start

```python
import matplotlib.pyplot as plt
from baseball_field_viz import draw_field, spraychart, transform_coords

# Spray chart (one-liner)
fig, ax = plt.subplots(figsize=(10, 10))
spraychart(ax, df, color_by="events", title="Ohtani 2025 - Batted Balls")
plt.show()
```

## Functions

### `transform_coords(df)`

Convert Statcast `hc_x`/`hc_y` to feet coordinates (home plate at origin).

```python
from baseball_field_viz import transform_coords

df_t = transform_coords(df)
# Adds 'x' and 'y' columns in feet
# x = 2.5 * (hc_x - 125.42)
# y = 2.5 * (198.27 - hc_y)
```

### `draw_field(ax, foul_distance=330, outfield_distance=340)`

Draw a baseball field on a matplotlib `Axes`.

```python
from baseball_field_viz import draw_field

fig, ax = plt.subplots(figsize=(10, 10))
draw_field(ax)
# Now overlay any plot: scatter, kdeplot, histplot, etc.
```

### `spraychart(ax, df, color_by="events", title=None)`

Draw a spray chart in one call. Internally calls `transform_coords` and `draw_field`.

```python
from baseball_field_viz import spraychart

fig, ax = plt.subplots(figsize=(10, 10))
spraychart(ax, df, color_by="events", title="Player - Season")
plt.show()
```

**`color_by` options:**

| Value | Effect |
|---|---|
| `"events"` (default) | home_run=red, triple=orange, double=blue, single=green, other=gray |
| Any column name | Categorical coloring with auto palette |

## Full Example with Heatmap

```python
from pybaseball import statcast
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns
from baseball_field_viz import draw_field, transform_coords

# Fetch data
df_raw = statcast(start_dt="2025-03-01", end_dt="2025-10-31")
con = duckdb.connect()
df = con.execute("""
    SELECT * FROM df_raw
    WHERE batter = 660271
      AND hc_x IS NOT NULL AND hc_y IS NOT NULL
      AND game_type = 'R'
""").df()

df_t = transform_coords(df)

# Hits vs outs heatmap
fig, axs = plt.subplots(1, 2, figsize=(16, 8))

hits = df_t[df_t["events"].isin(["home_run", "double", "triple", "single"])]
outs = df_t[~df_t["events"].isin(["home_run", "double", "triple", "single"])]

draw_field(axs[0])
sns.kdeplot(data=hits, x="x", y="y", ax=axs[0], cmap="Reds", fill=True, alpha=0.6)
axs[0].set_xlim(-350, 350); axs[0].set_ylim(-50, 400)
axs[0].set_title("Hits Heatmap")

draw_field(axs[1])
sns.kdeplot(data=outs, x="x", y="y", ax=axs[1], cmap="Blues", fill=True, alpha=0.6)
axs[1].set_xlim(-350, 350); axs[1].set_ylim(-50, 400)
axs[1].set_title("Outs Heatmap")

plt.tight_layout()
plt.show()
```

## Requirements

- Python 3.9+
- matplotlib >= 3.5
- numpy >= 1.21
- pandas >= 1.3

## Related

- [savant-extras](https://github.com/yasumorishima/savant-extras) — Statcast bat tracking data fetcher
- [pybaseball](https://github.com/jldbc/pybaseball) — Statcast data access

## License

MIT
