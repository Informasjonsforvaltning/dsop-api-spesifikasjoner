"""Module for Catalog class."""
from typing import List
import uuid


class API:
    """Class representing a json dataservice (API)."""

    def __init__(self, url: str) -> None:
        """Inits an API."""
        id = str(uuid.uuid4())
        self.identifier = f"https://dataservice-publisher.digdir.no/dataservices/{id}"
        self.url = url
        self.conformsTo: List[str] = []
        self.publisher = ""


class Catalog:
    """Class representing a json dataservice catalog."""

    def __init__(self) -> None:
        """Inits a catalog with fixed values."""
        id = str(uuid.uuid4())
        self.identifier = f"https://dataservice-publisher.digdir.no/catalogs/{id}"
        self.title = {"nb": "DSOP API katalog"}
        self.description = {"nb": "Samling av kontoopplysnings API"}
        self.publisher = "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
        self.apis: List[API] = []
