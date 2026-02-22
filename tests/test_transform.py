import pandas as pd
import pytest

from baseball_field_viz import transform_coords


def test_home_plate_maps_to_origin():
    df = pd.DataFrame({"hc_x": [125.42], "hc_y": [198.27]})
    result = transform_coords(df)
    assert abs(result["x"].iloc[0]) < 0.01
    assert abs(result["y"].iloc[0]) < 0.01


def test_x_transformation():
    # hc_x = 125.42 + 40 → x = 2.5 * 40 = 100
    df = pd.DataFrame({"hc_x": [125.42 + 40], "hc_y": [198.27]})
    result = transform_coords(df)
    assert abs(result["x"].iloc[0] - 100.0) < 0.01


def test_y_transformation():
    # hc_y = 198.27 - 40 → y = 2.5 * 40 = 100
    df = pd.DataFrame({"hc_x": [125.42], "hc_y": [198.27 - 40]})
    result = transform_coords(df)
    assert abs(result["y"].iloc[0] - 100.0) < 0.01


def test_original_df_not_modified():
    df = pd.DataFrame({"hc_x": [125.42], "hc_y": [198.27]})
    original_hc_x = df["hc_x"].iloc[0]
    transform_coords(df)
    assert df["hc_x"].iloc[0] == original_hc_x


def test_preserves_other_columns():
    df = pd.DataFrame({"hc_x": [125.42], "hc_y": [198.27], "events": ["home_run"]})
    result = transform_coords(df)
    assert "events" in result.columns
    assert result["events"].iloc[0] == "home_run"


def test_multiple_rows():
    df = pd.DataFrame(
        {
            "hc_x": [125.42, 125.42 + 20],
            "hc_y": [198.27, 198.27 - 20],
        }
    )
    result = transform_coords(df)
    assert len(result) == 2
    assert abs(result["x"].iloc[0]) < 0.01
    assert abs(result["x"].iloc[1] - 50.0) < 0.01
