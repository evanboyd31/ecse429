import httpx
from thingifier_tests.projects.conftest import *

def test_id_put_project_with_string_boolean_json(before_each):
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

def test_id_put_project_with_string_boolean_xml(before_each):
  test_project = test_projects[0]
  new_data = '''
        <project>
  <active type="string">true</active>
  <description>new description</description>
  <completed type="string">true</completed>
  <title>new title</title>
</project>
    '''
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", data=new_data, headers=XML_HEADERS)
  
  # ensure we get error message and that none of the fields are updated
  assert response.status_code == 400
  assert xml_to_json(response.content) == {"errorMessages": ["Failed Validation: active should be BOOLEAN, completed should be BOOLEAN"]}
  
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert len(xml_to_json(response.content).get("projects")) == 1
  
  assert_project(expected=test_project, actual=xml_to_json(response.content).get("projects")[0], check_id=True)
  
def test_id_put_project_with_valid_boolean_json(before_each):
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
  
def test_id_put_project_with_valid_boolean_xml(before_each):
  test_project = test_projects[0]
  new_data = '''
        <project>
  <active>true</active>
  <description>new description</description>
  <completed>true</completed>
  <title>new title</title>
</project>
    '''
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", data=new_data, headers=XML_HEADERS)
  
  # ensure we update successfully and fields are updated correctly
  assert response.status_code == 200
  assert_project(expected=xml_to_json(new_data).get("project"), actual=xml_to_json(response.content).get("project"))
  
def test_id_put_project_different_int_id_json(before_each):
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
  
def test_id_put_project_different_int_id_xml(before_each):
  test_project = test_projects[0]
  new_data = '''
        <project>
        <id>200</id>
  <active>true</active>
  <description>new description</description>
  <completed>true</completed>
  <title>new title</title>
</project>
    '''
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", data=new_data, headers=XML_HEADERS)
  
  # ensure we update successfully and fields are updated correctly
  assert response.status_code == 200
  assert_project(expected=xml_to_json(new_data).get("project"), actual=xml_to_json(response.content).get("project"))
  
def test_id_put_project_different_string_id_json(before_each):
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

def test_id_put_project_different_string_id_xml(before_each):
  test_project = test_projects[0]
  new_data = '''
        <project>
        <id type="string">200</id>
  <active>true</active>
  <description>new description</description>
  <completed>true</completed>
  <title>new title</title>
</project>
    '''
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", data=new_data, headers=XML_HEADERS)
  
  # ensure error is thrown and existing project is not updated
  assert response.status_code == 400
  assert xml_to_json(response.content) == {"errorMessages":["Failed Validation: id should be ID"]}
  
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert len(xml_to_json(response.content).get("projects")) == 1
  assert_project(expected=test_project, actual=xml_to_json(response.content).get("projects")[0], check_id=True)
  
def test_id_put_project_different_boolean_id_json(before_each):
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
  
def test_id_put_project_different_boolean_id_xml(before_each):
  test_project = test_projects[0]
  new_data = '''
        <project>
        <id>true</id>
  <active>true</active>
  <description>new description</description>
  <completed>true</completed>
  <title>new title</title>
</project>
    '''
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", data=new_data, headers=XML_HEADERS)
  
  # ensure error is thrown and existing project is not updated
  assert response.status_code == 400
  assert xml_to_json(response.content) == {"errorMessages":["Failed Validation: id should be ID"]}
  
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert len(xml_to_json(response.content).get("projects")) == 1
  assert_project(expected=test_project, actual=xml_to_json(response.content).get("projects")[0], check_id=True)
  