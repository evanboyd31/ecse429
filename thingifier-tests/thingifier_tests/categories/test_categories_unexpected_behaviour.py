import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *


def test_get_categories_query_faulty_should_return_badrequest(setup_each):
    print("Running test_get_categories_query_faulty_should_return_badrequest")
    res = httpx.get(categories_url + "?id=asdf")
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_get_categories_id_query_inconsistent_should_return_badrequest(setup_each):
    print("Running test_get_categories_id_query_inconsistent_should_return_badrequest")
    res = httpx.get(categories_url + "/" + test_categories[0]["id"] + "?id=99999")
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_post_categories_typeerror_should_return_error(setup_each):
    print("Running test_post_categories_typeerror_should_return_error")
    new_category = {"title": 235, "description": "Never seen before description"}
    res = httpx.post(categories_url, json=new_category)
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_post_id_categories_conflictid_should_return_badrequest(setup_each):
    print("Running test_post_id_categories_conflictid_should_return_badrequest")
    modify_category = {
        "id": int(test_categories[1]["id"]),
        "title": "Never seen before title",
    }
    res = httpx.post(
        categories_url + "/" + test_categories[0]["id"], json=modify_category
    )
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_post_id_categories_query_conflicting_should_return_badrequest(setup_each):
    print("Running test_post_id_categories_query_conflicting_should_return_badrequest")
    modify_category = {"title": "Never seen before title"}
    res = httpx.post(
        categories_url + "/" + test_categories[0]["id"] + "?id=99999",
        json=modify_category,
    )
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_post_id_categories_modifyid_should_return_categorymodified(setup_each):
    print("Running test_post_id_categories_modifyid_should_return_categorymodified")
    modify_category = {"id": "32", "title": "Never seen before title"}
    res = httpx.post(
        categories_url + "/" + test_categories[0]["id"], json=modify_category
    )
    modify_category.update({"description": test_categories[0]["description"]})
    assert res.status_code == 200
    assert res.json() == modify_category


def test_post_categories_id_titleinexistant_should_return_error(setup_each):
    print("Running test_post_categories_id_titleinexistant_should_return_error")
    new_category = {"description": "Never seen before description"}
    res = httpx.post(categories_url + "/" + test_categories[0]["id"], json=new_category)
    errorMessage = {"errorMessages": ["title : field is mandatory"]}
    assert res.status_code == 400
    assert res.json() == errorMessage


def test_put_id_categories_titlefield_should_return_categorymodified(setup_each):
    print("Running test_put_id_categories_titlefield_should_return_categorymodified")
    modify_category = {"title": "Never seen before title"}
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"], json=modify_category
    )
    modify_category.update(
        {
            "id": test_categories[0]["id"],
            "description": test_categories[0]["description"],
        }
    )
    assert res.status_code == 200
    assert res.json() == modify_category


def test_put_id_categories_conflictid_should_return_badrequest(setup_each):
    print("Running test_put_id_categories_conflictid_should_return_badrequest")
    modify_category = {
        "id": int(test_categories[1]["id"]),
        "title": "Never seen before title",
    }
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"], json=modify_category
    )
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_put_id_categories_query_conflicting_should_return_badrequest(setup_each):
    print("Running test_put_id_categories_query_conflicting_should_return_badrequest")
    modify_category = {"title": "Never seen before title"}
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"] + "?id=99999",
        json=modify_category,
    )
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_put_id_categories_modifyid_should_return_categorymodified(setup_each):
    print("Running test_put_id_categories_modifyid_should_return_categorymodified")
    modify_category = {"id": "99999", "title": "Never seen before title"}
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"], json=modify_category
    )
    modify_category.update({"description": test_categories[0]["description"]})
    assert res.status_code == 200
    assert res.json() == modify_category


def test_delete_categories_query_conflicting_should_return_400(setup_each):
    print("Running test_delete_categories_query_conflicting_should_return_400")
    res = httpx.delete(categories_url + "/" + test_categories[0]["id"] + "?id=99999")
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()
