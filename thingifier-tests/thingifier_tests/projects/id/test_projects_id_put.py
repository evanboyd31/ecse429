import httpx
from thingifier_tests.projects.conftest import *

def test_id_put_project_with_string_boolean(before_each):
  test_project = test_projects[0]
  new_data = {
    "title": "new title",
    "completed": "true",
    "active": "true",
    "description": "new description"
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # ensure we get error message and that none of the fields are updated
  assert response.status_code == 400
  assert response.json() == {"errorMessages": ["Failed Validation: completed should be BOOLEAN, active should be BOOLEAN"]}
  
  response = httpx.get(projects_url)
  assert len(response.json().get("projects")) == 1
  
  assert_project(expected=test_project, actual=response.json().get("projects")[0], check_id=True)
  
def test_id_put_project_with_valid_boolean(before_each):
  test_project = test_projects[0]
  new_data = {
    "title": "new title",
    "completed": True,
    "active": True,
    "description": "new description"
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # ensure we update successfully and fields are updated correctly
  assert response.status_code == 200
  assert_project(expected=new_data, actual=response.json())
  
def test_id_put_project_different_int_id(before_each):
  test_project = test_projects[0]
  new_data = {
    "id": 200,
    "title": "new title",
    "completed": True,
    "active": True,
    "description": "new description"
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # ensure we update successfully and fields are updated correctly
  assert response.status_code == 200
  assert_project(expected=new_data, actual=response.json())
  
def test_id_put_project_different_string_id(before_each):
  test_project = test_projects[0]
  new_data = {
    "id": "200"
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # ensure error is thrown and existing project is not updated
  assert response.status_code == 400
  assert response.json() == {"errorMessages":["Failed Validation: id should be ID"]}
  
  response = httpx.get(projects_url)
  assert len(response.json().get("projects")) == 1
  assert_project(expected=test_project, actual=response.json().get("projects")[0], check_id=True)
  
def test_id_put_project_different_boolean_id(before_each):
  test_project = test_projects[0]
  new_data = {
    "id": True
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # ensure error is thrown and existing project is not updated
  assert response.status_code == 400
  assert response.json() == {"errorMessages":["Failed Validation: id should be ID"]}
  
  response = httpx.get(projects_url)
  assert len(response.json().get("projects")) == 1
  assert_project(expected=test_project, actual=response.json().get("projects")[0], check_id=True)
  