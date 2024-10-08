import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import os


# JSON BODY AND RESPONSE
def test_head_id_categories_should_return_200(setup_each):
    print("Running test_head_id_categories_should_return_200")
    res = httpx.head(categories_url + "/" + test_categories[0]["id"])
    assert res.status_code == 200


def test_head_categories_id_xml(setup_each):
    print("Running test_head_categories_id_xml")
    res = httpx.head(
        categories_url + "/" + test_categories[0]["id"], headers=XML_HEADERS
    )
    assert res.status_code == 200


def test_head_id_categories_nonexistent_should_return_404(setup_each):
    print("Running test_head_id_categories_nonexistent_should_return_404")
    res = httpx.head(categories_url + "/99999")
    assert res.status_code == 404


def test_head_id_categories_nonexistent_should_return_404_xml(setup_each):
    print("Running test_head_id_categories_nonexistent_should_return_404_xml")
    res = httpx.head(categories_url + "/99999", headers=XML_HEADERS)
    assert res.status_code == 404
