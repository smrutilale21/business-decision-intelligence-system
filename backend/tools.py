from schema_detector import detect_business_schema


def determine_aggregation(question):

    question = question.lower()

    if any(
        keyword in question
        for keyword in [
            "average",
            "avg",
            "mean"
        ]
    ):
        return "mean"

    if any(
        keyword in question
        for keyword in [
            "count",
            "number of",
            "total orders"
        ]
    ):
        return "count"

    return "sum"


def determine_chart_type(
    question,
    datetime_cols,
    dimension_col
):

    question = question.lower()

    if any(
        keyword in question
        for keyword in [
            "trend",
            "over time",
            "monthly",
            "yearly"
        ]
    ) and datetime_cols:

        return "line"

    if any(
        keyword in question
        for keyword in [
            "distribution",
            "share",
            "percentage"
        ]
    ):
        return "pie"

    if dimension_col:
        return "bar"

    return "line"


def analyze_data(df, question):

    schema = detect_business_schema(
        df,
        question
    )

    metric_col = schema["metric_column"]

    dimension_col = schema["dimension_column"]

    datetime_cols = schema["datetime_columns"]

    aggregation = determine_aggregation(
        question
    )

    chart_type = determine_chart_type(
        question,
        datetime_cols,
        dimension_col
    )

    insights = {}

    if metric_col and dimension_col:

        if aggregation == "sum":

            grouped = (
                df.groupby(dimension_col)[metric_col]
                .sum()
                .sort_values(ascending=False)
            )

        elif aggregation == "mean":

            grouped = (
                df.groupby(dimension_col)[metric_col]
                .mean()
                .sort_values(ascending=False)
            )

        elif aggregation == "count":

            grouped = (
                df.groupby(dimension_col)[metric_col]
                .count()
                .sort_values(ascending=False)
            )

        insights["top_performers"] = (
            grouped.head(5).to_dict()
        )

        insights["bottom_performers"] = (
            grouped.tail(5).to_dict()
        )

        insights["total_metric"] = (
            float(df[metric_col].sum())
        )

        insights["average_metric"] = (
            float(df[metric_col].mean())
        )

    insights["schema"] = schema

    insights["chart_type"] = chart_type

    insights["aggregation"] = aggregation

    insights["metric_column"] = metric_col

    insights["dimension_column"] = dimension_col

    return insights