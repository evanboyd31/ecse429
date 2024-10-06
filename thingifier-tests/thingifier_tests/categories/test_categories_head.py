import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import xmltodict

# JSON BODY AND RESPONSE
def test_head_categories_should_return_200(setup_each):
    print("Running test_head_categories_should_return_200")
    res = httpx.head(categories_url)
    assert res.status_code == 200

def test_head_categories_xml(setup_each):
    print("test_get_categories_xml")
    res = httpx.head(categories_url, headers=XML_HEADERS)
    assert res.status_code == 200
