import pandas as pd
import pytask
from final_project_productivity.config import BLD
from final_project_productivity.data_management.clean_data import clean_and_merge_nor, clean_and_merge_den
pd.options.mode.chained_assignment = None

@pytask.mark.depends_on(
    {
        "capital_nor": BLD / "python" / "data" / "norway" / "capital_norway.xlsx",
        "hours_nor": BLD / "python" / "data" / "norway" / "hours_norway.xlsx",
        "value_added_nor": BLD / "python" / "data" / "norway" / "value_added_norway.xlsx",
        "capital_den": BLD / "python" / "data" / "denmark" / "capital_denmark.xlsx",
        "capital2_den": BLD / "python" / "data" / "denmark" / "capital2_denmark.xlsx",
        "hours_den": BLD / "python" / "data" / "denmark" / "hours_denmark.xlsx",
        "value_added_den": BLD / "python" / "data" / "denmark" / "value_added_denmark.xlsx",
    },
)
@pytask.mark.produces({
    "norway_cleaned" : BLD / "python" / "data" / "norway_cleaned.csv",
    "denmark_cleaned" : BLD / "python" / "data" / "denmark_cleaned.csv",
    })
def task_clean_data_python(depends_on, produces):
    """Collects data saved by web scraper, and clean/shape it in a desired format."""

    capital_nor = pd.read_excel(depends_on["capital_nor"])
    hours_nor = pd.read_excel(depends_on["hours_nor"])
    value_added_nor = pd.read_excel(depends_on["value_added_nor"])

    capital_den = pd.read_excel(depends_on["capital_den"])
    capital2_den = pd.read_excel(depends_on["capital2_den"])
    hours_den = pd.read_excel(depends_on["hours_den"])
    value_added_den = pd.read_excel(depends_on["value_added_den"])

    data = clean_and_merge_nor(capital_nor, hours_nor, value_added_nor)  
    data.to_csv(produces["norway_cleaned"], index=False)

    data = clean_and_merge_den(capital_den, hours_den, value_added_den, capital2_den)  
    data.to_csv(produces["denmark_cleaned"], index=False)

    