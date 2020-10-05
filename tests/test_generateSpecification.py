"""Unit test cases for the catalog module."""
from typing import Any, Dict, List

from click.testing import CliRunner
import pytest
import yaml


from dsop_api_spesifikasjoner.generateSpecification import _generateSpec, main


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


def test_main(runner: CliRunner) -> None:
    """Should return exit_code 0."""
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

        result = runner.invoke(main, ["template.yaml", "banker.csv", "."])
        assert result.output == ""
        assert result.exit_code == 0


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

        result = runner.invoke(main, ["template.yaml", "banker.csv", "."])
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

        result = runner.invoke(main, ["template.yaml", "banker.csv", "."])
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
