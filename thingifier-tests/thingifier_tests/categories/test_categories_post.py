import httpx
from thingifier_tests.test_common import *
from thingifier_tests.categories.test_categories_common import *
import os

# JSON BODY AND RESPONSE
def test_post_categories_allfields_should_return_categorycreated(setup_module, setup_each):
    print("Running test_post_categories_allfields_should_return_categorycreated")
    new_category = {"title":"Never seen before title", "description": "Never seen before description"}
    res = httpx.post(categories_url, json=new_category)
    actual = new_category
    assert res.status_code == 201
    del res.json()['id']
    assert res.json() == actual

def test_post_categories_withid_should_return_error(setup_module, setup_each):
    print("Running test_post_categories_withid_should_return_error")
    new_category = {"id": 23, "title":"Never seen before title", "description": "Never seen before description"}
    res = httpx.post(categories_url, json=new_category)
    errorMessage = {"errorMessages":["Invalid Creation: Failed Validation: Not allowed to create with id"]}
    assert res.status_code == 400
    assert res.json() == errorMessage

def test_post_categories_typeerror_should_return_error(setup_module, setup_each):
    print("Running test_post_categories_typeerror_should_return_error")
    new_category = {"title": 235, "description": "Never seen before description"}
    res = httpx.post(categories_url, json=new_category)
    assert res.status_code == 400

def test_post_categories_titleexistant_should_return_categorycreated(setup_module, setup_each):
    print("Running test_post_categories_typeerror_should_return_error")
    new_category = {"title": "A title", "description": "Never seen before description"}
    res = httpx.post(categories_url, json=new_category)
    actual = new_category
    del res.json()['id']
    assert res.status_code == 201
    assert res.json() == actual
