import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import os

# JSON BODY AND RESPONSE
def test_post_id_categories_allfields_should_return_categorymodified(setup_each):
    print("Running test_post_id_categories_allfields_should_return_categorymodified")
    modify_category = {"title":"Never seen before title", "description": "Never seen before description"}
    res = httpx.post(categories_url + '/' + test_categories[0]['id'], json=modify_category)
    modify_category.update({"id":test_categories[0]["id"]})
    assert res.status_code == 200
    assert res.json() == modify_category

def test_post_id_categories_titlefield_should_return_categorymodified(setup_each):
    print("Running test_post_id_categories_titlefield_should_return_categorymodified")
    modify_category = {"title":"Never seen before title"}
    res = httpx.post(categories_url + '/' + test_categories[0]['id'], json=modify_category)
    modify_category.update({"id":test_categories[0]["id"], "description":test_categories[0]["description"]})
    assert res.status_code == 200
    assert res.json() == modify_category

def test_post_id_categories_conflictid_should_return_badrequest(setup_each):
    print("Running test_post_id_categories_conflictid_should_return_badrequest")
    modify_category = {"id":test_categories[1]["id"], "title":"Never seen before title"}
    res = httpx.post(categories_url + '/' + test_categories[0]['id'], json=modify_category)
    assert res.status_code == 400

def test_post_id_categories_nonexistent_should_return_notfound(setup_each):
    print("Running test_post_id_categories_nonexistent_should_return_notfound")
    modify_category = {"title":"Never seen before title"}
    res = httpx.post(categories_url + '/99999', json=modify_category)
    errorMessage = {"errorMessages":[f"No such category entity instance with GUID or ID 99999 found"]}
    assert res.status_code == 404
    assert res.json() == errorMessage

def test_post_id_categories_query_conflicting_should_return_badrequest(setup_each):
    print("Running test_post_id_categories_query_conflicting_should_return_badrequest")
    modify_category = {"title":"Never seen before title"}
    res = httpx.post(categories_url + '/' + test_categories[0]['id'] + '?id=99999', json=modify_category)
    assert res.status_code == 400

def test_post_id_categories_modifyid_should_return_categorymodified(setup_each):
    print("Running test_post_id_categories_query_conflicting_should_return_badrequest")
    modify_category = {"id": "32", "title":"Never seen before title"}
    res = httpx.post(categories_url + '/' + test_categories[0]['id'], json=modify_category)
    modify_category.update({"description": test_categories[0]["description"]})
    assert res.status_code == 200
    assert res.json() == modify_category

# Add a test to check that we can't create without specifying the title

# Add a test to check that we can't create without specifying the title empty
