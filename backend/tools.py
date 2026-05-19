import pandas as pd


def get_schema(df: pd.DataFrame) -> dict:
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }



def get_summary(df: pd.DataFrame) -> dict:

    numeric_df = df.select_dtypes(include="number")

    return {
        "numeric_summary": numeric_df.describe().to_dict()
        if not numeric_df.empty else {}
    }



def analyze_question(df: pd.DataFrame, question: str) -> dict:

    q = question.lower()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    result = {}

    if "highest" in q or "top" in q:

        if numeric_cols and categorical_cols:

            category_col = categorical_cols[0]
            value_col = numeric_cols[0]

            grouped = (
                df.groupby(category_col)[value_col]
                .sum()
                .sort_values(ascending=False)
            )

            top_category = grouped.idxmax()
            top_value = grouped.max()

            result["analysis_type"] = "highest_sales"
            result["result"] = {
                "top_category": top_category,
                "sales": float(top_value)
            }

            return result

    if "lowest" in q or "underperform" in q:

        if numeric_cols and categorical_cols:

            category_col = categorical_cols[0]
            value_col = numeric_cols[0]

            grouped = (
                df.groupby(category_col)[value_col]
                .sum()
                .sort_values(ascending=True)
            )

            low_category = grouped.idxmin()
            low_value = grouped.min()

            result["analysis_type"] = "lowest_sales"
            result["result"] = {
                "lowest_category": low_category,
                "sales": float(low_value)
            }

            return result

    if "total" in q or "sum" in q:

        totals = {
            col: float(df[col].sum())
            for col in numeric_cols
        }

        result["analysis_type"] = "total_values"
        result["result"] = totals

        return result

    result["analysis_type"] = "general_summary"
    result["result"] = {
        "schema": get_schema(df),
        "summary": get_summary(df)
    }

    return result