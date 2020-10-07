"""Unit test cases for the generateSpecification module."""


from dsop_api_spesifikasjoner.catalog import Catalog


def test_Catalog_init() -> None:
    """Should return a catalog instance with default values."""
    catalog = Catalog()
    assert catalog
