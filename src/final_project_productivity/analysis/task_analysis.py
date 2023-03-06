import pandas as pd
import pytask
from final_project_productivity.analysis.estimation import productivity_table, for_plotting, largest_sectors
from final_project_productivity.config import BLD

@pytask.mark.depends_on(BLD / "python" / "data" / "norway_cleaned.csv")
@pytask.mark.produces({
    "norway_estimates" : BLD / "python" / "estimates" / "norway_estimates.csv",
    "norway_plot_table" : BLD / "python" / "estimates" / "norway_plot_table.csv",
    "norway_sectors" : BLD / "python" / "estimates" / "norway_largest_sectors.csv",
    })
def task_estimate_prod(depends_on, produces):
    """Creates estimates of productivity, and stores it in suitable tables for plotting."""

    results = pd.read_csv(depends_on)
    top_sectors = largest_sectors(results)
    results = productivity_table(results)
    plotting_data = for_plotting(results)

    top_sectors.to_csv(produces["norway_sectors"], index=False)
    results.to_csv(produces["norway_estimates"], index=False)
    plotting_data.to_csv(produces["norway_plot_table"], index=False)