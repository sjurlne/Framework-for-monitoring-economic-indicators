from final_project_productivity.utilities import read_yaml
from final_project_productivity.config import BLD
import pandas as pd
import pytask
import os
from final_project_productivity.data_management.clean_data import clean_and_merge_nor, clean_and_merge_den, clean_and_merge_swe, replace_sector_names
pd.options.mode.chained_assignment = None

current_file_dir = os.path.dirname(os.path.abspath(__file__))
specs_dir = os.path.join(current_file_dir, '..')
specs_dir = os.path.abspath(specs_dir)

specs = read_yaml(f"{specs_dir}\management_specs.yml")
col_names_swe = specs['col_names_swe']
den_nor = specs["den_nor"]
swe_nor = specs["swe_nor"]

@pytask.mark.depends_on(
    {
        "capital_nor": BLD / "python" / "data" / "norway" / "capital_norway.xlsx",
        "hours_nor": BLD / "python" / "data" / "norway" / "hours_norway.xlsx",
        "value_added_nor": BLD / "python" / "data" / "norway" / "value_added_norway.xlsx",
        "capital_den": BLD / "python" / "data" / "denmark" / "capital_denmark.xlsx",
        "capital2_den": BLD / "python" / "data" / "denmark" / "capital2_denmark.xlsx",
        "hours_den": BLD / "python" / "data" / "denmark" / "hours_denmark.xlsx",
        "value_added_den": BLD / "python" / "data" / "denmark" / "value_added_denmark.xlsx",
        "capital_swe": BLD / "python" / "data" / "sweden" / "capital_sweden.xlsx",
        "capital2_swe": BLD / "python" / "data" / "sweden" / "capital2_sweden.xlsx",
        "hours_swe": BLD / "python" / "data" / "sweden" / "hours_sweden.xlsx",
        "value_added_swe": BLD / "python" / "data" / "sweden" / "value_added_sweden.xlsx",
    },
    )
@pytask.mark.produces({
    "norway_cleaned" : BLD / "python" / "data" / "norway_cleaned.csv",
    "denmark_cleaned" : BLD / "python" / "data" / "denmark_cleaned.csv",
    "sweden_cleaned" : BLD / "python" / "data" / "sweden_cleaned.csv",
    }
    )
def task_clean_data(depends_on, produces):
    """Collects data saved by web scraper, and clean/shape it in a desired format."""
    data = clean_and_merge_nor(depends_on["capital_nor"], depends_on["hours_nor"], depends_on["value_added_nor"])  
    data.to_csv(produces["norway_cleaned"], index=False)

    data = clean_and_merge_den(depends_on["capital_den"], depends_on["capital2_den"], depends_on["hours_den"], depends_on["value_added_den"])
    data = replace_sector_names(data, den_nor)
    data.to_csv(produces["denmark_cleaned"], index=False)

    data = clean_and_merge_swe(depends_on["capital_swe"], depends_on["capital2_swe"], depends_on["hours_swe"], depends_on["value_added_swe"], col_names_swe)
    data = replace_sector_names(data, swe_nor)
    data.to_csv(produces["sweden_cleaned"], index=False)
    

    
    