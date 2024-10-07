import httpx
from thingifier_tests.projects.conftest import *


def test_put_project_filter_by_title_json(before_each):
    test_project = test_projects[0]

    new_data = {"title": "New title"}

    response = httpx.put(
        f"{projects_url}?title={test_project.get("title")}", json=new_data
    )

    # ensure method is not allowed and that the existing project remains unchanged
    assert response.status_code == 405

    response = httpx.get(projects_url)
    assert len(response.json().get("projects")) == 1

    assert_project(
        expected=test_project, actual=response.json().get("projects")[0], check_id=True
    )


def test_put_project_filter_by_title_xml(before_each):
    test_project = test_projects[0]

    xml_data = """
        <project>
  <active>false</active>
  <description>description</description>
  <completed>false</completed>
  <title>anotherTitle</title>
</project>
    """

    response = httpx.put(
        f"{projects_url}?title={test_project.get("title")}",
        data=xml_data,
        headers=XML_HEADERS,
    )

    # ensure method is not allowed and that the existing project remains unchanged
    assert response.status_code == 405

    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert len(xml_to_json(response.content).get("projects")) == 1

    assert_project(
        expected=test_project,
        actual=xml_to_json(response.content).get("projects")[0],
        check_id=True,
    )
