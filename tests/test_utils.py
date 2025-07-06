from unittest.mock import patch

import requests

import src.utils as utils


# ready
@patch("requests.request")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {
        "status": "200",
        "message": "rates",
        "data": {"USDRUB": "97.31"},
    }

    requests.request = mock_get
    assert utils.get_currency_rates("USD") == 97
