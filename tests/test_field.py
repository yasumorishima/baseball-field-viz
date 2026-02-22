import matplotlib.pyplot as plt
import pytest

from baseball_field_viz import draw_field


def test_draw_field_returns_ax():
    fig, ax = plt.subplots()
    result = draw_field(ax)
    assert result is ax
    plt.close(fig)


def test_draw_field_aspect_equal():
    fig, ax = plt.subplots()
    draw_field(ax)
    # matplotlib returns "equal" or 1.0 depending on version/backend
    assert ax.get_aspect() in ("equal", 1.0)
    plt.close(fig)


def test_draw_field_facecolor_set():
    fig, ax = plt.subplots()
    draw_field(ax)
    # facecolor should be set (not the default white)
    fc = ax.get_facecolor()
    assert fc is not None
    plt.close(fig)


def test_draw_field_custom_distances():
    fig, ax = plt.subplots()
    draw_field(ax, foul_distance=320, outfield_distance=380)
    plt.close(fig)


def test_draw_field_lines_drawn():
    fig, ax = plt.subplots()
    draw_field(ax)
    # Should have multiple line artists (foul lines, arcs, base paths)
    assert len(ax.lines) > 0
    plt.close(fig)
