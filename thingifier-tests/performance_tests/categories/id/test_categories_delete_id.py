import httpx
from performance_tests.conftest import *
from performance_tests.categories.conftest import *
import xmltodict


# JSON BODY AND RESPONSE
def test_delete_categories_should_return_200(setup_each):
    print("Running test_delete_categories_should_return_200")
    res = httpx.delete(categories_url + "/" + test_categories[0]["id"])
    assert res.status_code == 200
    resGet = httpx.get(categories_url + "/" + test_categories[0]["id"])
    assert resGet.status_code == 404
