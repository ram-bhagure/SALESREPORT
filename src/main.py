from pathlib import Path
from excel_reader import load_excel

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH =  BASE_DIR/"data"/"sample_MOU_data.xlsx"

df = load_excel(FILE_PATH)

print(df.head())

print("\n")

print(df.columns)