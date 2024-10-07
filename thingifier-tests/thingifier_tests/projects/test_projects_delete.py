import httpx
from thingifier_tests.projects.conftest import *


def test_delete_all_projects_should_not_delete_all_projects_json(before_each):
  # ensure method is not allowed and that the added project still exists
  response = httpx.delete(projects_url)
  assert response.status_code == 405
  
  
  response = httpx.get(projects_url)

  assert response.status_code == 200
  assert len(response.json().get("projects")) == 1
  assert_project(expected=test_projects[0], actual=response.json().get("projects")[0], check_id=True)
  
def test_delete_all_projects_should_not_delete_all_projects_xml(before_each):
  # ensure method is not allowed and that the added project still exists
  response = httpx.delete(projects_url, headers=XML_HEADERS)
  assert response.status_code == 405
  
  
  response = httpx.get(projects_url, headers=XML_HEADERS)

  assert response.status_code == 200
  list_of_projects = xml_to_json(response.content).get("projects")
  assert len(list_of_projects) == 1
  
  response_project = list_of_projects[0]
  
  assert_project(expected=test_projects[0], actual=response_project, check_id=True)
  
def test_delete_project_using_filter_should_not_delete_all_projects_matching_filter_json(before_each):
  # ensure method is not allowed and that the added project still exists
  response = httpx.delete(f"{projects_url}?title={test_projects[0].get("title")}")
  assert response.status_code == 405
  
  
  response = httpx.get(projects_url)

  assert response.status_code == 200
  assert len(response.json().get("projects")) == 1
  assert_project(expected=test_projects[0], actual=response.json().get("projects")[0], check_id=True)

def test_delete_project_using_filter_should_not_delete_all_projects_matching_filter_xml(before_each):
  # ensure method is not allowed and that the added project still exists
  response = httpx.delete(f"{projects_url}?title={test_projects[0].get("title")}", headers=XML_HEADERS)
  assert response.status_code == 405
  
  
  response = httpx.get(projects_url, headers=XML_HEADERS)

  assert response.status_code == 200
  list_of_projects = xml_to_json(response.content).get("projects")
  assert len(list_of_projects) == 1
  
  response_project = list_of_projects[0]
  
  assert_project(expected=test_projects[0], actual=response_project, check_id=True)