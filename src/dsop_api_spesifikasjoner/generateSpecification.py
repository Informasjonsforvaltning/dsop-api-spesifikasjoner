"""Module for generate openAPI specifications."""
import copy
import csv
import json
import os
from pathlib import Path
import sys
from typing import Any, List

import click
import datacatalogtordf
from oastodcat import OASDataService
from rdflib.graph import Graph, URIRef
from requests import get
import yaml

from . import __version__
from .catalog import API, Catalog


@click.command()
@click.version_option(version=__version__)
@click.argument("template", type=click.File("r"))
@click.argument("input", type=click.File("r"))
@click.argument("use_local_files", type=click.BOOL)
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
def main(
    template: Any, input: Any, directory: Any, use_local_files: bool = True
) -> None:
    """Write specification and catalog file based on template for bank."""
    # Add a trailing slash to directory if not there:
    directory = os.path.join(directory, "")
    template = yaml.safe_load(template)
    input = csv.reader(input, delimiter=",")
    prod_catalog_filename = os.path.join(directory, "dsop_catalog.json")
    Path("test").mkdir(parents=True, exist_ok=True)
    test_catalog_filename = os.path.join(directory, "test", "dsop_catalog_test.json")
    Path("rdf").mkdir(parents=True, exist_ok=True)
    turtle_prod_catalog_filename = os.path.join(directory, "rdf", "dsop_catalog.ttl")
    turtle_test_catalog_filename = os.path.join(
        directory, "rdf", "dsop_catalog_test.ttl"
    )
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
            _add_spec_to_catalog(
                orgnummer, bank[5], specification_filename, prod_catalog
            )
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
            _add_spec_to_catalog(
                orgnummer, bank[6], specification_filename, test_catalog
            )

    _write_catalog_file(prod_catalog_filename, prod_catalog)
    _write_catalog_file(test_catalog_filename, test_catalog)

    _write_catalog_rdf_file(
        turtle_prod_catalog_filename,
        create_catalog_graph(prod_catalog, use_local_files),
    )
    _write_catalog_rdf_file(
        turtle_test_catalog_filename,
        create_catalog_graph(test_catalog, use_local_files),
    )


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
    api_id: str,
    specification_filename: str,
    catalog: Catalog,
) -> None:
    url = (
        "https://raw.githubusercontent.com/"
        "Informasjonsforvaltning/dsop-api-spesifikasjoner/master/specs/"
        f"{specification_filename}"
    )
    api = API(url, api_id)
    api.publisher = f"https://organization-catalog.fellesdatakatalog.digdir.no/organizations/{orgnummer}"  # noqa: B950
    api.conformsTo.append("https://bitsnorge.github.io/dsop-accounts-api")
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


def _write_catalog_rdf_file(catalog_filename: str, catalog: Graph) -> None:
    with open(catalog_filename, "w", encoding="utf-8") as catalogfile:
        catalogfile.write(catalog.serialize(format="turtle"))


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


def create_catalog_graph(catalog: Catalog, use_local_files: bool) -> Graph:
    """Create a graph based on catalog and persist to store."""
    # Use datacatalogtordf and oastodcat to create a graph and persist:
    g = datacatalogtordf.Catalog()
    g.identifier = URIRef(catalog.identifier)
    g.title = catalog.title
    g.description = catalog.description
    g.publisher = catalog.publisher

    for api in catalog.apis:
        if (
            use_local_files
            and "https://raw.githubusercontent.com/Informasjonsforvaltning/dsop-api-spesifikasjoner/master/"
            in api.url
        ):
            file_path = api.url.replace(
                "https://raw.githubusercontent.com/Informasjonsforvaltning/dsop-api-spesifikasjoner/master/",
                "",
            )
            api_spec_file = open(file_path, "r")
            api_spec = api_spec_file.read()
            api_spec_file.close()
            oas = yaml.safe_load(api_spec)
        else:
            with get(api.url, timeout=5) as response:
                if response.status_code == 200:
                    api_spec = response.text
                    oas = yaml.safe_load(api_spec)

        oas_spec = OASDataService(api.url, oas, api.identifier)
        oas_spec.conforms_to = api.conformsTo
        oas_spec.publisher = api.publisher

        # Add dataservices to catalog:
        for dataservice in oas_spec.dataservices:
            g.services.append(dataservice)

    return g._to_graph()
