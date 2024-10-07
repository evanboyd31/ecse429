import httpx
from thingifier_tests.projects.conftest import *


def test_get_projects_should_return_all_projects_json(before_each):
    """
    Test to get projects from the /projects API endpoint
    """

    response = httpx.get(projects_url)
    assert response.status_code == 200
    list_of_projects = response.json().get("projects")

    for test_project in test_projects:
        # response booleans are represented as strings, so make a copy of them
        expected_project = test_project.copy()
        expected_project["completed"] = (
            "true" if expected_project["completed"] else "false"
        )
        expected_project["active"] = "true" if expected_project["active"] else "false"

        assert expected_project in list_of_projects


def test_get_projects_should_return_all_projects_xml(before_each):
    """
    Test to get projects from the /projects API endpoint
    """

    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert response.status_code == 200
    list_of_projects = xml_to_json(response.content).get("projects")

    for i, test_project in enumerate(test_projects):
        # response booleans are represented as strings, so make a copy of the
        assert_project(
            expected=test_project, actual=list_of_projects[i], check_id=False
        )


def test_get_project_filter_by_title_should_return_projects_with_that_title_json(
    before_each,
):
    project = test_projects[0]

    response = httpx.get(f"{projects_url}?title={project.get("title")}")

    assert response.status_code == 200
    assert len(response.json().get("projects", [])) == 1

    response_project = response.json().get("projects")[0]

    assert_project(expected=project, actual=response_project, check_id=True)


def test_get_project_filter_by_title_should_return_projects_with_that_title_xml(
    before_each,
):
    project = test_projects[0]

    response = httpx.get(
        f"{projects_url}?title={project.get("title")}", headers=XML_HEADERS
    )

    assert response.status_code == 200
    list_of_projects = xml_to_json(response.content).get("projects")
    assert len(list_of_projects) == 1

    response_project = list_of_projects[0]

    assert_project(expected=project, actual=response_project, check_id=True)


def test_get_project_filter_by_description_should_return_projects_with_that_description_json(
    before_each,
):
    project = test_projects[0]

    response = httpx.get(f"{projects_url}?description={project.get("description")}")

    assert response.status_code == 200
    assert len(response.json().get("projects", [])) == 1

    response_project = response.json().get("projects")[0]

    assert_project(expected=project, actual=response_project, check_id=True)


def test_get_project_filter_by_description_should_return_projects_with_that_description_xml(
    before_each,
):
    project = test_projects[0]

    response = httpx.get(
        f"{projects_url}?description={project.get("description")}", headers=XML_HEADERS
    )

    assert response.status_code == 200
    list_of_projects = xml_to_json(response.content).get("projects")
    assert len(list_of_projects) == 1

    response_project = list_of_projects[0]

    assert_project(expected=project, actual=response_project, check_id=True)


def test_get_project_filter_by_id_should_return_project_with_that_id_json(before_each):
    project = test_projects[0]
    response = httpx.get(f"{projects_url}?id={project.get("id")}")

    assert response.status_code == 200
    assert len(response.json().get("projects", [])) == 1

    response_project = response.json().get("projects")[0]

    assert_project(expected=project, actual=response_project, check_id=True)


def test_get_project_filter_by_id_should_return_project_with_that_id_xml(before_each):
    project = test_projects[0]
    response = httpx.get(f"{projects_url}?id={project.get("id")}", headers=XML_HEADERS)

    assert response.status_code == 200
    list_of_projects = xml_to_json(response.content).get("projects")
    assert len(list_of_projects) == 1

    response_project = list_of_projects[0]

    assert_project(expected=project, actual=response_project, check_id=True)


def test_get_project_filter_by_multiple_params_should_return_projects_that_match_all_filters_json(
    before_each,
):
    project = test_projects[0]

    response = httpx.get(
        f"{projects_url}?id={project.get("id")}&description={project.get("description")}"
    )

    assert response.status_code == 200
    assert len(response.json().get("projects", [])) == 1

    response_project = response.json().get("projects")[0]

    assert_project(expected=project, actual=response_project, check_id=True)


def test_get_project_filter_by_multiple_params_should_return_projects_that_match_all_filters_xml(
    before_each,
):
    project = test_projects[0]

    response = httpx.get(
        f"{projects_url}?id={project.get("id")}&description={project.get("description")}",
        headers=XML_HEADERS,
    )

    assert response.status_code == 200
    list_of_projects = xml_to_json(response.content).get("projects")
    assert len(list_of_projects) == 1

    response_project = list_of_projects[0]

    assert_project(expected=project, actual=response_project, check_id=True)
