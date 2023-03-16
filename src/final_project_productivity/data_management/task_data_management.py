import pandas as pd
import pytask
import os
from final_project_productivity.config import BLD
from final_project_productivity.data_management.clean_data import clean_and_merge_nor, clean_and_merge_den, clean_and_merge_swe, replace_sector_names
pd.options.mode.chained_assignment = None
from final_project_productivity.utilities import read_yaml

col_names_swe = [["sector", "year", "none", "none", "CF"],
             ["sector", "year", "none", "none", "FA"],
             ["sector", "year", "none", "TH", "none"],
             ["sector", "year", "VA", "CE", "CC"]]

current_file_dir = os.path.dirname(os.path.abspath(__file__))
specs_dir = os.path.join(current_file_dir, '..')
specs_dir = os.path.abspath(specs_dir)

specs = read_yaml(f"{specs_dir}\web_scraping_specs.yml")
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
    })
def task_clean_data_python(depends_on, produces):
    """Collects data saved by web scraper, and clean/shape it in a desired format."""

    capital_nor = pd.read_excel(depends_on["capital_nor"])
    hours_nor = pd.read_excel(depends_on["hours_nor"])
    value_added_nor = pd.read_excel(depends_on["value_added_nor"])

    capital_den = pd.read_excel(depends_on["capital_den"])
    capital2_den = pd.read_excel(depends_on["capital2_den"])
    hours_den = pd.read_excel(depends_on["hours_den"])
    value_added_den = pd.read_excel(depends_on["value_added_den"])

    capital_swe = pd.read_excel(depends_on["capital_swe"])
    capital2_swe = pd.read_excel(depends_on["capital2_swe"])
    hours_swe = pd.read_excel(depends_on["hours_swe"])
    value_added_swe = pd.read_excel(depends_on["value_added_swe"])

    data = clean_and_merge_nor(capital_nor, hours_nor, value_added_nor)  
    data.to_csv(produces["norway_cleaned"], index=False)

    data = clean_and_merge_den(capital_den, hours_den, value_added_den, capital2_den)
    data = replace_sector_names(data, den_nor)
    data.to_csv(produces["denmark_cleaned"], index=False)

    data = clean_and_merge_swe(capital_swe, hours_swe, value_added_swe, capital2_swe, col_names_swe)
    data = replace_sector_names(data, swe_nor)
    data.to_csv(produces["sweden_cleaned"], index=False)

    
    