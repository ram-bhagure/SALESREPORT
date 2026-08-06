MONTH_MAPPING = [
    ("Apr", "April"),
    ("May", "May"),
    ("June", "June"),
    ("July", "July"),
    ("Aug", "August"),
    ("Sep", "September"),
    ("Oct", "October"),
    ("Nov", "November"),
    ("Dec", "December"),
    ("Jan", "January"),
    ("Feb", "February"),
    ("Mar", "March"),
]

QUARTER_MAPPING = [
    ("1st QT", "Q1"),
    ("2nd QT", "Q2"),
    ("3rd QT", "Q3"),
    ("4th QT", "Q4"),
]

QUARTER_MONTH_MAPPING = {
    "Q1": ["April", "May", "June"],
    "Q2": ["July", "August", "September"],
    "Q3": ["October", "November", "December"],
    "Q4": ["January", "February", "March"]
}

def build_months(row):
    months = {}

    for excel_name, display_name in MONTH_MAPPING:

        target = row[f"{excel_name} Target"]
        sales = row[f"{excel_name} Value"]
        diff = row[f"{excel_name} Diff"]

        achievement = 0

        if target > 0:
            achievement = round((sales / target) * 100, 2)

        months[display_name] = {
            "target": target,
            "sales": sales,
            "diff": diff,
            "achievement": achievement
        }
    return months


def build_quarters(row):
    quarters = {}
    for excel_name, display_name in QUARTER_MAPPING:
        target = row[f"{excel_name} Target"]
        sales = row[f"{excel_name} Value"]            
        diff = row[f"{excel_name} Diff"]
        achievement = 0
    
        if target > 0:
            achievement = round((sales / target) * 100, 2)
    
        quarters[display_name] = {
            "target": target,
            "sales": sales,
            "diff": diff,
            "achievement": achievement
        }
    return quarters


def build_quarter_sections(months, quarters):

    quarter_sections = []

    for quarter_name, month_names in QUARTER_MONTH_MAPPING.items():

        section = {
            "name": quarter_name,
            "months": [],
            "summary": quarters[quarter_name]
        }

        for month in month_names:
            month_data = months[month].copy()
            month_data["name"] = month

            section["months"].append(month_data)

        quarter_sections.append(section)

    return quarter_sections

def get_distributor_data(df, distributor_name):

    distributor = df[df["Party Name"] == distributor_name]

    if distributor.empty:
        return None

    row = distributor.iloc[0]
    months = build_months(row)
    quarters = build_quarters(row)
    quarter_sections = build_quarter_sections(months, quarters)
    

    report_data = {

        "distributor": row["Party Name"],

        "city": row["City"],

        "executive": row["Executive"],

        "mobile": row["Mobile1"],

        "annual": {

            "target": row["Year Target"],

            "sales": row["Year Value"],

            "achievement": row["Total %"]

        },
        "months": months,
        "quarters":quarters,
        "quarter_sections": quarter_sections
    

        # "months":{
        #     "April":{
        #         "target":row["Apr Target"],
        #         "sales":row["Apr Value"],
        #         "diff":row["Apr Diff"],
        #         "achivement": round(
        #             (row["Apr Value"]/row["Apr Target"])*100,2
        #         )
        #     },
        #     "May":{
        #         "target":row["May Target"],
        #         "sales":row["May Value"],
        #         "diff":row["May Diff"],
        #         "achivement": round(
        #         (row["May Value"]/row["May Target"])*100,2
        #         )
        #     }
        # }

    }
    

    return report_data