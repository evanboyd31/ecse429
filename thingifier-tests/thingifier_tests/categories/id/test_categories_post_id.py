import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import xmltodict

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

def test_post_id_categories_nonexistent_should_return_notfound(setup_each):
    print("Running test_post_id_categories_nonexistent_should_return_notfound")
    modify_category = {"title":"Never seen before title"}
    res = httpx.post(categories_url + '/99999', json=modify_category)
    errorMessage = {"errorMessages":[f"No such category entity instance with GUID or ID 99999 found"]}
    assert res.status_code == 404
    assert res.json() == errorMessage

def test_post_categories_id_titleempty_should_return_error(setup_each):
    print("Running test_post_categories_typeerror_should_return_error")
    new_category = {"title": "", "description": "Never seen before description"}
    res = httpx.post(categories_url + '/' + test_categories[0]['id'], json=new_category)
    errorMessage = {"errorMessages":["Failed Validation: title : can not be empty"]}
    assert res.status_code == 400
    assert res.json() == errorMessage

def test_post_categories_id_xml(setup_each):
    print("test_get_categories_xml")
    xml_data = '''
        <category>
            <title>titlee</title>
            <description>description</description>
        </category>
    '''
    res = httpx.post(categories_url + '/' + test_categories[0]["id"], headers=XML_HEADERS, data=xml_data)
    resJson = xmltodict.parse(res.content)
    assert res.status_code == 200
    resJson['category'].pop("id")
    assert resJson['category'] == {"title":"titlee", "description":"description"}
