import pandas as pd
from datetime import datetime


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

MONTH_ORDER = [
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March"
]


def get_completed_months(report_month):

    report_month_index = MONTH_ORDER.index(report_month)

    completed_months = MONTH_ORDER[:report_month_index + 1]

    return completed_months


def calculate_performance(months, completed_months):

    total_achievement = 0

    month_count = 0

    for month in completed_months:

        if months[month]["target"] > 0:

            total_achievement += months[month]["achievement"]

            month_count += 1

    if month_count == 0:

        return {
            "performance": 0,
            "months_considered": 0
        }

    performance = round(total_achievement / month_count, 2)

    return {
        "performance": performance,
        "months_considered": month_count
    }

def calculate_average_monthly_sales(months, completed_months):

    total_sales = 0

    month_count = 0

    for month in completed_months:

        if months[month]["target"] > 0:

            total_sales += months[month]["sales"]

            month_count += 1

    if month_count == 0:

        return {
            "average_sales": 0,
            "months_considered": 0
        }

    average_sales = round(total_sales / month_count, 2)

    return {
        "average_sales": average_sales,
        "months_considered": month_count
    }


def get_highest_month(months, completed_months):

    highest_month = None

    for month in completed_months:

        if months[month]["target"] == 0:
            continue

        if highest_month is None:

            highest_month = {
                "month": month,
                "achievement": months[month]["achievement"],
                "sales": months[month]["sales"],
                "target": months[month]["target"]
            }

        elif months[month]["achievement"] > highest_month["achievement"]:

            highest_month = {
                "month": month,
                "achievement": months[month]["achievement"],
                "sales": months[month]["sales"],
                "target": months[month]["target"]
            }

    return highest_month


def get_lowest_month(months, completed_months):

    lowest_month = None

    for month in completed_months:

        if months[month]["target"] == 0:
            continue

        if lowest_month is None:

            lowest_month = {
                "month": month,
                "achievement": months[month]["achievement"],
                "sales": months[month]["sales"],
                "target": months[month]["target"]
            }

        elif months[month]["achievement"] < lowest_month["achievement"]:

            lowest_month = {
                "month": month,
                "achievement": months[month]["achievement"],
                "sales": months[month]["sales"],
                "target": months[month]["target"]
            }

    return lowest_month

def calculate_target_status(months, completed_months):

    total_target = 0
    total_sales = 0

    for month in completed_months:

        if months[month]["target"] == 0:
            continue

        total_target += months[month]["target"]
        total_sales += months[month]["sales"]

    difference = total_sales - total_target

    if difference > 0:
        status = "Ahead"

    elif difference < 0:
        status = "Behind"

    else:
        status = "On Target"

    return {
        "status": status,
        "amount": abs(difference),
        "target": total_target,
        "sales": total_sales
    }



def build_summary(months, report_month):

    completed_months = get_completed_months(report_month)

    performance = calculate_performance(
        months,
        completed_months
    )
    average_sales = calculate_average_monthly_sales(
        months,
        completed_months
    )
    highest_month = get_highest_month(
        months,
        completed_months
    )
    lowest_month = get_lowest_month(
        months,
        completed_months
    )
    target_status = calculate_target_status(
        months,
        completed_months
    )

    summary = {

        "performance": performance["performance"],

        "months_considered": performance["months_considered"],

        "average_monthly_sales": average_sales["average_sales"],

        "highest_month": highest_month,

        "lowest_month": lowest_month,

        "target_status": target_status

    }

    return summary


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

        if pd.isna(target):
            target = 0

        if pd.isna(sales):
            sales = 0

        if pd.isna(diff):
            diff = 0

        achievement = 0

        if target > 0:
            achievement = round((sales / target) * 100, 1)

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

        if pd.isna(target):
            target = 0

        if pd.isna(sales):
            sales = 0

        if pd.isna(diff):
            diff = 0
        achievement = 0
    
        if target > 0:
            achievement = round((sales / target) * 100, 1)
    
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

def safe_number(value):

    if pd.isna(value):
        return 0

    return value

def get_distributor_data(df, distributor_name,report_month):
    distributor_name = distributor_name.strip()

    distributor = df[df["Party Name"].astype(str).str.strip() == distributor_name]

    if distributor.empty:
        return None

    row = distributor.iloc[0]
    months = build_months(row)
    quarters = build_quarters(row)
    quarter_sections = build_quarter_sections(months, quarters)
    summary = build_summary(
        months,
        report_month
    )

    report_data = {

        "distributor": row["Party Name"],

        "city": row["City"],

        "executive": row["Executive"],

        "mobile": row["Mobile1"],

        "report_month":report_month,

        "generated_on": datetime.now().strftime("%d-%b-%Y"),

        "annual": {

            "target": safe_number(row["Year Target"]),

            "sales": safe_number(row["Year Value"]),

            "achievement": safe_number(row["Total %"])

        },
        "summary": summary,
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