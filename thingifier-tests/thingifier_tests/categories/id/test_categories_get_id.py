import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import xmltodict


# JSON BODY AND RESPONSE
def test_get_categories_id_should_return_corresponding_category(setup_each):
    print("Running test_get_categories_id_should_return_corresponding_category")
    res = httpx.get(categories_url + "/" + test_categories[0]["id"])
    actual = [test_categories[0]]
    assert res.status_code == 200
    assert contain_same_categories(res.json()["categories"], actual)


def test_get_categories_id_xml(setup_each):
    print("Running test_get_categories_id_xml")
    res = httpx.get(
        categories_url + "/" + test_categories[0]["id"], headers=XML_HEADERS
    )
    resJson = xmltodict.parse(res.content)
    assert res.status_code == 200
    assert resJson["categories"]["category"] == test_categories[0]


def test_get_categories_id_nonexsistent_should_return_error(setup_each):
    print("Running test_get_categories_id_nonexsistent_should_return_error")
    res = httpx.get(categories_url + "/99999")
    errorMessage = {
        "errorMessages": ["Could not find an instance with categories/99999"]
    }
    assert res.status_code == 404
    assert res.json() == errorMessage


def test_get_categories_id_nonexsistent_should_return_error_xml(setup_each):
    print("Running test_get_categories_id_nonexsistent_should_return_error_xml")
    res = httpx.get(categories_url + "/99999", headers=XML_HEADERS)
    errorMessage = "Could not find an instance with categories/99999"
    assert res.status_code == 404
    resJson = xmltodict.parse(res.content)
    assert resJson["errorMessages"]["errorMessage"] == errorMessage
