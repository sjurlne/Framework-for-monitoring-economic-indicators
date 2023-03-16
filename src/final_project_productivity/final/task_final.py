"""Tasks running the results formatting (tables, figures)."""
import pandas as pd
import pytask
import plotly.io as pio

from final_project_productivity.config import BLD
from final_project_productivity.final import plot_prod, plot_sector_data

countries = ["norway", "denmark", "sweden"]

for country in countries:

    @pytask.mark.task
    @pytask.mark.depends_on({
            f"{country}_estimates" : BLD / "python" / "estimates" / f"{country}_estimates.csv",
            f"{country}_plot_table" : BLD / "python" / "estimates" / "plot_tables" / f"{country}_plot_table.csv",
            f"{country}_sectors" : BLD / "python" / "estimates" / "sectors" / f"{country}_largest_sectors.csv",
            })
    @pytask.mark.produces({
        f"{country}_TFP" : BLD / "python" / "figures" / f"{country}_TFP_plot.png",
        f"{country}_LP" : BLD / "python" / "figures" / f"{country}_LP_plot.png",
    })
    def task_plots(depends_on, produces, country=country):
        plot_table = pd.read_csv(depends_on[f"{country}_plot_table"])
        sectors = pd.read_csv(depends_on[f"{country}_sectors"])

        figure_TFP = plot_prod(plot_table, sectors, 
                               prod_measure="TFP", 
                               amount_of_sectors=10)
        figure_LP = plot_prod(plot_table, sectors, 
                              prod_measure="LP", 
                              amount_of_sectors=10)

        pio.write_image(figure_TFP, produces[f"{country}_TFP"])
        pio.write_image(figure_LP, produces[f"{country}_LP"])

    

@pytask.mark.depends_on(BLD / "python" / "reports" / "common.csv")
@pytask.mark.produces(BLD / "python" / "figures" / "compared.png")
def task_plot_compare(depends_on, produces):
    fig = plot_sector_data(depends_on, "level_LP_Accommodation and food service activities")

    pio.write_image(fig, produces)


