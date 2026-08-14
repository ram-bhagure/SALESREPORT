from pathlib import Path
import re

from excel_reader import load_excel
from report_data import (get_distributor_data, get_completed_months, calculate_performance)
from template_render import render_template

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH =  BASE_DIR/"data"/"MOU 01.04.26 TO 24.06.26.xlsx"

df = load_excel(FILE_PATH)
df["Party Name"] = df["Party Name"].astype(str).str.strip()

# print(
#     df[df["Party Name"].str.contains(
#         "JAYBHARAT TRADERS",
#         case=False,
#         na=False
#     )]["Party Name"].tolist()
# )

REPORT_MONTH = "June"

def safe_filename(name):
    name = str(name).strip()
    # Replace characters that are problematic in filenames
    name = re.sub(r'[<>:"/\\|?*&]', '_',name)

    #Replace multiple spaces with a single space
    name = re.sub(r'\s+', ' ', name)

    return name

distributors = (
    df["Party Name"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

completed_months = get_completed_months(REPORT_MONTH)

for distributor_name in distributors:

    party = get_distributor_data(
        df,
        distributor_name,
        REPORT_MONTH
    )

    if party is None:
        print(f"Skipped: {distributor_name}")
        continue

    performance = calculate_performance(
        party["months"],
        completed_months
    )

    html = render_template(
        "scorecard.html",
        party
    )

    # Executive folder
    executive_name = safe_filename(party["executive"])

    executive_folder = (
        BASE_DIR
        / "output"
        / executive_name
    )

    executive_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # Distributor filename
    safe_name = safe_filename(distributor_name)

    output_path = (
        executive_folder
        / f"{safe_name}.html"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(html)

    print(
        f"Generated: {executive_name} / {safe_name}.html"
    )

