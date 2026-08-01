from pathlib import Path

from excel_reader import load_excel
from report_data import get_distributor_data

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH =  BASE_DIR/"data"/"sample_MOU_data.xlsx"

df = load_excel(FILE_PATH)

party= get_distributor_data(df, "ABC Traders")

# print(party["distributor"])

# print(party["city"])

# print(party["annual"])

print(party["months"])
# print(party["months"]["May"])