import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import os


# JSON BODY AND RESPONSE
def test_delete_categories_should_return_200(setup_each):
    print("Running test_post_categories_allfields_should_return_categorycreated")
    res = httpx.delete(categories_url + "/" + test_categories[0]["id"])
    assert res.status_code == 200


def test_delete_categories_nonexistent_should_return_404(setup_each):
    print("Running test_post_categories_allfields_should_return_categorycreated")
    res = httpx.delete(categories_url + "/99999")
    errorMessage = {
        "errorMessages": ["Could not find any instances with categories/99999"]
    }
    assert res.status_code == 404
    assert res.json() == errorMessage


def test_delete_categories_query_conflicting_should_return_400(setup_each):
    print("Running test_post_categories_allfields_should_return_categorycreated")
    res = httpx.delete(categories_url + "/" + test_categories[0]["id"] + "?id=99999")
    assert res.status_code == 400
