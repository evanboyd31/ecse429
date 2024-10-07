import httpx
from thingifier_tests.projects.conftest import *


def test_id_delete_project_should_delete_project_with_that_id_json(before_each):
    id = test_projects[0].get("id")
    response = httpx.delete(f"{projects_url}/{id}")

    assert response.status_code == 200
    assert not response.content

    # ensure no projects exist in the system after deleting this project
    response = httpx.get(projects_url)
    assert len(response.json().get("projects")) == 0


def test_id_delete_project_should_delete_project_with_that_id_xml(before_each):
    id = test_projects[0].get("id")
    response = httpx.delete(f"{projects_url}/{id}", headers=XML_HEADERS)

    assert response.status_code == 200
    assert not response.content

    # ensure no projects exist in the system after deleting this project
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert len(xml_to_json(response.content).get("projects")) == 0


def test_id_delete_project_invalid_id_should_not_delete_project_json(before_each):
    id = -1
    # ensure the project with id does not exist
    response = httpx.get(f"{projects_url}/{id}")
    assert response.status_code == 404
    assert response.json() == {
        "errorMessages": [f"Could not find an instance with projects/{id}"]
    }

    # for reasons, the error messages for get and delete are different when the project doesn't exist
    response = httpx.delete(f"{projects_url}/{id}")
    assert response.status_code == 404
    assert response.json() == {
        "errorMessages": [f"Could not find any instances with projects/{id}"]
    }

    # ensure the single project still exists in the system
    response = httpx.get(projects_url)
    assert len(response.json().get("projects")) == 1


def test_id_delete_project_invalid_id_should_not_delete_project_xml(before_each):
    id = -1
    # ensure the project with id does not exist
    response = httpx.get(f"{projects_url}/{id}", headers=XML_HEADERS)
    assert response.status_code == 404
    assert xml_to_json(response.content) == {
        "errorMessages": [f"Could not find an instance with projects/{id}"]
    }

    # for reasons, the error messages for get and delete are different when the project doesn't exist
    response = httpx.delete(f"{projects_url}/{id}", headers=XML_HEADERS)
    assert response.status_code == 404
    assert xml_to_json(response.content) == {
        "errorMessages": [f"Could not find any instances with projects/{id}"]
    }

    # ensure the single project still exists in the system
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert len(xml_to_json(response.content).get("projects")) == 1
