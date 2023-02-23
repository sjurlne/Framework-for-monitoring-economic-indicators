"""Tasks for managing the data."""

import pandas as pd
import pytask

"""
from final_project_productivity.config import BLD, SRC
from final_project_productivity.data_management import clean_data
from final_project_productivity.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
        "data": SRC / "data" / "data.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "data_clean.csv")
def task_clean_data_python(depends_on, produces):
    """"""Clean the data.""""""
"""