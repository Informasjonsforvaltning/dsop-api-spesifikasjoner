"""Module for generate openAPI specifications."""
import copy
import csv
import json
import sys
from typing import Any, List

import click
import yaml

from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.argument("template", type=click.File("r"))
@click.argument("input", type=click.File("r"))
@click.argument("path", type=click.Path(exists=True))
def main(template: Any, input: Any, path: Any) -> None:
    """Write specifcation based on template for bank."""
    template = yaml.safe_load(template)
    input = csv.reader(input, delimiter=",")
    # extracting field names through first row
    next(input)
    for bank in input:
        # specificationFileName = specificationPath + bank[2]
        specificationFileName = path + bank[2]
        # Validate Prod url:
        if bank[3].endswith("/"):
            sys.exit("ERROR: Trailing slash in url is not allowed >" + bank[3] + "<")
        # Validate Test url:
        if bank[4].endswith("/"):
            sys.exit("ERROR: Trailing slash in url is not allowed >" + bank[4] + "<")
        spec = _generateSpec(template, bank)
        with open(specificationFileName, "w", encoding="utf-8") as outfile:
            json.dump(
                spec,
                outfile,
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
