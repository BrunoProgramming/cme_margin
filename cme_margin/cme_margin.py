import io
from pathlib import Path

import pandas as pd
import requests


def check_data_frame(df: pd.DataFrame) -> None:
    """Ensure required columns are present"""

    required_cols = {
        "Time",
        "Exchange",
        "Asset Class",
        "Product Name",
        "Product Code",
        "Start Period",
        "End Period",
        "Maintenance",
        "Currency",
        "Maint. Vol. Scan",
    }
    assert required_cols.issubset(df.columns)


def read(file: Path) -> pd.DataFrame:
    """Read margin file"""

    # read and check margin file
    margin = pd.read_csv(file, parse_dates=["Time"])
    check_data_frame(margin)

    return margin


def download(
    url: str = "https://www.cmegroup.com/CmeWS/mvc/Margins/OUTRIGHT.csv"
) -> pd.DataFrame:
    """Download margin"""

    # download and parse margin file from URL
    response = requests.get(url)
    file_object = io.StringIO(response.content.decode("utf-8"))
    margin = pd.read_csv(file_object)
    margin = margin.dropna(subset=["Maintenance"])
    margin.insert(loc=0, column="Time", value=pd.Timestamp.now(tz="UTC"))

    check_data_frame(margin)

    return margin


def merge(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Concatenate data frames and drop duplicates"""

    check_data_frame(df1)
    check_data_frame(df2)

    df = df1.append(df2, ignore_index=True)

    # drop duplicates
    df["id"] = (
        df["Exchange"]
        + df["Asset Class"]
        + df["Product Code"]
        + df["Start Period"]
        + df["End Period"]
        + df["Currency"]
    )
    df = df.groupby(["id"], sort=False).apply(
        lambda x: x[x["Maintenance"] != x["Maintenance"].shift(fill_value=0)]
    )
    df = df.drop(["id"], axis=1).reset_index(drop=True)

    return df


def write(df: pd.DataFrame, file: Path) -> None:
    """Write margin to file"""

    check_data_frame(df)
    df.to_csv(file, index=False, encoding="utf-8", date_format="%Y-%m-%dT%H:%M:%SZ")
