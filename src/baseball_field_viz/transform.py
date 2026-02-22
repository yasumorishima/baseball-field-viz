def transform_coords(df):
    """Convert Statcast hc_x/hc_y to feet coordinates (home plate at origin).

    Statcast coordinate system:
    - Home plate is at approximately (125.42, 198.27)
    - Y-axis is screen coordinates (increases downward)

    After transformation:
    - Home plate is at (0, 0)
    - Y-axis points toward the outfield (increases upward)
    - Units are approximately feet

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with 'hc_x' and 'hc_y' columns (Statcast coordinates).

    Returns
    -------
    pandas.DataFrame
        Copy of df with added 'x' and 'y' columns in feet.
    """
    df = df.copy()
    df["x"] = 2.5 * (df["hc_x"] - 125.42)
    df["y"] = 2.5 * (198.27 - df["hc_y"])
    return df
