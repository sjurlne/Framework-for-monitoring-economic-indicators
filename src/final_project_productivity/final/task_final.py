"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask
import plotly.io as pio

from final_project_productivity.config import BLD, SRC
from final_project_productivity.final import plot_prod

@pytask.mark.depends_on({
    "norway_estimates" : BLD / "python" / "estimates" / "norway_estimates.csv",
    "norway_plot_table" : BLD / "python" / "estimates" / "norway_plot_table.csv",
    "norway_sectors" : BLD / "python" / "estimates" / "norway_largest_sectors.csv",
    })
@pytask.mark.produces({
    "nor_TFP" : BLD / "python" / "figures" / "norway_TFP_plot.png",
    "nor_LP" : BLD / "python" / "figures" / "norway_LP_plot.png",
    })
def task_plots(depends_on, produces):
    plot_table = pd.read_csv(depends_on["norway_plot_table"])
    sectors = pd.read_csv(depends_on["norway_sectors"])

    figure_TFP = plot_prod(plot_table, sectors, prod_measure="TFP", amount_of_sectors=10)
    figure_LP = plot_prod(plot_table, sectors, prod_measure="LP", amount_of_sectors=10)

    pio.write_image(figure_TFP, produces["nor_TFP"])
    pio.write_image(figure_LP, produces["nor_LP"])