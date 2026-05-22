import pandas as pd


DERIVED_METRICS = {

    "profit": {
        "required_keywords": {
            "revenue": [
                "revenue",
                "sales",
                "income"
            ],
            "cost": [
                "cost",
                "expense"
            ]
        }
    },

    "margin": {
        "required_keywords": {
            "revenue": [
                "revenue",
                "sales",
                "income"
            ],
            "cost": [
                "cost",
                "expense"
            ]
        }
    }
}


def find_matching_column(columns, keywords):

    for col in columns:

        for keyword in keywords:

            if keyword in col.lower():
                return col

    return None


def detect_business_schema(df, question):

    question = question.lower()

    numeric_cols = (
        df.select_dtypes(include="number")
        .columns
        .tolist()
    )

    categorical_cols = (
        df.select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    datetime_cols = []

    for col in df.columns:

        try:

            parsed = df[col].astype(str)

            if parsed.str.contains(
                r"\d{4}-\d{2}-\d{2}"
            ).any():

                datetime_cols.append(col)

        except:
            pass

    metric_col = None

    dimension_col = None

    derived_metric = None

    # -----------------------------------
    # QUESTION-AWARE METRIC SELECTION
    # -----------------------------------

    for col in numeric_cols:

        if col.lower() in question:
            metric_col = col
            break

    # -----------------------------------
    # QUESTION-AWARE DIMENSION SELECTION
    # -----------------------------------

    for col in categorical_cols:

        if col.lower() in question:
            dimension_col = col
            break

    # -----------------------------------
    # DERIVED METRIC CALCULATION
    # -----------------------------------

    for metric_name, config in DERIVED_METRICS.items():

        if metric_name in question:

            revenue_col = find_matching_column(
                numeric_cols,
                config["required_keywords"]["revenue"]
            )

            cost_col = find_matching_column(
                numeric_cols,
                config["required_keywords"]["cost"]
            )

            if revenue_col and cost_col:

                if metric_name == "profit":

                    df["profit"] = (
                        df[revenue_col] - df[cost_col]
                    )

                    metric_col = "profit"

                    derived_metric = "profit"

                elif metric_name == "margin":

                    df["margin"] = (
                        (
                            df[revenue_col] - df[cost_col]
                        ) / df[revenue_col]
                    )

                    metric_col = "margin"

                    derived_metric = "margin"

                break

    # -----------------------------------
    # FALLBACK METRIC SELECTION
    # -----------------------------------

    if not metric_col and numeric_cols:

        metric_priority = [
            "sales",
            "revenue",
            "profit",
            "amount",
            "quantity",
            "orders"
        ]

        for keyword in metric_priority:

            for col in numeric_cols:

                if keyword in col.lower():

                    metric_col = col

                    break

            if metric_col:
                break

    if not metric_col and numeric_cols:
        metric_col = numeric_cols[0]

    # -----------------------------------
    # FALLBACK DIMENSION SELECTION
    # -----------------------------------

    if not dimension_col and categorical_cols:

        dimension_priority = [
            "region",
            "product",
            "category",
            "segment",
            "department",
            "city"
        ]

        for keyword in dimension_priority:

            for col in categorical_cols:

                if keyword in col.lower():

                    dimension_col = col

                    break

            if dimension_col:
                break

    if not dimension_col and categorical_cols:
        dimension_col = categorical_cols[0]

    return {

        "metric_column": metric_col,

        "dimension_column": dimension_col,

        "datetime_columns": datetime_cols,

        "numeric_columns": numeric_cols,

        "categorical_columns": categorical_cols,

        "derived_metric": derived_metric
    }