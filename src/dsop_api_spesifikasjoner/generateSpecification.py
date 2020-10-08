"""Module for generate openAPI specifications."""
import copy
import csv
import json
import os
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
    catalog_filename = directory + "dsop_catalog.json"
    catalog = Catalog()
    # skipping first row, which is headers:
    next(input)
    for bank in input:
        orgnummer = bank[0]
        # specification_filedirectory = directory + specification_filename
        specification_filename = bank[2]
        specification_filedirectory = directory + specification_filename
        # Validate Prod url:
        if bank[3].endswith("/"):
            sys.exit("ERROR: Trailing slash in url is not allowed >" + bank[3] + "<")
        # Validate Test url:
        if bank[4].endswith("/"):
            sys.exit("ERROR: Trailing slash in url is not allowed >" + bank[4] + "<")
        spec = _generateSpec(template, bank)
        _write_spec_to_file(specification_filedirectory, spec)
        _add_spec_to_catalog(orgnummer, specification_filename, catalog)

    _write_catalog_file(catalog_filename, catalog)


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
    api.publisher = f"https://data.brreg.no/enhetsregisteret/api/enheter/{orgnummer}"
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


def _generateSpec(template: dict, bank: List[str]) -> dict:
    """Generate spec based on template for bank."""
    # Need to do a deepcopy to actually copy the template into a new object.
    specification = copy.deepcopy(template)
    # Then put the bank-specific values into the specification:
    specification["info"]["title"] = template["info"]["title"] + " " + bank[1]
    # We must recreate the Server object
    specification["servers"] = []
    # Prod url
    if len(bank[3]) > 0:
        server = {}
        server["url"] = bank[3]
        server["description"] = "production"
        specification["servers"].append(server)
    # Test url
    if len(bank[4]) > 0:
        server = {}
        server["url"] = bank[4]
        server["description"] = "test"
        specification["servers"].append(server)
    return specification
