"""Module for generate openAPI specifications."""
import copy
import csv
import json
import os
from pathlib import Path
import sys
from typing import Any, List

import click
import yaml

from . import __version__
from .catalog import API, Catalog


@click.command()
@click.version_option(version=__version__)
@click.argument("template", type=click.File("r"))
@click.argument("input", type=click.File("r"))
@click.option(
    "-d",
    "--directory",
    default=".",
    help="The output directory",
    show_default=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        writable=True,
    ),
)
def main(template: Any, input: Any, directory: Any) -> None:
    """Write specification and catalog file based on template for bank."""
    # Add a trailing slash to directory if not there:
    directory = os.path.join(directory, "")
    template = yaml.safe_load(template)
    input = csv.reader(input, delimiter=",")
    prod_catalog_filename = os.path.join(directory, "dsop_catalog.json")
    Path("test").mkdir(parents=True, exist_ok=True)
    test_catalog_filename = os.path.join(directory, "test", "dsop_catalog_test.json")
    prod_catalog = Catalog(production=True)
    test_catalog = Catalog(production=False)
    # skipping first row, which is headers:
    next(input)
    for bank in input:
        orgnummer = bank[0]
        if bank[3] and len(bank[3]) > 0:  # Production
            # Validate Prod url:
            if bank[3].endswith("/"):
                sys.exit(
                    "ERROR: Trailing slash in url is not allowed >" + bank[3] + "<"
                )
            spec = _generateSpec(template, bank, production=True)
            specification_filename = bank[2]
            specification_filedirectory = os.path.join(
                directory, specification_filename
            )
            _write_spec_to_file(specification_filedirectory, spec)
            _add_spec_to_catalog(orgnummer, specification_filename, prod_catalog)
        if bank[4] and len(bank[4]) > 0:  # Test
            # Validate Test url:
            if bank[4].endswith("/"):
                sys.exit(
                    "ERROR: Trailing slash in url is not allowed >" + bank[4] + "<"
                )
            spec = _generateSpec(template, bank, production=False)
            specification_filename = os.path.join("test", bank[2])
            specification_filedirectory = os.path.join(
                directory, specification_filename
            )
            _write_spec_to_file(specification_filedirectory, spec)
            _add_spec_to_catalog(orgnummer, specification_filename, test_catalog)

    _write_catalog_file(prod_catalog_filename, prod_catalog)
    _write_catalog_file(test_catalog_filename, test_catalog)


def _write_spec_to_file(specification_filedirectory: str, spec: dict) -> None:
    with open(specification_filedirectory, "w", encoding="utf-8") as outfile:
        json.dump(
            spec,
            outfile,
            ensure_ascii=False,
            indent=2,
        )


def _add_spec_to_catalog(
    orgnummer: str,
    specification_filename: str,
    catalog: Catalog,
) -> None:
    url = (
        "https://raw.githubusercontent.com/"
        "Informasjonsforvaltning/dsop-api-spesifikasjoner/master/specs/"
        f"{specification_filename}"
    )
    api = API(url)
    api.publisher = f"https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/{orgnummer}"  # noqa: B950
    api.conformsTo.append("https://data.norge.no/specification/kontoopplysninger")
    catalog.apis.append(api)


def _write_catalog_file(catalog_filename: str, catalog: Catalog) -> None:
    with open(catalog_filename, "w", encoding="utf-8") as catalogfile:
        json.dump(
            catalog.__dict__,
            catalogfile,
            default=lambda o: o.__dict__,
            ensure_ascii=False,
            indent=2,
        )


def _generateSpec(template: dict, bank: List[str], production: bool) -> dict:
    """Generate spec based on template for bank."""
    # Need to do a deepcopy to actually copy the template into a new object.
    specification = copy.deepcopy(template)
    # Then put the bank-specific values into the specification:
    specification["info"]["title"] = template["info"]["title"] + " " + bank[1]
    # We must recreate the Server object
    specification["servers"] = []
    # Prod url
    if production is True:
        server = {}
        server["url"] = bank[3]
        server["description"] = "production"
        specification["servers"].append(server)
    # Test url
    if production is False:
        server = {}
        server["url"] = bank[4]
        server["description"] = "test"
        specification["servers"].append(server)
    return specification
