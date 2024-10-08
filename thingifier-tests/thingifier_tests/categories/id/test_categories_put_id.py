import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import xmltodict


# JSON BODY AND RESPONSE
def test_put_id_categories_allfields_should_return_categorymodified(setup_each):
    print("Running test_put_id_categories_allfields_should_return_categorymodified")
    modify_category = {
        "title": "Never seen before title",
        "description": "Never seen before description",
    }
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"], json=modify_category
    )
    modify_category.update({"id": test_categories[0]["id"]})
    assert res.status_code == 200
    assert res.json() == modify_category


def test_put_categories_id_xml(setup_each):
    print("Running test_put_categories_id_xml")
    xml_data = """
        <category>
            <title>titlee</title>
            <description>description</description>
        </category>
    """
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"],
        headers=XML_HEADERS,
        data=xml_data,
    )
    resJson = xmltodict.parse(res.content)
    assert res.status_code == 200
    resJson["category"].pop("id")
    assert resJson["category"] == {"title": "titlee", "description": "description"}


def test_put_id_categories_nonexistent_should_return_notfound(setup_each):
    print("Running test_put_id_categories_nonexistent_should_return_notfound")
    modify_category = {"title": "Never seen before title"}
    res = httpx.put(categories_url + "/99999", json=modify_category)
    errorMessage = {"errorMessages": [f"Invalid GUID for 99999 entity category"]}
    assert res.status_code == 404
    assert res.json() == errorMessage


def test_put_id_categories_nonexistent_should_return_notfound_xml(setup_each):
    print("Running test_put_id_categories_nonexistent_should_return_notfound_xml")
    modify_category = {"title": "Never seen before title"}
    xml_data = """
    <category>
        <title>Never seen before title</title>
    </category>"""
    res = httpx.put(categories_url + "/99999", headers=XML_HEADERS, data=xml_data)
    errorMessage = "Invalid GUID for 99999 entity category"
    assert res.status_code == 404
    resJson = xmltodict.parse(res.content)
    assert resJson["errorMessages"]["errorMessage"] == errorMessage


def test_put_categories_id_titleinexistant_should_return_error(setup_each):
    print("Running test_put_categories_id_titleinexistant_should_return_error")
    new_category = {"description": "Never seen before description"}
    res = httpx.put(categories_url + "/" + test_categories[0]["id"], json=new_category)
    errorMessage = {"errorMessages": ["title : field is mandatory"]}
    assert res.status_code == 400
    assert res.json() == errorMessage


def test_put_categories_id_titleinexistant_should_return_error_xml(setup_each):
    print("Running test_put_categories_id_titleinexistant_should_return_error_xml")
    xml_data = """
    <category>
        <description>Never seen before description</description>
    </category>
    """
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"],
        headers=XML_HEADERS,
        data=xml_data,
    )
    errorMessage = "title : field is mandatory"
    assert res.status_code == 400
    resJson = xmltodict.parse(res.content)
    assert resJson["errorMessages"]["errorMessage"] == errorMessage


def test_put_categories_id_titleempty_should_return_error(setup_each):
    print("Running test_put_categories_id_titleempty_should_return_error")
    new_category = {"title": "", "description": "Never seen before description"}
    res = httpx.put(categories_url + "/" + test_categories[0]["id"], json=new_category)
    errorMessage = {"errorMessages": ["Failed Validation: title : can not be empty"]}
    assert res.status_code == 400
    assert res.json() == errorMessage


def test_put_categories_id_titleempty_should_return_error_xml(setup_each):
    print("Running test_put_categories_id_titleempty_should_return_error_xml")
    xml_data = """
    <category>
        <title></title>
        <description>Never seen before description</description>
    </category>
    """
    res = httpx.put(
        categories_url + "/" + test_categories[0]["id"],
        headers=XML_HEADERS,
        data=xml_data,
    )
    errorMessage = "Failed Validation: title : can not be empty"
    assert res.status_code == 400
    resJson = xmltodict.parse(res.content)
    assert resJson["errorMessages"]["errorMessage"] == errorMessage


def test_put_id_categories_titlefield_actually_return_categorymodified(setup_each):
    print("Running test_put_id_categories_titlefield_actually_return_categorymodified")
    modify_category = {"title": "Never seen before title"}
    modify_category.update({"description": test_categories[0]["description"]})
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
