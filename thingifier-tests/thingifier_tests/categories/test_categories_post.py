import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
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


def test_post_categories_withid_should_return_error(setup_each):
    print("Running test_post_categories_withid_should_return_error")
    new_category = {
        "id": 23,
        "title": "Never seen before title",
        "description": "Never seen before description",
    }
    res = httpx.post(categories_url, json=new_category)
    errorMessage = {
        "errorMessages": [
            "Invalid Creation: Failed Validation: Not allowed to create with id"
        ]
    }
    assert res.status_code == 400
    assert res.json() == errorMessage


def test_post_categories_titleonly_should_return_categorycreated(setup_each):
    print("Running test_post_categories_titleonly_should_return_categorycreated")
    new_category = {"title": "A title"}
    res = httpx.post(categories_url, json=new_category)
    new_category.update({"description": ""})
    received = res.json()
    received.pop("id")
    assert res.status_code == 201
    assert received == new_category


def test_post_categories_titleinexistant_should_return_error(setup_each):
    print("Running test_post_categories_titleinexistant_should_return_error")
    new_category = {"description": "Never seen before description"}
    res = httpx.post(categories_url, json=new_category)
    errorMessage = {"errorMessages": ["title : field is mandatory"]}
    assert res.status_code == 400
    assert res.json() == errorMessage


def test_post_categories_xml(setup_each):
    print("Running test_post_categories_xml")
    xml_data = """
        <category>
            <title>titlee</title>
            <description>description</description>
        </category>
    """
    res = httpx.post(categories_url, headers=XML_HEADERS, data=xml_data)
    resJson = xmltodict.parse(res.content)
    assert res.status_code == 201
    resJson["category"].pop("id")
    assert resJson["category"] == {"title": "titlee", "description": "description"}


def test_post_categories_malformed_json(setup_each):
    print("Running test_post_categories_malformed_json")
    new_category = """{
        "title": "Never seen before title
        "description": "Never seen before description",
    }"""
    res = httpx.post(categories_url, data=new_category)
    actual = new_category
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()


def test_post_categories_malformed_xml(setup_each):
    print("Running test_post_categories_malformed_xml")
    new_category = """
        <category>
            <titleitlee</title
            <description>description</description>
        </category>"""
    res = httpx.post(categories_url, data=new_category)
    actual = new_category
    assert res.status_code == 400
    assert "errorMessages" in res.json().keys()
