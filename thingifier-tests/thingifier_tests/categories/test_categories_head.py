import httpx
from thingifier_tests.conftest import *
from thingifier_tests.categories.conftest import *
import os

# JSON BODY AND RESPONSE
def test_head_categories_should_return_200(setup_each):
    print("Running test_head_categories_should_return_200")
    res = httpx.head(categories_url)
    assert res.status_code == 200
