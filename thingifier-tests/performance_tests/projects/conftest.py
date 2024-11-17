import time
import pytest
import httpx
import thingifier_tests.conftest as common
import xmltodict

projects_url = "http://localhost:4567/projects"

XML_HEADERS = {"Content-Type": "application/xml", "Accept": "application/xml"}

test_projects = [
    {
        "title": "test title 1",
        "completed": False,
        "active": False,
        "description": "test description 1",
    }
]


# Runs before each test
@pytest.fixture()
def before_each():
    if common.make_sure_system_ready() != True:
        print("The system is not ready to be tested.")
        assert False
    common.remove_all()
    for project in test_projects:
        project.pop("id", None)
        response = httpx.post(projects_url, json=project)

        assert response.status_code == 201

        project.update({"id": response.json().get("id")})
        assert_project(expected=project, actual=response.json(), check_id=True)

    start_time = time.time()  # Record the start time
    
    yield
    
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Test execution time: {execution_time:.2f} seconds")


def assert_project(expected, actual, check_id=False):
    """
    method for asserting that two json representations of projects are equal
    """

    if check_id:
        assert actual.get("id") == expected.get("id", "")

    assert (
        actual.get("title") if actual.get("title") is not None else ""
    ) == expected.get("title", "")
    assert actual.get("completed") == (
        "true" if expected.get("completed") in [True, "true"] else "false"
    )
    assert actual.get("active") == (
        "true" if expected.get("active") in [True, "true"] else "false"
    )
    assert (
        actual.get("description") if actual.get("description") is not None else ""
    ) == expected.get("description", "")


def xml_to_json(xml_content):
    """
    Convert XML content to a JSON-like dictionary structure using xmltodict.
    Handles cases for successful responses and errors.
    """
    if not xml_content:
        return {}

    data_dict = xmltodict.parse(xml_content)

    if "errorMessages" in data_dict:
        errors = data_dict["errorMessages"].get("errorMessage", [])

        if not isinstance(errors, list):
            errors = [errors]
        return {"errorMessages": errors}

    projects = []
    if "projects" in data_dict:
        projects = (
            data_dict["projects"].get("project", [])
            if data_dict["projects"] is not None
            else []
        )

        if not isinstance(projects, list):
            projects = [projects]

        return {"projects": projects}

    return data_dict
