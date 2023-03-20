"""Tasks running the results formatting (tables, figures)."""
import pandas as pd
import pytask
import plotly.io as pio
import os

from final_project_productivity.config import BLD, SRC
from final_project_productivity.final import plot_prod, plot_sector_data

countries = ["norway", "denmark", "sweden"]
country_names = ["Norway", "Denmark", "Sweden"]
sectors_for_comparison = ["Construction" ,"Tranport and storage", "Accommodation and food service activities", "Telecommunications", "Financial and insurance activities"]
productivity_measure = "level_TFP"

current_dir = os.path.dirname(os.path.abspath(__file__))
image = os.path.join(current_dir, "..", "layout", "map_for_layout.jpg")

for country in countries:

    @pytask.mark.task
    @pytask.mark.depends_on({
            f"{country}_estimates" : BLD / "python" / "estimates" / f"{country}_estimates.csv",
            f"{country}_plot_table" : BLD / "python" / "estimates" / "plot_tables" / f"{country}_plot_table.csv",
            f"{country}_sectors" : BLD / "python" / "estimates" / "sectors" / f"{country}_largest_sectors.csv",
            })
    @pytask.mark.produces({
        f"{country}_TFP" : BLD / "python" / "figures" / "LP_and_TFP" /f"{country}_TFP_plot.png",
        f"{country}_LP" : BLD / "python" / "figures" / "LP_and_TFP" / f"{country}_LP_plot.png",
    })
    def task_plots(depends_on, produces, country=country):
        plot_table = pd.read_csv(depends_on[f"{country}_plot_table"])
        sectors = pd.read_csv(depends_on[f"{country}_sectors"])

        figure_TFP = plot_prod(plot_table, 
                               sectors,
                               country,
                               prod_measure="TFP", 
                               amount_of_sectors=10, 
                               )
        figure_LP = plot_prod(plot_table, 
                              sectors,
                              country, 
                              prod_measure="LP", 
                              amount_of_sectors=10, 
                              )

        pio.write_image(figure_TFP, produces[f"{country}_TFP"])
        pio.write_image(figure_LP, produces[f"{country}_LP"])
        

for sector in sectors_for_comparison:
    @pytask.mark.task
    @pytask.mark.depends_on(BLD / "python" / "estimates" / "comparing_tables" / f"{sector}.csv")
    @pytask.mark.produces(BLD / "python" / "figures" / "sectors" /f"{sector}_compared.png")
    def task_plot_compare(depends_on, produces, sector=sector):
        """
        Generates a plot comparing the productivity of a given economic sector across multiple countries,
        on the data in the input file specified by the `depends_on` argument. The resulting plot is
        saved in the file specified by the `produces` argument.

        Args:
            depends_on (str): The path to the input file containing the sector-level productivity data
                for multiple countries.
            produces (str): The path where the resulting plot will be saved as an image file.
        """
        fig = plot_sector_data(depends_on, sector, country_names, layout=image, productivity=productivity_measure)
        pio.write_image(fig, produces)