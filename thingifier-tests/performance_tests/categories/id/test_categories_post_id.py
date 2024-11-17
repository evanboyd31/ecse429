import httpx
from performance_tests.conftest import *
from performance_tests.categories.conftest import *
import xmltodict


# JSON BODY AND RESPONSE
def test_post_id_categories_allfields_should_return_categorymodified(setup_each):
    print("Running test_post_id_categories_allfields_should_return_categorymodified")
    modify_category = {
        "title": "Never seen before title",
        "description": "Never seen before description",
    }
    res = httpx.post(
        categories_url + "/" + test_categories[0]["id"], json=modify_category
    )
    modify_category.update({"id": test_categories[0]["id"]})
    assert res.status_code == 200
    assert res.json() == modify_category
