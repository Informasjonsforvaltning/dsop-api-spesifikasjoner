"""Unit test cases for the generateSpecification module."""
import json
import os
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

    _spec = _generateSpec(template, bank, production=True)

    assert isinstance(_spec, dict)
    assert _spec["info"]["title"] == "Accounts API SPAREBANK 1 ØSTFOLD AKERSHUS"
    assert _spec["servers"][0]["description"] == "production"
    assert (
        _spec["servers"][0]["url"] == "https://api.sparebank1.no/Service/v2/837884942"
    )

    _spec = _generateSpec(template, bank, production=False)
    assert _spec["servers"][0]["description"] == "test"
    assert (
        _spec["servers"][0]["url"]
        == "https://api-test.sparebank1.no/Service/v2/837884942"
    )


def test_main(mocker: MockerFixture, runner: CliRunner) -> None:
    """Should return exit_code 0."""
    with runner.isolated_filesystem():
        with open("banker.csv", "w") as f:
            f.write(
                "OrgNummer,Navn,Filnavn,EndepunktProduksjon,EndepunktTest,Id,TestId\n"
            )
            f.write(
                "837884942,SPAREBANK 1 ØSTFOLD AKERSHUS,"
                "Sparebank1_837884942_Accounts-API.json,"
                "https://api.sparebank1.no/dsop/Service/v2/837884942,"
                "https://api-test.sparebank1.no/dsop/Service/v2/837884942,"
                ","
                "\n"
            )
        with open("template.yaml", "w") as t:
            t.write("openapi: 3.0.0\n")
            t.write("info:\n")
            t.write("  title: Accounts API\n")
            t.write("servers:\n")
            t.write("  - url: 'https://hostname.no/v1'\n")

        result = runner.invoke(main, ["template.yaml", "banker.csv", "False"])
        assert result.output == ""
        assert result.exit_code == 0

        # Specification-file for prod-environment
        specification_file = Path("Sparebank1_837884942_Accounts-API.json")
        assert specification_file.is_file()
        with open(specification_file, "r") as s:
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

        # Specification-file for test-environment
        specification_filename = os.path.join(
            "test", "Sparebank1_837884942_Accounts-API.json"
        )
        specification_file = Path(specification_filename)
        assert specification_file.is_file()
        with open(specification_file, "r") as s:
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

        # check that a prod dsop_catalog.json file has been created and has correct content:
        catalog_filename = "dsop_catalog.json"
        catalog_file = Path(catalog_filename)
        assert catalog_file.is_file()
        with open(catalog_file, "r") as c:
            _catalog = json.load(c)
        _correct_catalog_string = """
        {
          "identifier": "https://dataservice-publisher.digdir.no/catalogs/2d795f2e16757134b064f2a5cfa4ec9a2f85fa36",
          "title": {
            "nb": "DSOP API katalog"
          },
          "description": {
            "nb": "Samling av kontoopplysnings API"
          },
          "publisher": "https://organization-catalog.fellesdatakatalog.digdir.no/organizations/991825827",
          "apis": [
           {
            "identifier": "https://dataservice-publisher.digdir.no/dataservices/34472b326c22e41650828da4a13ffff41d1a7cf0",
            "publisher": "https://organization-catalog.fellesdatakatalog.digdir.no/organizations/837884942",
            "url": "%s",
            "conformsTo": [
               "https://bitsnorge.github.io/dsop-accounts-api"
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

        # check that a test dsop_catalog.json file has been created and has correct content:
        catalog_filename = os.path.join("test", "dsop_catalog_test.json")
        catalog_file = Path(catalog_filename)
        assert catalog_file.is_file()
        with open(catalog_file, "r") as c:
            _catalog = json.load(c)
        _correct_catalog_string = """
        {
          "identifier": "https://dataservice-publisher.digdir.no/catalogs/6071cb9b1ec01bd2748130ab212d7c04650b1cde",
          "title": {
            "nb": "DSOP API katalog [TEST]"
          },
          "description": {
            "nb": "Samling av kontoopplysnings API"
          },
          "publisher": "https://organization-catalog.fellesdatakatalog.digdir.no/organizations/991825827",
          "apis": [
           {
            "identifier": "https://dataservice-publisher.digdir.no/dataservices/a9227a94f668f23b64bd676873832b70962011ee",
            "publisher": "https://organization-catalog.fellesdatakatalog.digdir.no/organizations/837884942",
            "url": "%s",
            "conformsTo": [
               "https://bitsnorge.github.io/dsop-accounts-api"
            ]
           }
          ]
        }
        """ % (
            URL_BASE + "test/" + "Sparebank1_837884942_Accounts-API.json"
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
            f.write(
                "OrgNummer,Navn,Filnavn,EndepunktProduksjon,EndepunktTest,Id,TestId\n"
            )
            f.write(
                "837884942,SPAREBANK 1 ØSTFOLD AKERSHUS,"
                "Sparebank1_837884942_Accounts-API.json,"
                "https://api.sparebank1.no/dsop/Service/v2/837884942/,"
                "https://api-test.sparebank1.no/dsop/Service/v2/837884942,"
                ","
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

        result = runner.invoke(main, ["template.yaml", "banker.csv", "False"])
        assert result.exit_code == 1
        assert result.output is not None


def test_main_fails_trailing_slash_2(runner: CliRunner) -> None:
    """Should return exit_code 0."""
    with runner.isolated_filesystem():
        with open("banker.csv", "w") as f:
            f.write(
                "OrgNummer,Navn,Filnavn,EndepunktProduksjon,EndepunktTest,Id,TestId\n"
            )
            f.write(
                "837884942,SPAREBANK 1 ØSTFOLD AKERSHUS,"
                "Sparebank1_837884942_Accounts-API.json,"
                "https://api.sparebank1.no/dsop/Service/v2/837884942,"
                "https://api-test.sparebank1.no/dsop/Service/v2/837884942/,"
                ","
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

        result = runner.invoke(main, ["template.yaml", "banker.csv", "False"])
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
        "https://api-test.sparebank1.no/Service/v2/837884942,"
        ","
    )
    return bank_str.split(",")
