from pathlib import Path

from excel_reader import load_excel
from report_data import get_distributor_data
from template_render import render_template

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH =  BASE_DIR/"data"/"sample_MOU_data.xlsx"

df = load_excel(FILE_PATH)

party= get_distributor_data(df, "ABC Traders")



# print(party["distributor"])

# print(party["city"])

# print(party["annual"])

html = render_template(
    "scorecard.html",
    party
    )

output_path = Path(__file__).resolve().parent.parent / "output" / "output.html"

with open(output_path, "w", encoding="utf-8") as file:
    file.write(html)

print(f"HTML generated successfully: {output_path}")
# print(party["months"]["May"])