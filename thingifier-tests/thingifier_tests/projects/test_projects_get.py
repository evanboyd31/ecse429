import httpx
from thingifier_tests.projects.conftest import *

def test_get_projects_json(before_each):
    """
    Test to get projects from the /projects API endpoint
    """
    
    response = httpx.get(projects_url)
    assert response.status_code == 200
    list_of_projects = response.json().get("projects")
    
    for test_project in test_projects:
      # response booleans are represented as strings, so make a copy of them
      expected_project = test_project.copy()
      expected_project['completed'] = "true" if expected_project["completed"] else "false"
      expected_project['active'] = "true" if expected_project["active"] else "false"
      
      assert expected_project in list_of_projects
      
def test_get_project_filter_by_title_json(before_each):
  project = test_projects[0]
  
  response = httpx.get(f"{projects_url}?title={project.get("title")}")
  
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 1
  
  response_project = response.json().get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)
  
def test_get_project_filter_by_description_json(before_each):
  project = test_projects[0]
  
  response = httpx.get(f"{projects_url}?description={project.get("description")}")
  
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 1
  
  response_project = response.json().get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)

def test_get_project_filter_by_id_json(before_each):
  project = test_projects[0]
  response = httpx.get(f"{projects_url}?id={project.get("id")}")
  
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 1
  
  response_project = response.json().get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)
  
def test_get_project_filter_by_multiple_params(before_each):
  project = test_projects[0]
  
  response = httpx.get(f"{projects_url}?id={project.get("id")}&description={project.get("description")}")
  
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 1
  
  response_project = response.json().get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)