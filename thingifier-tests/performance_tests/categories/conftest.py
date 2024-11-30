import pytest
from performance_tests.conftest import *

test_categories = [
    {"title": "A title", "description": "The best description"},
    {"title": "A title", "description": "A different description"},
    {"title": "Another title", "description": "Second best description"},
]
categories_url = url_header + "categories"

XML_HEADERS = {"Content-Type": "application/xml", "Accept": "application/xml"}


# Runs before each test
@pytest.fixture()
def setup_each():
    print("Setting up before each categories test")
    if make_sure_system_ready() != True:
        print("The system is not ready to be tested.")
        assert False

    # Create a few instances that will be used in tests
    for i in range(len(test_categories)):
        response = httpx.post(url_header + "categories", json=test_categories[i]).json()
        test_categories[i].update({"id": response["id"]})

    start_time = time.time()  # Record the start time

    yield

    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Test execution time: {execution_time:.2f} seconds")

    print("Tearing down after each categories test")
    remove_all()

    # Clear out the Ids
    for i in range(len(test_categories)):
        del test_categories[i]["id"]


def contain_same_categories(categories_list1, categories_list2):
    if len(categories_list1) != len(categories_list1):
        return False
    for e in categories_list1:
        if e not in categories_list2:
            return False
    return True
