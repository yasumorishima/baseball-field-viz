import numpy as np


def draw_field(ax, foul_distance=330, outfield_distance=340):
    """Draw a baseball field on a matplotlib Axes (home plate at origin).

    Draws: foul lines, infield arc, outfield fence, base paths, bases,
    and pitcher's mound.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to draw on.
    foul_distance : int, optional
        Length of foul lines in feet. Default 330.
    outfield_distance : int, optional
        Distance to the outfield fence in feet. Default 340.

    Returns
    -------
    matplotlib.axes.Axes
        The same axes, with the field drawn.
    """
    # Foul lines (45 degrees: cos(45°) = sin(45°) ≈ 0.7071)
    ax.plot([0, -foul_distance * 0.7071], [0, foul_distance * 0.7071], "k-", lw=2)
    ax.plot([0, foul_distance * 0.7071], [0, foul_distance * 0.7071], "k-", lw=2)

    # Infield arc (~95 feet radius)
    theta = np.linspace(-np.pi / 4, np.pi / 4, 100)
    infield_dist = 95
    ax.plot(
        infield_dist * np.sin(theta),
        infield_dist * np.cos(theta),
        color="green",
        lw=2,
        alpha=0.7,
    )

    # Outfield fence
    ax.plot(
        outfield_distance * np.sin(theta),
        outfield_distance * np.cos(theta),
        color="saddlebrown",
        lw=3,
        alpha=0.7,
    )

    # Base paths (90-foot square diamond; diagonal = 90 * sqrt(2) / 2 ≈ 63.64 ft)
    bases_x = [0, 63.64, 0, -63.64, 0]
    bases_y = [0, 63.64, 127.28, 63.64, 0]
    ax.plot(bases_x, bases_y, "k-", lw=1.5)

    # Home plate
    ax.scatter([0], [0], color="white", edgecolors="black", s=150, marker="p", zorder=5)
    # 1st, 2nd, 3rd base
    ax.scatter(
        [63.64, 0, -63.64],
        [63.64, 127.28, 63.64],
        color="white",
        edgecolors="black",
        s=100,
        marker="s",
        zorder=5,
    )

    # Pitcher's mound (60.5 feet from home plate)
    ax.scatter([0], [60.5], color="brown", s=80, zorder=5)

    ax.set_aspect("equal")
    ax.set_facecolor("lightgreen")
    return ax
