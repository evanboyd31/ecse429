import httpx
from performance_tests.projects.conftest import *


def test_id_post_project_should_update_project_json(before_each):
    test_project = test_projects[0]

    id = test_project.get("id")

    updated_project = {
        "title": "updated title",
        "completed": True,
        "active": True,
        "description": "updated description",
    }
    response = httpx.put(f"{projects_url}/{id}", json=updated_project)

    assert response.status_code == 200
    response_project = response.json()

    updated_project.update({"id": id})
    assert_project(expected=updated_project, actual=response_project, check_id=True)

    # ensure only a single project exists in the system
    response = httpx.get(projects_url)
    assert response.status_code == 200
    assert len(response.json().get("projects", [])) == 1
