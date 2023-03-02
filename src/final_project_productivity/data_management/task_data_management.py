import pandas as pd
import pytask
from final_project_productivity.config import BLD, SRC
from final_project_productivity.data_management.clean_data import clean_and_merge


@pytask.mark.depends_on(
    {
        "capital": SRC / "data" / "norway" / "capital_norway.xlsx",
        "hours": SRC / "data" / "norway" / "hours_norway.xlsx",
        "value_added": SRC / "data" / "norway" / "value_added_norway.xlsx",
    },
)

@pytask.mark.produces(BLD / "python" / "data" / "norway_cleaned.csv")
@pytask.mark.try_first
def task_clean_data_python(depends_on, produces):
    df1 = pd.read_excel(depends_on["capital"])
    df2 = pd.read_excel(depends_on["hours"])
    df3 = pd.read_excel(depends_on["value_added"])

    data = clean_and_merge(df1, df2, df3)  
    
    data.to_csv(produces, index=False)
