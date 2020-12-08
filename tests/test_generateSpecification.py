"""Unit test cases for the generateSpecification module."""
import json
from pathlib import Path
from typing import Any, Dict, List

from click.testing import CliRunner
from deepdiff import DeepDiff
import pytest
from pytest_mock import MockerFixture
import yaml


from dsop_api_spesifikasjoner.generateSpecification import _generateSpec, main

URL_BASE = (
    "https://raw.githubusercontent.com/"
    "Informasjonsforvaltning/dsop-api-spesifikasjoner/master/specs/"
)


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_generateSpec() -> None:
    """Should return a bank specific spec as dict."""
    template = _get_openapi_template()
    bank = _get_bank()

    _spec = _generateSpec(template, bank)

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


def test_main(mocker: MockerFixture, runner: CliRunner) -> None:
    """Should return exit_code 0."""
    # Set up mock for uuid4:
    mocker.patch("uuid.uuid4", return_value=1234)

    with runner.isolated_filesystem():
        with open("banker.csv", "w") as f:
            f.write("OrgNummer,Navn,Filnavn,EndepunktProduksjon,EndepunktTest\n")
            f.write(
                "837884942,SPAREBANK 1 ØSTFOLD AKERSHUS,"
                "Sparebank1_837884942_Accounts-API.json,"
                "https://api.sparebank1.no/dsop/Service/v2/837884942,"
                "https://api-test.sparebank1.no/dsop/Service/v2/837884942"
                "\n"
            )
        with open("template.yaml", "w") as t:
            t.write("openapi: 3.0.0\n")
            t.write("info:\n")
            t.write("  title: Accounts API\n")
            t.write("servers:\n")
            t.write("  - url: 'https://hostname.no/v1'\n")
            t.write("    description: 'production'\n")
            t.write("  - url: 'https://hostname.no/v1'\n")
            t.write("    description: 'test'\n")

        result = runner.invoke(main, ["template.yaml", "banker.csv"])
        assert result.output == ""
        assert result.exit_code == 0
        # check that a specification file has been created and has correct content:
        specification_file = Path("Sparebank1_837884942_Accounts-API.json")
        assert specification_file.is_file()
        with open("Sparebank1_837884942_Accounts-API.json", "r") as s:
            _specification = json.load(s)
        _correct_specification = json.loads(
            """
        {
           "openapi": "3.0.0",
           "info": {
              "title": "Accounts API SPAREBANK 1 ØSTFOLD AKERSHUS"
           },
           "servers": [
              {
                 "description": "production",
                 "url": "https://api.sparebank1.no/dsop/Service/v2/837884942"
              },
              {
                 "description": "test",
                 "url": "https://api-test.sparebank1.no/dsop/Service/v2/837884942"
              }
           ]
        }
        """
        )
        ddiff = DeepDiff(
            _specification,
            _correct_specification,
            ignore_order=True,
            report_repetition=True,
        )
        if ddiff:
            print(ddiff)
        assert not ddiff

        # check that a dsop_catalog.json file has been created and has correct content:
        catalog_file = Path("dsop_catalog.json")
        assert catalog_file.is_file()
        with open("dsop_catalog.json", "r") as c:
            _catalog = json.load(c)
        _correct_catalog_string = """
        {
          "identifier": "https://dataservice-publisher.digdir.no/catalogs/1234",
          "title": {
            "nb": "DSOP API katalog"
          },
          "description": {
            "nb": "Samling av kontoopplysnings API"
          },
          "publisher": "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/991825827",
          "apis": [
           {
            "identifier": "https://dataservice-publisher.digdir.no/dataservices/1234",
            "publisher": "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/837884942",
            "url": "%s",
            "conformsTo": [
               "https://data.norge.no/specification/kontoopplysninger"
            ]
           }
          ]
        }
        """ % (
            URL_BASE + "Sparebank1_837884942_Accounts-API.json"
        )
        print(_correct_catalog_string)
        _correct_catalog = json.loads(_correct_catalog_string)
        ddiff = DeepDiff(
            _catalog,
            _correct_catalog,
            ignore_order=True,
            report_repetition=True,
        )
        if ddiff:
            print(ddiff)
        assert not ddiff


def test_main_fails_trailing_slash_1(runner: CliRunner) -> None:
    """Should return exit_code 0."""
    with runner.isolated_filesystem():
        with open("banker.csv", "w") as f:
            f.write("OrgNummer,Navn,Filnavn,EndepunktProduksjon,EndepunktTest\n")
            f.write(
                "837884942,SPAREBANK 1 ØSTFOLD AKERSHUS,"
                "Sparebank1_837884942_Accounts-API.json,"
                "https://api.sparebank1.no/dsop/Service/v2/837884942/,"
                "https://api-test.sparebank1.no/dsop/Service/v2/837884942"
                "\n"
            )
        with open("template.yaml", "w") as t:
            t.write("openapi: 3.0.0\n")
            t.write("info:\n")
            t.write("  title: Accounts API\n")
            t.write("servers:\n")
            t.write("  - url: 'https://hostname.no/v1'\n")
            t.write("    description: 'production'\n")
            t.write("  - url: 'https://hostname.no/v1'\n")
            t.write("    description: 'test'\n")

        result = runner.invoke(main, ["template.yaml", "banker.csv"])
        assert result.exit_code == 1
        assert result.output is not None


def test_main_fails_trailing_slash_2(runner: CliRunner) -> None:
    """Should return exit_code 0."""
    with runner.isolated_filesystem():
        with open("banker.csv", "w") as f:
            f.write("OrgNummer,Navn,Filnavn,EndepunktProduksjon,EndepunktTest\n")
            f.write(
                "837884942,SPAREBANK 1 ØSTFOLD AKERSHUS,"
                "Sparebank1_837884942_Accounts-API.json,"
                "https://api.sparebank1.no/dsop/Service/v2/837884942,"
                "https://api-test.sparebank1.no/dsop/Service/v2/837884942/"
                "\n"
            )
        with open("template.yaml", "w") as t:
            t.write("openapi: 3.0.0\n")
            t.write("info:\n")
            t.write("  title: Accounts API\n")
            t.write("servers:\n")
            t.write("  - url: 'https://hostname.no/v1'\n")
            t.write("    description: 'production'\n")
            t.write("  - url: 'https://hostname.no/v1'\n")
            t.write("    description: 'test'\n")

        result = runner.invoke(main, ["template.yaml", "banker.csv"])
        assert result.exit_code == 1
        assert result.output is not None


def test_main_with_no_arguments_fails(runner: CliRunner) -> None:
    """Should return exit_code 2."""
    runner = CliRunner()

    result = runner.invoke(main)
    assert result.exit_code == 2


# --
def _get_openapi_template() -> Dict[str, Any]:
    """Create an openAPI-specification dokument."""
    with open("./template/Accounts API openapi v1.0.0.yaml", "r") as file:
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
