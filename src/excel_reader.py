import pandas as pd


def load_excel(file_path):
    """
    Reads the MOU Excel file and returns
    a cleaned DataFrame.
    """

    df = pd.read_excel(
        file_path,
        header=5
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()
    # Remove unnamed column 
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df