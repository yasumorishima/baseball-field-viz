import matplotlib.pyplot as plt
import pandas as pd
import pytest
from baseball_field_viz import draw_strike_zone, pitch_zone_chart


@pytest.fixture
def ax():
    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "plate_x": [-0.5, 0.0, 0.5, 1.5, -1.5, -0.3, 0.2, 0.8, -0.8, 0.1],
        "plate_z": [2.0, 2.5, 3.0, 1.0, 4.5, 2.2, 2.8, 3.2, 1.8, 2.6],
        "pitch_type": ["FF", "SL", "FF", "CU", "SL", "FF", "SL", "FF", "CU", "FF"],
        "sz_top": [3.5] * 10,
        "sz_bot": [1.5] * 10,
    })


def test_draw_strike_zone_returns_ax(ax):
    result = draw_strike_zone(ax)
    assert result is ax


def test_draw_strike_zone_adds_patch(ax):
    patches_before = len(ax.patches)
    draw_strike_zone(ax)
    assert len(ax.patches) > patches_before


def test_draw_strike_zone_custom_bounds(ax):
    draw_strike_zone(ax, sz_top=4.0, sz_bot=1.2)
    rect = ax.patches[-1]
    assert abs(rect.get_height() - (4.0 - 1.2)) < 1e-6


def test_pitch_zone_chart_returns_ax(ax, sample_df):
    result = pitch_zone_chart(ax, sample_df)
    assert result is ax


def test_pitch_zone_chart_draws_something(ax, sample_df):
    pitch_zone_chart(ax, sample_df)
    # kdeplot creates collections (filled contours) or lines
    assert len(ax.collections) > 0 or len(ax.lines) > 0


def test_pitch_zone_chart_uses_df_sz(ax, sample_df):
    pitch_zone_chart(ax, sample_df)
    rect = ax.patches[-1]
    assert abs(rect.get_height() - (3.5 - 1.5)) < 1e-6


def test_pitch_zone_chart_override_sz(ax, sample_df):
    pitch_zone_chart(ax, sample_df, sz_top=4.0, sz_bot=1.0)
    rect = ax.patches[-1]
    assert abs(rect.get_height() - (4.0 - 1.0)) < 1e-6


def test_pitch_zone_chart_title(ax, sample_df):
    pitch_zone_chart(ax, sample_df, title="Test Title")
    assert ax.get_title() == "Test Title"


def test_pitch_zone_chart_no_color_by_column(ax, sample_df):
    pitch_zone_chart(ax, sample_df, color_by="nonexistent_col")
    assert len(ax.collections) > 0 or len(ax.lines) > 0


def test_pitch_zone_chart_axis_limits(ax, sample_df):
    pitch_zone_chart(ax, sample_df)
    assert ax.get_xlim() == (-2.5, 2.5)
    assert ax.get_ylim() == (0, 5.5)


def test_pitch_zone_chart_filters_nan(ax):
    df = pd.DataFrame({
        "plate_x": [0.0, None, 0.5, -0.3, 0.2, 0.1, -0.1, 0.4, -0.4, 0.3],
        "plate_z": [2.5, 2.0, None, 2.8, 3.0, 2.2, 2.6, 2.9, 2.1, 2.7],
        "pitch_type": ["FF"] * 10,
    })
    pitch_zone_chart(ax, df)
    assert len(ax.collections) > 0 or len(ax.lines) > 0
