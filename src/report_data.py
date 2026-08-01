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
def get_distributor_data(df, distributor_name):

    distributor = df[df["Party Name"] == distributor_name]

    if distributor.empty:
        return None

    row = distributor.iloc[0]

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
        "months": months
    

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