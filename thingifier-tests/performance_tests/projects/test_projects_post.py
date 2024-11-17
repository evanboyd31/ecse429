import httpx
from performance_tests.projects.conftest import *


def test_post_project_valid_boolean_should_create_project_json(before_each):
    valid_project = {
        "title": "title",
        "completed": False,
        "active": True,
        "description": "description",
    }

    response = httpx.post(projects_url, json=valid_project)

    assert response.status_code == 201
    response_json = response.json()

    # assert that the two projects are equal (except for their IDs)
    assert_project(expected=valid_project, actual=response_json, check_id=False)
