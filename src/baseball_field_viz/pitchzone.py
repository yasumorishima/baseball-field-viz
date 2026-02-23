import matplotlib.patches as mpatches

# Home plate width: 17 inches = 17/12 feet
_PLATE_HALF_WIDTH = 17 / 12 / 2  # ~0.7083 ft


def draw_strike_zone(ax, sz_top=3.5, sz_bot=1.5, color="black", lw=2):
    """Draw a strike zone rectangle on a matplotlib Axes.

    The coordinate system is plate_x (horizontal, feet, catcher's perspective)
    and plate_z (vertical, feet from ground).

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to draw on.
    sz_top : float
        Top of strike zone in feet. Default 3.5 (average MLB value).
    sz_bot : float
        Bottom of strike zone in feet. Default 1.5 (average MLB value).
    color : str
        Rectangle edge color. Default "black".
    lw : float
        Line width. Default 2.
    """
    width = 2 * _PLATE_HALF_WIDTH
    height = sz_top - sz_bot
    rect = mpatches.Rectangle(
        (-_PLATE_HALF_WIDTH, sz_bot),
        width,
        height,
        linewidth=lw,
        edgecolor=color,
        facecolor="none",
        zorder=5,
    )
    ax.add_patch(rect)
    return ax


def pitch_zone_chart(ax, df, sz_top=None, sz_bot=None, title=None):
    """Plot pitch location density with strike zone overlay.

    Pass a pre-filtered DataFrame for one pitch type (or any subset).
    For multi-type comparison, call this in a loop — one subplot per type.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes to draw on.
    df : pandas.DataFrame
        Must contain 'plate_x' and 'plate_z' columns (Statcast standard).
        If sz_top/sz_bot are None, uses mean of 'sz_top'/'sz_bot' columns
        if present, otherwise defaults to 3.5/1.5.
    sz_top : float or None
        Override strike zone top. If None, inferred from df.
    sz_bot : float or None
        Override strike zone bottom. If None, inferred from df.
    title : str or None
        Axes title.

    Example
    -------
    >>> pitch_types = df['pitch_type'].value_counts().index
    >>> fig, axs = plt.subplots(1, len(pitch_types), figsize=(5*len(pitch_types), 5))
    >>> for ax, pt in zip(axs, pitch_types):
    ...     pitch_zone_chart(ax, df[df['pitch_type'] == pt], title=pt)
    """
    import seaborn as sns

    df = df.dropna(subset=["plate_x", "plate_z"])

    if sz_top is None:
        sz_top = df["sz_top"].mean() if "sz_top" in df.columns and df["sz_top"].notna().any() else 3.5
    if sz_bot is None:
        sz_bot = df["sz_bot"].mean() if "sz_bot" in df.columns and df["sz_bot"].notna().any() else 1.5

    sns.kdeplot(
        data=df, x="plate_x", y="plate_z", ax=ax,
        fill=True, alpha=0.6, levels=6,
        clip=((-2.0, 2.0), (0.3, 5.2)),
        thresh=0.05,
    )

    draw_strike_zone(ax, sz_top=sz_top, sz_bot=sz_bot)

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(0, 5.5)
    ax.set_aspect("equal")
    ax.set_xlabel("plate_x (ft)")
    ax.set_ylabel("plate_z (ft)")
    if title:
        ax.set_title(title)

    return ax
