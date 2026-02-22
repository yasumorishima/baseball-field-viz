import matplotlib.pyplot as plt
import pandas as pd
import pytest

from baseball_field_viz import spraychart


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "hc_x": [125.42, 150.0, 100.0, 125.42 + 50, 80.0],
            "hc_y": [198.27, 170.0, 180.0, 198.27 - 100, 160.0],
            "events": ["home_run", "single", "double", "out", "triple"],
        }
    )


def test_spraychart_returns_ax(sample_df):
    fig, ax = plt.subplots()
    result = spraychart(ax, sample_df)
    assert result is ax
    plt.close(fig)


def test_spraychart_filters_nan():
    df = pd.DataFrame(
        {
            "hc_x": [125.42, None],
            "hc_y": [198.27, None],
            "events": ["home_run", "single"],
        }
    )
    fig, ax = plt.subplots()
    spraychart(ax, df)
    plt.close(fig)


def test_spraychart_with_title(sample_df):
    fig, ax = plt.subplots()
    spraychart(ax, sample_df, title="Test Chart")
    assert ax.get_title() == "Test Chart"
    plt.close(fig)


def test_spraychart_custom_color_by(sample_df):
    fig, ax = plt.subplots()
    spraychart(ax, sample_df, color_by="events")
    plt.close(fig)


def test_spraychart_empty_df():
    df = pd.DataFrame({"hc_x": [], "hc_y": [], "events": []})
    fig, ax = plt.subplots()
    spraychart(ax, df)
    plt.close(fig)


def test_spraychart_axis_limits(sample_df):
    fig, ax = plt.subplots()
    spraychart(ax, sample_df)
    assert ax.get_xlim() == (-350, 350)
    assert ax.get_ylim() == (-50, 420)
    plt.close(fig)


def test_spraychart_no_events_column():
    df = pd.DataFrame(
        {
            "hc_x": [125.42, 150.0],
            "hc_y": [198.27, 170.0],
            "pitch_type": ["FF", "SL"],
        }
    )
    fig, ax = plt.subplots()
    # color_by='events' but no events column → plain scatter
    spraychart(ax, df, color_by="events")
    plt.close(fig)
