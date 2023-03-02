"""Tasks running the core analyses."""
import pandas as pd
import pytask
from final_project_productivity.analysis.estimation import productivity_table, changes
from final_project_productivity.config import BLD

@pytask.mark.depends_on(BLD / "python" / "data" / "norway_cleaned.csv")
@pytask.mark.produces(BLD / "python" / "estimates" / "norway_estimates.csv")
def task_estimate_productivity(depends_on, produces):
    df = pd.read_csv(depends_on)
    results = changes(df)
    results = productivity_table(results)
    results.to_csv(produces, index=False) 