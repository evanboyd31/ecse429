import pytest
import httpx
from thingifier_tests.test_common import *
import os

categories = []
#Runs once before all tests in the module
@pytest.fixture(scope="module")
def setup_module():
    print("Setting up before all tests in the categories module")
    categories = httpx.get(url_header + "categories").json()['categories']
    remove_all()
    print(os.getcwd())
    print(categories)
    for category in categories:
        print("hey")
        print(category)
        httpx.post(url_header + "categories/" + category[id], json = category)
    categories = httpx.post(url_header + "categories")
    print(categories.json())
    expected : dict = {'todos': [{'id': '2', 'title': 'file paperwork', 'doneStatus': 'false', 'description': '', 'tasksof': [{'id': '1'}]}, {'id': '1', 'title': 'scan paperwork', 'doneStatus': 'false', 'description': '', 'categories': [{'id': '1'}], 'tasksof': [{'id': '1'}]}]}
    # assert response.json() == expected 
    yield
    print("Tearing down after all tests in the categories module")

#Runs before each test
@pytest.fixture()
def setup_each():
    print("Setting up before each test")
    yield
    print("Tearing down after each test")

def test_example_1(setup_module, setup_each):
    print("Running test_example_1")
    assert True

def test_example_2(setup_module, setup_each):
    print("Running test_example_2")
    assert True