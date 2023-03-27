from final_project_productivity.compare import combine_sectors
from final_project_productivity.config import BLD
import pytask

country_names = ["Norway", "Denmark", "Sweden"]
sectors_for_comparison = ["Construction" ,"Tranport and storage", "Accommodation and food service activities", "Telecommunications", "Financial and insurance activities"]
productivity_measure = "level_TFP"

for sector in sectors_for_comparison:
        @pytask.mark.task
        @pytask.mark.depends_on({
                "norway_sectors" : BLD / "python" / "estimates" / "plot_tables" / "norway_plot_table.csv",
                "denmark_sectors" : BLD / "python" / "estimates" / "plot_tables" / "denmark_plot_table.csv",
                "sweden_sectors" : BLD / "python" / "estimates" / "plot_tables" / "sweden_plot_table.csv",
                })
        @pytask.mark.produces(BLD / "python" / "estimates" / "comparing_tables" / f"{sector}.csv")
        def task_find_common_sectors(depends_on, produces, sector=sector):
                """
                Finds common sectors between multiple countries, combines them into a single table, and stores it as a CSV file.

                Parameters:
                        depends_on (dict): A dictionary of input file paths for the different countries.
                        produces (str): Path to the output CSV file.
                        sector (str, optional): Name of the sector being analyzed.
                """
                sectors = combine_sectors(depends_on["norway_sectors"], depends_on["denmark_sectors"], depends_on["sweden_sectors"], sector, country_names, productivity=productivity_measure)
                sectors.to_csv(produces)
    
