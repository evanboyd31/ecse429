import httpx
from performance_tests.conftest import *
from performance_tests.categories.conftest import *
import xmltodict


# JSON BODY AND RESPONSE
def test_post_categories_allfields_should_return_categorycreated(setup_each):
    print("Running test_post_categories_allfields_should_return_categorycreated")
    new_category = {
        "title": "Never seen before title",
        "description": "Never seen before description",
    }
    res = httpx.post(categories_url, json=new_category)
    actual = new_category
    assert res.status_code == 201
    resJson = res.json()
    resJson.pop("id")
    assert resJson == actual
