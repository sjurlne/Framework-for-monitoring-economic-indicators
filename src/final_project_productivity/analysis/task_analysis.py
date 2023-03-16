import pandas as pd
import pytask
from final_project_productivity.analysis.estimation import productivity_table, for_plotting, largest_sectors
from final_project_productivity.config import BLD

countries = ["norway", "denmark", "sweden"]

for country in countries:

    @pytask.mark.task
    @pytask.mark.depends_on(BLD / "python" / "data" / f"{country}_cleaned.csv")
    @pytask.mark.produces({
            f"{country}_estimates" : BLD / "python" / "estimates" / f"{country}_estimates.csv",
            f"{country}_plot_table" : BLD / "python" / "estimates" / "plot_tables" / f"{country}_plot_table.csv",
            f"{country}_sectors" : BLD / "python" / "estimates" / "sectors" / f"{country}_largest_sectors.csv",
            })
    def task_estimate_prod(depends_on, produces, country=country):
        """Creates estimates of productivity, and stores it in suitable tables for plotting."""
        results = pd.read_csv(depends_on)
        top_sectors = largest_sectors(results)
        results = productivity_table(results, ref_year=2000)
        plotting_data = for_plotting(results)
        top_sectors.to_csv(produces[f"{country}_sectors"], index=False)
        results.to_csv(produces[f"{country}_estimates"], index=False)
        plotting_data.to_csv(produces[f"{country}_plot_table"], index=False)