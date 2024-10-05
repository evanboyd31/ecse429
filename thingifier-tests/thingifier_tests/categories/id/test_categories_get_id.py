import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import os



# JSON BODY AND RESPONSE
def test_get_categories_id_should_return_corresponding_category(setup_each):
    print("Running test_get_categories_id_should_return_corresponding_category")
    res = httpx.get(categories_url + "/" + test_categories[0]["id"])
    actual = [test_categories[0]]
    assert res.status_code == 200
    assert contain_same_categories(res.json()['categories'], actual)

def test_get_categories_id_nonexsistent_should_return_error(setup_each):
    print("Running test_get_categories_id_nonexsistent_should_return_corresponding_categories")
    res = httpx.get(categories_url + "/99999")
    errorMessage = {"errorMessages":["Could not find an instance with categories/10"]}
    assert res.status_code == 404
    assert contain_same_categories(res.json(), errorMessage)

def test_get_categories_id_query_inconsistent_should_return_badrequest(setup_each):
    print("Running test_get_categories_id_query_inconsistent_should_return_badrequest")
    res = httpx.get(categories_url + "/" + test_categories[0]["id"] + "?id=99999")
    assert res.status_code == 400
