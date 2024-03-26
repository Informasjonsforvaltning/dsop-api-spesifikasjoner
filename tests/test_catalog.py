"""Unit test cases for the generateSpecification module."""
import hashlib

from pytest_mock import MockerFixture

from dsop_api_spesifikasjoner.catalog import API, Catalog


def test_Catalog_init(
    mocker: MockerFixture,
) -> None:
    """Should return a catalog instance with default values."""
    _id = hashlib.sha1(str.encode("DSOP API katalog"))  # noqa: S303,S324
    mocker.patch("hashlib.sha1", return_value=_id)
    _str_id = _id.hexdigest()
    catalog = Catalog(production=True)
    assert catalog
    assert (
        catalog.identifier
        == f"https://dataservice-publisher.digdir.no/catalogs/{_str_id}"
    )
    assert catalog.apis is not None
    assert len(catalog.apis) == 0


def test_API_init() -> None:
    """Should return a catalog instance with default values."""
    url_to_spec = "https://example.com/specification/oas_1"
    api = API(url_to_spec, "123")
    assert api
    assert api.identifier == "https://dataservice-publisher.digdir.no/dataservices/123"
    assert api.url == "https://example.com/specification/oas_1"


def test_add_API_to_catalog() -> None:
    """Should return a catalog instance with list of APIs."""
    catalog = Catalog(production=True)
    url_to_spec = "https://example.com/specification/oas_1"
    api = API(url_to_spec, "123")
    catalog.apis.append(api)
    assert catalog.apis
    assert len(catalog.apis) == 1
