import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import xmltodict


# JSON BODY AND RESPONSE
def test_get_categories_should_return_all_categories(setup_each):
    print("Running test_get_categories_should_return_all_categories")
    res = httpx.get(categories_url)
    actual = test_categories
    assert res.status_code == 200
    assert contain_same_categories(res.json()["categories"], actual)


def test_get_categories_xml(setup_each):
    print("Running test_get_categories_xml")
    res = httpx.get(categories_url, headers=XML_HEADERS)
    resJson = xmltodict.parse(res.content)
    assert res.status_code == 200
    assert contain_same_categories(resJson["categories"]["category"], test_categories)

def test_get_categories_query_id_should_return_corresponding_categories(setup_each):
    print("Running test_get_categories_query_id_should_return_corresponding_categories")
    res = httpx.get(categories_url + "?id=" + test_categories[0]["id"])
    actual = [test_categories[0]]
    assert res.status_code == 200
    assert contain_same_categories(res.json()["categories"], actual)

def test_get_categories_query_id_should_return_corresponding_categories_xml(setup_each):
    print("Running test_get_categories_query_id_should_return_corresponding_categories_xml")
    res = httpx.get(categories_url + "?id=" + test_categories[0]["id"], headers=XML_HEADERS)
    actual = [test_categories[0]]
    assert res.status_code == 200
    resJson = xmltodict.parse(res.content)
    assert contain_same_categories([resJson["categories"]["category"]], actual)


def test_get_categories_query_title_should_return_corresponding_categories(setup_each):
    print(
        "Running test_get_categories_query_title_should_return_corresponding_categories"
    )
    res = httpx.get(categories_url + "?title=" + test_categories[0]["title"])
    actual = [test_categories[0], test_categories[1]]
    assert res.status_code == 200
    assert contain_same_categories(res.json()["categories"], actual)

def test_get_categories_query_title_should_return_corresponding_categories_xml(setup_each):
    print(
        "Running test_get_categories_query_title_should_return_corresponding_categories_xml"
    )
    res = httpx.get(categories_url + "?title=" + test_categories[0]["title"], headers=XML_HEADERS)
    actual = [test_categories[0], test_categories[1]]
    assert res.status_code == 200
    resJson = xmltodict.parse(res.content)
    assert contain_same_categories(resJson["categories"]['category'], actual)

def test_get_categories_query_description_should_return_corresponding_categories(
    setup_each,
):
    print(
        "Running test_get_categories_query_description_should_return_corresponding_categories"
    )
    res = httpx.get(
        categories_url + "?description=" + test_categories[0]["description"]
    )
    actual = [test_categories[0]]
    assert res.status_code == 200
    assert contain_same_categories(res.json()["categories"], actual)

def test_get_categories_query_description_should_return_corresponding_categories_xml(
    setup_each,
):
    print(
        "Running test_get_categories_query_description_should_return_corresponding_categories_xml"
    )
    res = httpx.get(
        categories_url + "?description=" + test_categories[0]["description"], headers=XML_HEADERS
    )
    actual = [test_categories[0]]
    assert res.status_code == 200
    resJson = xmltodict.parse(res.content)
    assert contain_same_categories([resJson["categories"]['category']], actual)


def test_get_categories_query_all_should_return_corresponding_categories(setup_each):
    print(
        "Running test_get_categories_query_all_should_return_corresponding_categories"
    )
    res = httpx.get(
        categories_url
        + "?id="
        + test_categories[0]["id"]
        + "&title="
        + test_categories[0]["title"]
        + "&description="
        + test_categories[0]["description"]
    )
    actual = [test_categories[0]]
    assert res.status_code == 200
    assert contain_same_categories(res.json()["categories"], actual)

def test_get_categories_query_all_should_return_corresponding_categories_xml(setup_each):
    print(
        "Running test_get_categories_query_all_should_return_corresponding_categories_xml"
    )
    res = httpx.get(
        categories_url
        + "?id="
        + test_categories[0]["id"]
        + "&title="
        + test_categories[0]["title"]
        + "&description="
        + test_categories[0]["description"], headers=XML_HEADERS
    )
    actual = [test_categories[0]]
    assert res.status_code == 200
    resJson = xmltodict.parse(res.content)
    assert contain_same_categories([resJson["categories"]['category']], actual)

def test_get_categories_query_nonexistent_should_return_empty(setup_each):
    print("Running test_get_categories_query_nonexistent_should_return_empty")
    res = httpx.get(categories_url + "?id=99999")
    actual = []
    assert res.status_code == 200
    assert contain_same_categories(res.json()["categories"], actual)

def test_get_categories_query_nonexistent_should_return_empty_xml(setup_each):
    print("Running test_get_categories_query_nonexistent_should_return_empty_xml")
    res = httpx.get(categories_url + "?id=99999", headers=XML_HEADERS)
    actual = None
    assert res.status_code == 200
    resJson = xmltodict.parse(res.content)
    assert resJson["categories"] == actual

def test_get_categories_extendedendpoint_should_return_notfound(setup_each):
    print("Running test_get_categories_extendedendpoint_should_return_notfound")
    res = httpx.get(categories_url + "/")
    assert res.status_code == 404

def test_get_categories_extendedendpoint_should_return_notfound_xml(setup_each):
    print("Running test_get_categories_extendedendpoint_should_return_notfound_xml")
    res = httpx.get(categories_url + "/", headers=XML_HEADERS)
    assert res.status_code == 404
