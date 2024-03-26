"""Module for Catalog class."""
import hashlib
from typing import List


class API:
    """Class representing a json dataservice (API)."""

    def __init__(self, url: str, predefined_id: str) -> None:
        """Inits an API."""
        api_id = (
            predefined_id
            if len(predefined_id) > 0
            else hashlib.sha1(str.encode(url), usedforsecurity=False).hexdigest()
        )
        self.identifier = (
            f"https://dataservice-publisher.digdir.no/dataservices/{api_id}"
        )
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
        catalog_id = hashlib.sha1(
            str.encode(catalog_title), usedforsecurity=False
        ).hexdigest()
        self.identifier = (
            f"https://dataservice-publisher.digdir.no/catalogs/{catalog_id}"
        )
        self.title = {"nb": catalog_title}
        self.description = {"nb": "Samling av kontoopplysnings API"}
        self.publisher = "https://organization-catalog.fellesdatakatalog.digdir.no/organizations/991825827"  # noqa: B950
        self.apis: List[API] = []
