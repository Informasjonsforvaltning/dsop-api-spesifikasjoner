"""Unit test cases for the generateSpecification module."""
from pytest_mock import MockerFixture

from dsop_api_spesifikasjoner.catalog import API, Catalog


def test_Catalog_init(
    mocker: MockerFixture,
) -> None:
    """Should return a catalog instance with default values."""
    mocker.patch("uuid.uuid4", return_value=1234)

    catalog = Catalog()
    assert catalog
    assert catalog.identifier == "https://dataservice-publisher.digdir.no/catalogs/1234"
    assert catalog.apis is not None
    assert len(catalog.apis) == 0


def test_API_init(
    mocker: MockerFixture,
) -> None:
    """Should return a catalog instance with default values."""
    mocker.patch("uuid.uuid4", return_value=4321)
    url_to_spec = "https://example.com/specification/oas_1"
    api = API(url_to_spec)
    assert api
    assert api.identifier == "https://dataservice-publisher.digdir.no/dataservices/4321"
    assert api.url == "https://example.com/specification/oas_1"


def test_add_API_to_catalog() -> None:
    """Should return a catalog instance with list of APIs."""
    catalog = Catalog()
    url_to_spec = "https://example.com/specification/oas_1"
    api = API(url_to_spec)
    catalog.apis.append(api)
    assert catalog.apis
    assert len(catalog.apis) == 1
