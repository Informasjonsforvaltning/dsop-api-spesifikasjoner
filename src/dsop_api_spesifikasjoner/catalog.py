"""Module for Catalog class."""
import hashlib
from typing import List


class API:
    """Class representing a json dataservice (API)."""

    def __init__(self, url: str) -> None:
        """Inits an API."""
        self.identifier = "https://dataservice-publisher.digdir.no/dataservices/{id}"
        self.url = url
        self.conformsTo: List[str] = []
        self.publisher = ""


class Catalog:
    """Class representing a json dataservice catalog."""

    def __init__(self, production: bool) -> None:
        """Inits a catalog with fixed values."""
        catalog_title = "DSOP API katalog"
        if not production:
            catalog_title = catalog_title + " [TEST]"
        id = hashlib.sha1(str.encode(catalog_title)).hexdigest()  # noqa: S303
        self.identifier = f"https://dataservice-publisher.digdir.no/catalogs/{id}"
        self.title = {"nb": catalog_title}
        self.description = {"nb": "Samling av kontoopplysnings API"}
        self.publisher = "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/991825827"  # noqa: B950
        self.apis: List[API] = []
