import httpx
from performance_tests.projects.conftest import *


def test_id_delete_project_should_delete_project_with_that_id_json(before_each):
    id = test_projects[0].get("id")
    response = httpx.delete(f"{projects_url}/{id}")

    assert response.status_code == 200
    assert not response.content

    # ensure no projects exist in the system after deleting this project
    response = httpx.get(projects_url)
    assert len(response.json().get("projects")) == 0
