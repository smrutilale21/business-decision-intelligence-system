import os
import uuid

import matplotlib.pyplot as plt
from schema_detector import detect_business_schema
from tools import determine_aggregation, determine_chart_type


def generate_chart(df, question):

    schema = detect_business_schema(df, question)

    metric_col = schema["metric_column"]

    dimension_col = schema["dimension_column"]

    datetime_cols = schema["datetime_columns"]

    aggregation = determine_aggregation(question)

    chart_type = determine_chart_type(question, datetime_cols, dimension_col)

    # Prevent invalid pie charts for negative values
    if chart_type == "pie" and (df[metric_col] < 0).any():
        chart_type = "bar"

    if not metric_col:
        return None

    os.makedirs("charts", exist_ok=True)

    chart_id = str(uuid.uuid4())

    chart_path = f"../charts/{chart_id}.png"

    plt.figure(figsize=(10, 6))

    # -----------------------------------
    # LINE CHART
    # -----------------------------------

    if chart_type == "line" and datetime_cols:

        date_col = datetime_cols[0]

        grouped = df.groupby(date_col)[metric_col]

        if aggregation == "sum":
            grouped = grouped.sum()

        elif aggregation == "mean":
            grouped = grouped.mean()

        elif aggregation == "count":
            grouped = grouped.count()

        grouped.plot(kind="line")

        plt.title(f"{metric_col} Trend")

    # -----------------------------------
    # PIE CHART
    # -----------------------------------

    elif chart_type == "pie" and dimension_col:

        grouped = (
            df.groupby(dimension_col)[metric_col]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )

        grouped.plot(kind="pie")

        plt.ylabel("")

        plt.title(f"{metric_col} Distribution")

    # -----------------------------------
    # BAR CHART
    # -----------------------------------

    elif dimension_col:

        grouped = df.groupby(dimension_col)[metric_col]

        if aggregation == "sum":
            grouped = grouped.sum()

        elif aggregation == "mean":
            grouped = grouped.mean()

        elif aggregation == "count":
            grouped = grouped.count()

        grouped = grouped.sort_values(ascending=False).head(10)

        grouped.plot(kind="bar")

        plt.title(f"{metric_col} by {dimension_col}")

    else:
        return None

    plt.ylabel(metric_col)

    plt.tight_layout()

    plt.savefig(chart_path)

    plt.close()

    return chart_path
