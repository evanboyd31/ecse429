import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import xmltodict


# JSON BODY AND RESPONSE
def test_delete_categories_should_return_200(setup_each):
    print("Running test_delete_categories_should_return_200")
    res = httpx.delete(categories_url + "/" + test_categories[0]["id"])
    assert res.status_code == 200
    resGet = httpx.get(categories_url + "/" + test_categories[0]["id"])
    assert resGet.status_code == 404

def test_delete_categories_id_xml(setup_each):
    print("Running test_delete_categories_id_xml")
    res = httpx.delete(
        categories_url + "/" + test_categories[0]["id"], headers=XML_HEADERS
    )
    assert res.status_code == 200
    resGet = httpx.get(categories_url + "/" + test_categories[0]["id"])
    assert resGet.status_code == 404

def test_delete_categories_nonexistent_should_return_404(setup_each):
    print("Running test_delete_categories_nonexistent_should_return_404")
    res = httpx.delete(categories_url + "/99999")
    errorMessage = {
        "errorMessages": ["Could not find any instances with categories/99999"]
    }
    assert res.status_code == 404
    assert res.json() == errorMessage

def test_delete_categories_nonexistent_should_return_404_xml(setup_each):
    print("Running test_delete_categories_nonexistent_should_return_404_xml")
    res = httpx.delete(categories_url + "/99999", headers=XML_HEADERS)
    errorMessage = "Could not find any instances with categories/99999"
    assert res.status_code == 404
    resJson = xmltodict.parse(res.content)
    assert resJson['errorMessages']['errorMessage'] == errorMessage
