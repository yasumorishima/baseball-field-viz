from .field import draw_field
from .transform import transform_coords

_EVENT_COLORS = {
    "home_run": "red",
    "triple": "orange",
    "double": "blue",
    "single": "green",
}

_DEFAULT_COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]


def spraychart(ax, df, color_by="events", title=None):
    """Draw a spray chart on a baseball field.

    Filters rows with valid hc_x/hc_y, transforms coordinates, draws the
    field, then overlays a scatter plot colored by the specified column.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to draw on.
    df : pandas.DataFrame
        DataFrame with Statcast columns 'hc_x' and 'hc_y'.
    color_by : str, optional
        Column name to color points by. Use 'events' (default) for preset
        colors: home_run=red, triple=orange, double=blue, single=green.
        Any other column name applies categorical coloring.
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.axes.Axes
        The axes with the spray chart drawn.
    """
    df_valid = df[df["hc_x"].notna() & df["hc_y"].notna()].copy()
    df_t = transform_coords(df_valid)

    draw_field(ax)

    if color_by == "events" and "events" in df_t.columns:
        for event, color in _EVENT_COLORS.items():
            subset = df_t[df_t["events"] == event]
            if len(subset) > 0:
                ax.scatter(
                    subset["x"],
                    subset["y"],
                    c=color,
                    alpha=0.7,
                    s=50,
                    label=f"{event} ({len(subset)})",
                    zorder=4,
                )
        other = df_t[~df_t["events"].isin(_EVENT_COLORS)]
        if len(other) > 0:
            ax.scatter(
                other["x"],
                other["y"],
                c="gray",
                alpha=0.4,
                s=30,
                label=f"other ({len(other)})",
                zorder=3,
            )
    elif color_by in df_t.columns:
        categories = sorted(df_t[color_by].dropna().unique(), key=str)
        for i, cat in enumerate(categories):
            color = _DEFAULT_COLORS[i % len(_DEFAULT_COLORS)]
            subset = df_t[df_t[color_by] == cat]
            ax.scatter(
                subset["x"],
                subset["y"],
                c=color,
                alpha=0.7,
                s=50,
                label=str(cat),
                zorder=4,
            )
    else:
        ax.scatter(df_t["x"], df_t["y"], alpha=0.7, s=50, zorder=4)

    ax.set_xlim(-350, 350)
    ax.set_ylim(-50, 420)
    ax.set_xlabel("X (feet)")
    ax.set_ylabel("Y (feet)")
    if title:
        ax.set_title(title)
    ax.legend(loc="upper right")

    return ax
