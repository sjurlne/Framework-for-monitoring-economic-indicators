"""Tests for the regression model."""

import numpy as np
import pandas as pd
import pytest
from final_project_productivity.analysis.model import fit_logit_model

DESIRED_PRECISION = 10e-2

"""
@pytest.fixture()
def data():
    return pd.DataFrame(
        {"outcome_numerical": np.random.binomial(1, prob), "covariate": x},
    )
"""

"""
@pytest.fixture()
def data_info():
    return {"outcome": "outcome", "outcome_numerical": "outcome_numerical"}
"""
"""
def test_fit_logit_model_recover_coefficients(data, data_info):
    assert np.abs(params["Intercept"]) < DESIRED_PRECISION
"""