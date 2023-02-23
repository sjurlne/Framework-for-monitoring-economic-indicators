"""Tasks running the core analyses."""
"""
import pandas as pd
import pytask

#from final_project_productivity.analysis.model import fit_logit_model, load_model
from final_project_productivity.config import BLD, GROUPS, SRC
"""
"""
@pytask.mark.depends_on(
    {
        "scripts": ["model.py", "predict.py"],
        "data": BLD / "python" / "data" / "data_clean.csv",
        "data_info": SRC / "data_management" / "data_info.yaml",
    },
)
@pytask.mark.produces(BLD / "python" / "models" / "model.pickle")
def task_fit_model_python(depends_on, produces):
    
"""