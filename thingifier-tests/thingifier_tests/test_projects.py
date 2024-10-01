import pytest
import httpx
from thingifier_tests.test_common import *

url: str = "http://localhost:4567/"
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
    remove_all()
    for project in test_projects:
      response = httpx.post(f"{url}projects", json=project)
      
      if response.status_code == 201:
        project.update({
            "id": response.json().get("id")
        })
    
    yield
    remove_all()

def test_get_projects(before_each):
    """
    Test to get projects from the /projects API endpoint
    """
    response = httpx.get(f"{url}projects")
    assert response.status_code == 200
    list_of_projects = response.json().get("projects")
    
    for test_project in test_projects:
      # response booleans are represented as strings, so make a copy of them
      expected_project = test_project.copy()
      expected_project['completed'] = "true" if expected_project["completed"] else "false"
      expected_project['active'] = "true" if expected_project["active"] else "false"
      
      assert expected_project in list_of_projects

def test_post_project_invalid_boolean(before_each):
    invalid_project = {
      "title": "title",
      "completed": "false",
      "active": "true",
      "description": "description"
    }
    
    response = httpx.post(f"{url}projects", json=invalid_project)
    assert response.status_code == 400
    assert response.json() == {"errorMessages": ["Failed Validation: completed should be BOOLEAN, active should be BOOLEAN"]}

def test_post_project_valid_boolean(before_each):
  valid_project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }  

  response = httpx.post(f"{url}projects", json=valid_project)
  
  assert response.status_code == 201
  
  response_json = response.json()
  assert response_json.get("id")
  assert response_json.get("title") == valid_project.get("title")
  assert response_json.get("completed") == ("true" if valid_project.get("completed") else "false")
  assert response_json.get("active") == ("true" if valid_project.get("active") else "false")
  assert response_json.get("description") == valid_project.get("description")
  
def test_post_identical_project(before_each):
  project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  } 
  
  response1 = httpx.post(f"{url}projects", json=project)
  
  assert response1.status_code == 201
  
  response1_json = response1.json()
  first_id = response1_json.get("id")
  
  assert first_id
  assert response1_json.get("title") == project.get("title")
  assert response1_json.get("completed") == ("true" if project.get("completed") else "false")
  assert response1_json.get("active") == ("true" if project.get("active") else "false")
  assert response1_json.get("description") == project.get("description") 
  
  # post the exact same project again and ensure that they have different IDs
  
  response2 = httpx.post(f"{url}projects", json=project)
  
  assert response2.status_code == 201
  
  response2_json = response2.json()
  second_id = response2_json.get("id")
  
  assert second_id
  assert first_id != second_id
  assert response2_json.get("title") == project.get("title")
  assert response2_json.get("completed") == ("true" if project.get("completed") else "false")
  assert response2_json.get("active") == ("true" if project.get("active") else "false")
  assert response2_json.get("description") == project.get("description") 
  
def test_post_project_with_id(before_each):
  project = {
      "id": 100,
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }
  
  response = httpx.post(f"{url}projects", json=project)
  
  assert response.status_code == 400
  assert response.json() == {"errorMessages": ["Invalid Creation: Failed Validation: Not allowed to create with id"]}
  
def test_post_project_with_new_id_put(before_each):
  project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }
  
  response = httpx.post(f"{url}projects", json=project)
  
  assert response.status_code == 201
  
  id = response.json().get("id")
  data = {
    "id": str(int(id) + 1)
  }
  
  response = httpx.post(f"{url}projects/{id}", json=data)
  assert response.status_code == 400
  assert response.json() == {"errorMessages":["Failed Validation: id should be ID"]}

def test_post_project_with_same_id_put(before_each):
  project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }
  
  response = httpx.post(f"{url}projects", json=project)
  
  assert response.status_code == 201
  
  id = response.json().get("id")
  data = {
    "id": id
  }
  response = httpx.post(f"{url_header}projects/{id}", json=data)
  
  assert response.status_code == 400
  assert response.json() == {"errorMessages":["Failed Validation: id should be ID"]}
  
def test_post_project_using_id(before_each):
  project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }
  
  response = httpx.post(f"{url}projects", json=project)
  
  assert response.status_code == 201
  
  id = response.json().get("id")
  data = {
    "title": f"Project {id}",
    "completed": True,
    "active": False
  }
  
  response = httpx.post(f"{url_header}projects/{id}", json=data)
  
  assert response.status_code == 200
  assert response.json().get("title") == data.get("title")
  assert response.json().get("completed") == ("true" if data.get("completed") else "false")
  assert response.json().get("active") == ("true" if data.get("active") else "false")
  
def test_delete_project_using_id(before_each):
  project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }
  
  response = httpx.post(f"{url}projects", json=project)
  
  assert response.status_code == 201
  
  id = response.json().get("id")
  
  # ensure 200 response and no response body
  response = httpx.delete(f"{url}projects/{id}")
  
  assert response.status_code == 200
  assert not response.content
  
  # ensure that an error occurs when we attempt to get the project with the id we just deleted
  
  response = httpx.get(f"{url}projects/{id}")
  assert response.status_code == 404
  assert response.json() == {"errorMessages":[f"Could not find an instance with projects/{id}"]}
  
def test_delete_project_using_invalid_id(before_each):
  id = -1
  # ensure the project with id does not exist
  response = httpx.get(f"{url}projects/{id}")
  assert response.status_code == 404
  assert response.json() == {"errorMessages":[f"Could not find an instance with projects/{id}"]}
  
  # for reasons, the error messages for get and delete are different when the project doesn't exist
  response = httpx.delete(f"{url}projects/{id}")
  assert response.status_code == 404
  assert response.json() == {"errorMessages":[f"Could not find any instances with projects/{id}"]}
  
def test_delete_all_projects(before_each):
  
  project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }
  
  response = httpx.post(f"{url}projects", json=project)
  
  assert response.status_code == 201
  
  id = response.json().get("id")
  
  # ensure method is not allowed and that the added project still exists
  response = httpx.delete(f"{url}projects")
  assert response.status_code == 405
  
  
  response = httpx.get(f"{url}projects")

  assert response.status_code == 200
  assert len(response.json().get("projects")) == 1
  
  response_project = response.json().get("projects")[0]

  assert response_project.get("id") == id
  assert response_project.get("title") == project.get("title")
  assert response_project.get("completed") == ("true" if project.get("completed") else "false")
  assert response_project.get("active") == ("true" if project.get("active") else "false")
  assert response_project.get("description") == project.get("description")
  
