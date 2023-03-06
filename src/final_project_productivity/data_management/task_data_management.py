import pandas as pd
import pytask
from final_project_productivity.config import BLD
from final_project_productivity.data_management.clean_data import clean_and_merge_nor
pd.options.mode.chained_assignment = None


@pytask.mark.depends_on(
    {
        "capital_nor": BLD / "python" / "data" / "norway" / "capital_norway.xlsx",
        "hours_nor": BLD / "python" / "data" / "norway" / "hours_norway.xlsx",
        "value_added_nor": BLD / "python" / "data" / "norway" / "value_added_norway.xlsx",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "norway_cleaned.csv")
def task_clean_data_python(depends_on, produces):
    """Collects data saved by web scraper, and clean/shape it in a desired format."""

    capital_nor = pd.read_excel(depends_on["capital_nor"])
    hours_nor = pd.read_excel(depends_on["hours_nor"])
    value_added_nor = pd.read_excel(depends_on["value_added_nor"])

    data = clean_and_merge_nor(capital_nor, hours_nor, value_added_nor)  
    data.to_csv(produces, index=False)
