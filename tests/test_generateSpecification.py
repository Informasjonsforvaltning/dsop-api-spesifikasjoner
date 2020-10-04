"""Unit test cases for the catalog module."""
from typing import Any, Dict, List

import yaml

from dsop_api_spesifikasjoner.generateSpecification import generateSpec


def test_generateSpec() -> None:
    """Should return a bank specific spec as dict."""
    template = _get_openapi_template()
    bank = _get_bank()

    _spec = generateSpec(template, bank)

    assert isinstance(_spec, dict)
    assert _spec["info"]["title"] == "Accounts API SPAREBANK 1 ØSTFOLD AKERSHUS"
    assert _spec["servers"][0]["description"] == "production"
    assert (
        _spec["servers"][0]["url"] == "https://api.sparebank1.no/Service/v2/837884942"
    )
    assert _spec["servers"][1]["description"] == "test"
    assert (
        _spec["servers"][1]["url"]
        == "https://api-test.sparebank1.no/Service/v2/837884942"
    )


# --
def _get_openapi_template() -> Dict[str, Any]:
    """Create a mock openAPI-specification dokument."""
    with open("./template/Accounts API openapi v1.0.0-RC2.yaml", "r") as file:
        _yaml = yaml.safe_load(file)

    return _yaml


def _get_bank() -> List[str]:
    bank_str = (
        "837884942,"
        "SPAREBANK 1 ØSTFOLD AKERSHUS,"
        "Sparebank1_837884942_Accounts-API.json,"
        "https://api.sparebank1.no/Service/v2/837884942,"
        "https://api-test.sparebank1.no/Service/v2/837884942"
    )
    return bank_str.split(",")
