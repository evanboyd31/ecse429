import pytest
import httpx
import thingifier_tests.test_common as common


projects_url = "http://localhost:4567/projects"

test_projects = [
    {
        "title": "test title 1",
        "completed": False,
        "active": False,
        "description": "test description 1"
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
      
      project.update({
          "id": response.json().get("id")
      })
      assert_project(expected=project, actual=response.json(), check_id=True)
    
def assert_project(expected, actual , check_id=False):
  """
  method for asserting that two json representations of projects are equal
  """
  
  if check_id:
    assert actual.get("id") == expected.get("id", "")
    
  assert actual.get("title") == expected.get("title", "")
  assert actual.get("completed") == ("true" if expected.get("completed", False) else "false")
  assert actual.get("active") == ("true" if expected.get("active", False) else "false")
  assert actual.get("description") == expected.get("description", "") 