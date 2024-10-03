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
    common.remove_all()
    for project in test_projects:
        project.pop("id", None)
        response = httpx.post(projects_url, json=project)

        assert response.status_code == 201

        project.update({"id": response.json().get("id")})
        assert_project(expected=project, actual=response.json(), check_id=True)


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

    # Convert XML to an OrderedDict
    data_dict = xmltodict.parse(xml_content)

    # Check for error indicators in the parsed data
    if "errorMessages" in data_dict:
        errors = data_dict["errorMessages"].get("errorMessage", [])

        # Ensure projects is a list
        if not isinstance(
            errors, list
        ):  # If there's only one project, convert to a list
            errors = [errors]
        return {"errorMessages": errors}  # Handle the error case

    # Initialize projects as an empty list
    projects = []

    # Check if 'projects' is in the parsed data
    if "projects" in data_dict:
        projects = (
            data_dict["projects"].get("project", [])
            if data_dict["projects"] is not None
            else []
        )

        # Ensure projects is a list
        if not isinstance(
            projects, list
        ):  # If there's only one project, convert to a list
            projects = [projects]

        return {"projects": projects}

    return data_dict
