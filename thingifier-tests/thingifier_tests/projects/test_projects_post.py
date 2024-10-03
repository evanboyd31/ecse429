import httpx
from thingifier_tests.projects.conftest import *

def test_post_project_with_string_boolean_json(before_each):
    invalid_project = {
      "title": "title",
      "completed": "false",
      "active": "true",
      "description": "description"
    }
    
    # ensure correct error messages and codes and check that no extra project has been created
    response = httpx.post(projects_url, json=invalid_project)
    assert response.status_code == 400
    assert response.json() == {"errorMessages": ["Failed Validation: completed should be BOOLEAN, active should be BOOLEAN"]}
    
    response = httpx.get(projects_url)
    # only one project should exist in the system: the project created in before_each
    assert len(response.json().get("projects")) == 1
    
def test_post_project_with_string_boolean_xml(before_each):
    xml_data = '''
        <project>
          <title type="string">type</title>
          <completed type="string">false</completed>
          <active type="string">false</active>
          <description type="string">description</description>
        </project>
    '''
    
    # ensure correct error messages and codes and check that no extra project has been created
    response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
    assert response.status_code == 400
    assert xml_to_json(response.content) == {"errorMessages": ["Failed Validation: active should be BOOLEAN, completed should be BOOLEAN"]}
    
    response = httpx.get(projects_url, headers=XML_HEADERS)
    # only one project should exist in the system: the project created in before_each
    assert len(xml_to_json(response.content).get("projects"))== 1
    
  
def test_post_project_valid_boolean_json(before_each):
  valid_project = {
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }  

  response = httpx.post(projects_url, json=valid_project)
  
  assert response.status_code == 201
  response_json = response.json()
  
  # assert that the two projects are equal (except for their IDs)
  assert_project(expected=valid_project, actual=response_json, check_id=False)
  
def test_post_project_valid_boolean_xml(before_each):
  xml_data = '''
        <project>
  <active>false</active>
  <description>xercitation ullamcoa</description>
  <completed>false</completed>
  <title>ng elit, sed do eius</title>
</project>
    '''

  response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
  assert response.status_code == 201

  # assert that the two projects are equal (except for their IDs)
  assert_project(expected=xml_to_json(xml_data).get("project"), actual=xml_to_json(response.content).get("project"), check_id=False)
  
def test_post_blank_project_json(before_each):
  # blank project
  project = {}
  
  response = httpx.post(projects_url, json=project)
  
  assert response.status_code == 201
  assert_project(expected=project, actual=response.json(), check_id=False)
  
def test_post_blank_project_xml(before_each):
  xml_data = ""
  
  response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
  assert response.status_code == 201
  assert_project(expected=xml_to_json(xml_data), actual=xml_to_json(response.content).get("project"))
  
def test_post_project_with_id_in_body_json(before_each):
  project = {
      "id": 100,
      "title": "title",
      "completed": False,
      "active": True,
      "description": "description"
  }
  
  response = httpx.post(projects_url, json=project)
  
  assert response.status_code == 400
  assert response.json() == {"errorMessages": ["Invalid Creation: Failed Validation: Not allowed to create with id"]}
  
  response = httpx.get(projects_url)
  # only one project should exist in the system: the project created in before_each
  assert len(response.json().get("projects")) == 1
  
def test_post_project_with_id_in_body_xml(before_each):
  xml_data = '''
        <project>
        <id>100</id>
  <active>false</active>
  <description>xercitation ullamcoa</description>
  <completed>false</completed>
  <title>ng elit, sed do eius</title>
</project>
    '''
  
  response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
  
  assert response.status_code == 400
  assert xml_to_json(response.content) == {"errorMessages": ["Invalid Creation: Failed Validation: Not allowed to create with id"]}
  
  response = httpx.get(projects_url, headers=XML_HEADERS)
  # only one project should exist in the system: the project created in before_each
  assert len(xml_to_json(response.content).get("projects")) == 1

def test_post_project_with_positive_integer_string_json(before_each):
  project = {
      "title": int(1)
  }
  
  response = httpx.post(projects_url, json=project)
  
  assert response.status_code == 201
  
  response_project = response.json()
  assert response_project.get("id")
  assert response_project.get("title") == f"{project.get("title")}.0"
  assert response_project.get("completed") == ("true" if project.get("completed", "") else "false")
  assert response_project.get("active") == ("true" if project.get("active", "") else "false")
  assert response_project.get("description") == project.get("description", "")
  
def test_post_project_with_positive_integer_string_xml(before_each):
  xml_data = '''
        <project>
  <active>false</active>
  <description>description</description>
  <completed>false</completed>
  <title>100</title>
</project>
    '''
  
  response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
  print(response.content)
  
  assert response.status_code == 201
  response_project = xml_to_json(response.content).get("project")
  assert response_project.get("id")
  assert response_project.get("title") == "100.0"
  assert response_project.get("completed") == "false"
  assert response_project.get("active") == "false"
  assert response_project.get("description") == "description"
  
def test_post_project_integer_boolean_json(before_each):
  project = {
      "completed": int(1)
  }
  
  response = httpx.post(projects_url, json=project)
  
  # ensure there is a message and no projects are created
  assert response.status_code == 400
  assert response.json() == {"errorMessages":["Failed Validation: completed should be BOOLEAN"]}
  
  response = httpx.get(projects_url)
  # only one project should exist in the system: the project created in before_each
  assert len(response.json().get("projects")) == 1
  
def test_post_project_integer_boolean_xml(before_each):
  xml_data = '''
        <project>
  <active>false</active>
  <description>description</description>
  <completed>1</completed>
  <title>100</title>
</project>
    '''
  
  response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
  
  # ensure there is a message and no projects are created
  assert response.status_code == 400
  assert xml_to_json(response.content) == {"errorMessages":["Failed Validation: completed should be BOOLEAN"]}
  
  response = httpx.get(projects_url, headers=XML_HEADERS)
  # only one project should exist in the system: the project created in before_each
  assert len(xml_to_json(response.content).get("projects")) == 1

  
def test_post_project_negative_integer_string_json(before_each):
  project = {
    "description": int(-1)
  }
  
  response = httpx.post(projects_url, json=project)
  
  assert response.status_code == 201  
  response_project = response.json()
  
  assert response_project.get("id")
  assert response_project.get("title") == project.get("title", "")
  assert response_project.get("completed") == ("true" if project.get("completed", "") else "false")
  assert response_project.get("active") == ("true" if project.get("active", "") else "false")
  assert response_project.get("description") == f"{project.get("description")}.0"

def test_post_project_with_negative_integer_string_xml(before_each):
  xml_data = '''
        <project>
  <active>false</active>
  <description>-1</description>
  <completed>false</completed>
  <title>title</title>
</project>
    '''
  
  response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
  print(response.content)
  
  assert response.status_code == 201
  response_project = xml_to_json(response.content).get("project")
  assert response_project.get("id")
  assert response_project.get("title") == "title"
  assert response_project.get("completed") == "false"
  assert response_project.get("active") == "false"
  assert response_project.get("description") == "-1.0"
  
def test_post_project_integer_id_json(before_each):
  project = {
    "id": 100
  }
  
  response = httpx.post(projects_url, json=project)
  
  # ensure error message and that no project is created
  assert response.status_code == 400
  assert response.json() == {"errorMessages":["Invalid Creation: Failed Validation: Not allowed to create with id"]}
  
  response = httpx.get(projects_url)
  # only one project should exist in the system: the project created in before_each
  assert len(response.json().get("projects")) == 1
  
def test_post_project_integer_id_xml(before_each):
  xml_data = '''
        <project>
        <id>100</id>
  <active>false</active>
  <description>description</description>
  <completed>false</completed>
  <title>title</title>
</project>
    '''
  
  response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
  
  # ensure error message and that no project is created
  assert response.status_code == 400
  assert xml_to_json(response.content) == {"errorMessages":["Invalid Creation: Failed Validation: Not allowed to create with id"]}
  
  response = httpx.get(projects_url, headers=XML_HEADERS)
  # only one project should exist in the system: the project created in before_each
  assert len(xml_to_json(response.content).get("projects")) == 1
  
def test_post_project_with_title_query_param_json(before_each):
  
  test_project_title = test_projects[0].get("title")
  project = {
      "title": "anotherTitle",
      "completed": False,
      "active": False,
      "description": "description"
  }
  
    # ensure a brand new project is created and the id in the query params was ignored
  response = httpx.post(f"{projects_url}?title={test_project_title}", json=project)
  
  assert response.status_code == 201
  response_project = response.json()
  assert_project(expected=project, actual=response_project, check_id=False)

  
  # ensure two separate projects exist in the system
  response = httpx.get(projects_url)
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 2
  
def test_post_project_with_title_query_param_xml(before_each):
  
  test_project_title = test_projects[0].get("title")
  xml_data = '''
        <project>
  <active>false</active>
  <description>description</description>
  <completed>false</completed>
  <title>anotherTitle</title>
</project>
    '''
  
    # ensure a brand new project is created and the id in the query params was ignored
  response = httpx.post(f"{projects_url}?title={test_project_title}", data=xml_data, headers=XML_HEADERS)
  
  assert response.status_code == 201
  response_project = xml_to_json(response.content).get("project")
  assert_project(expected=xml_to_json(xml_data).get("project"), actual=response_project, check_id=False)

  
  # ensure two separate projects exist in the system
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 2
  
def test_post_project_with_id_query_param_json(before_each):
  
  test_project_id = test_projects[0].get("id")
  project = {
      "title": "anotherTitle",
      "completed": False,
      "active": False,
      "description": "description"
  }
  
    # ensure a brand new project is created and the id in the query params was ignored
  response = httpx.post(f"{projects_url}?id={test_project_id}", json=project)
  
  assert response.status_code == 201
  response_project = response.json()
  assert_project(expected=project, actual=response_project, check_id=False)

  # ensure two separate projects exist in the system
  response = httpx.get(projects_url)
  assert response.status_code == 200
  assert len(response.json().get("projects", [])) == 2
  
def test_post_project_with_id_query_param_xml(before_each):
  
  test_project_id = test_projects[0].get("id")
  xml_data = '''
        <project>
  <active>false</active>
  <description>description</description>
  <completed>false</completed>
  <title>anotherTitle</title>
</project>
    '''
  
    # ensure a brand new project is created and the id in the query params was ignored
  response = httpx.post(f"{projects_url}?id={test_project_id}", data=xml_data, headers=XML_HEADERS)
  
  assert response.status_code == 201
  response_project = xml_to_json(response.content).get("project")
  assert_project(expected=xml_to_json(xml_data).get("project"), actual=response_project, check_id=False)

  
  # ensure two separate projects exist in the system
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 2