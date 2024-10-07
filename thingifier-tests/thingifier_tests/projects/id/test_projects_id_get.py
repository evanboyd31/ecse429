import httpx
from thingifier_tests.projects.conftest import *


def test_get_project_with_path_id_should_get_project_with_that_id_json(before_each):
  project = test_projects[0]
  response = httpx.get(f"{projects_url}/{project.get("id")}")
  
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 1
  
  response_project = response.json().get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)
  
def test_get_project_with_path_id_should_get_project_with_that_id_xml(before_each):
  project = test_projects[0]
  response = httpx.get(f"{projects_url}/{project.get("id")}", headers=XML_HEADERS)
  
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 1
  
  response_project = xml_to_json(response.content).get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)

def test_get_project_with_invalid_path_id_should_not_get_project_json(before_each):
  invalid_id = -1
  response = httpx.get(f"{projects_url}/{invalid_id}")
  
  assert response.status_code == 404
  assert response.json() == {"errorMessages": [f"Could not find an instance with projects/{invalid_id}"]}
  
def test_get_project_with_invalid_path_id_should_not_get_project_xml(before_each):
  invalid_id = -1
  response = httpx.get(f"{projects_url}/{invalid_id}", headers=XML_HEADERS)
  
  assert response.status_code == 404
  assert xml_to_json(response.content) == {"errorMessages": [f"Could not find an instance with projects/{invalid_id}"]}

def test_get_project_with_path_id_and_related_query_param_should_get_project_with_that_id_json(before_each):
  project = test_projects[0]
  # ensure that the response is returns the expected single project
  response = httpx.get(f"{projects_url}/{project.get("id")}?title={project.get("title")}")
  
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 1
  
  response_project = response.json().get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)
  
def test_get_project_with_path_id_and_related_query_param_should_get_project_with_that_id_xml(before_each):
  project = test_projects[0]
  # ensure that the response is returns the expected single project
  response = httpx.get(f"{projects_url}/{project.get("id")}?title={project.get("title")}", headers=XML_HEADERS)
  
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 1
  
  response_project = xml_to_json(response.content).get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)
  
def test_get_project_with_path_id_and_unrelated_query_param_should_get_project_with_that_id_json(before_each):
  project = test_projects[0]
  
  # ensure that the response is returns the expected single project
  response = httpx.get(f"{projects_url}/{project.get("id")}?title=otherTitle")
  
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 1
  
  response_project = response.json().get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)
  
def test_get_project_with_path_id_and_unrelated_query_param_should_get_project_with_that_id_xml(before_each):
  project = test_projects[0]
  
  # ensure that the response is returns the expected single project
  response = httpx.get(f"{projects_url}/{project.get("id")}?title=otherTitle", headers=XML_HEADERS)
  
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 1
  
  response_project = xml_to_json(response.content).get("projects")[0]
  
  assert_project(expected=project, actual=response_project, check_id=True)