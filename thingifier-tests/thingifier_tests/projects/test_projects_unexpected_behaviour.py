import httpx
from thingifier_tests.projects.conftest import *

def test_post_project_with_string_boolean_json_expected_behaviour(before_each):
  invalid_project = {
      "title": "title",
      "completed": "false",
      "active": "true",
      "description": "description"
    }
    
  # the response message should've had message 201 and returned the created project
  response = httpx.post(projects_url, json=invalid_project)
  assert response.status_code != 201
  assert response.json() != invalid_project
  
  response = httpx.get(projects_url)
  # one project should've been added, so 2 projects would exist in the system
  assert len(response.json().get("projects")) != 2

def test_post_project_with_string_boolean_json_actual_behaviour(before_each):
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
    
def test_post_project_with_string_boolean_xml_expected_behaviour(before_each):
    xml_data = '''
        <project>
          <title type="string">type</title>
          <completed type="string">false</completed>
          <active type="string">false</active>
          <description type="string">description</description>
        </project>
    '''
    
    # the response message should've had message 201 and returned the created project
    response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)
    assert response.status_code != 201
    assert response.content != xml_data
    
    response = httpx.get(projects_url, headers=XML_HEADERS)
     # only one project should exist in the system: the project created in before_each
    assert len(xml_to_json(response.content).get("projects")) != 2

def test_post_project_with_string_boolean_xml_actual_behaviour(before_each):
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
    assert len(xml_to_json(response.content).get("projects")) == 1
    
def test_id_post_project_with_new_id_string_json_expected_behaviour(before_each):
  test_project = test_projects[0]

  id = str(int(test_project.get("id")) + 1)
  
  # expected that the id of project would be updated according to documentation
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", json={"id": id})
  assert response.status_code != 200
  assert response.json() != {"id": id, "title": "", "completed": "false", "active": "false", "description": ""}
  
  # only one project should exist after expected update
  response = httpx.get(projects_url)
  assert response.status_code == 200
  assert len(response.json().get("projects")) == 1
  assert response.json().get("projects")[0].get("id") == test_project.get("id")

def test_id_post_project_with_new_id_string_json_actual_behaviour(before_each):
  test_project = test_projects[0]

  id = str(int(test_project.get("id")) + 1)
  
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", json={"id": id})
  assert response.status_code == 400
  assert response.json() == {"errorMessages":["Failed Validation: id should be ID"]}
  
  # ensure that only one project exists in the system and it has the old id
  response = httpx.get(projects_url)
  assert response.status_code == 200
  assert len(response.json().get("projects")) == 1
  assert response.json().get("projects")[0].get("id") == test_project.get("id")

def test_id_post_project_with_new_id_string_xml_expected_behaviour(before_each):
  test_project = test_projects[0]

  id = str(int(test_project.get("id")) + 1)
  
  xml_data = f'''
                <project>
                <id type="string">{id}</id>
                <active>true</active>
                <description>updated description</description>
                <completed>false</completed>
                <title>updated title</title>
                </project>
                '''
  
  # expected that the id of project would be updated according to documentation
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS)
  assert response.status_code == 400
  assert xml_to_json(response.content) == {"errorMessages":["Failed Validation: id should be ID"]}
  
  # only one project should exist after expected update
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 1
  assert xml_to_json(response.content).get("projects")[0].get("id") == test_project.get("id")

def test_id_post_project_with_new_id_string_xml_actual_behaviour(before_each):
  test_project = test_projects[0]

  id = str(int(test_project.get("id")) + 1)
  
  xml_data = f'''
                <project>
                <id type="string">{id}</id>
                <active>true</active>
                <description>updated description</description>
                <completed>false</completed>
                <title>updated title</title>
                </project>
                '''
  
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS)
  assert response.status_code != 200
  assert xml_to_json(response.content) != {"id": id, "title": "", "completed": "false", "active": "false", "description": ""}
  
  # ensure that only one project exists in the system and it has the old id
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 1
  assert xml_to_json(response.content).get("projects")[0].get("id") == test_project.get("id")
  
def test_id_put_project_with_string_boolean_json_expected_behaviour(before_each):
  test_project = test_projects[0]
  new_data = {
    "title": "new title",
    "completed": "true",
    "active": "true",
    "description": "new description"
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # expected that the project would be updated
  new_data.update({
    "id" : test_project.get("id")
  })
  assert response.status_code != 200
  assert response.json() != new_data
  
  # only one project should exist in the system after update
  response = httpx.get(projects_url)
  assert len(response.json().get("projects")) == 1

def test_id_put_project_with_string_boolean_json_actual_behaviour(before_each):
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

def test_id_put_project_with_string_boolean_xml_expected_behaviour(before_each):
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
  
  # project should've been updated with 200 response code
  expected_data = xml_to_json(new_data)
  expected_data.get("project").update({
    "id": test_project.get("id") 
  })
  assert response.status_code != 200
  assert xml_to_json(response.content) != expected_data
  
  # a single project would exist in system after update
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert len(xml_to_json(response.content).get("projects")) == 1

def test_id_put_project_with_string_boolean_xml_actual_behaviour(before_each):
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
  
def test_id_put_project_different_int_id_json_expected_behaviour(before_each):
  test_project = test_projects[0]
  new_data = {
    "id": 200,
    "title": "new title",
    "completed": True,
    "active": True,
    "description": "new description"
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # ensure we update successfully and fields (including ID) are updated correctly
  assert response.status_code == 200
  assert response.json() != {"id": "200", "title": "new title", "completed": "true", "active": "true", "description": "new description"}

def test_id_put_project_different_int_id_json_actual_behaviour(before_each):
  test_project = test_projects[0]
  new_data = {
    "id": 200,
    "title": "new title",
    "completed": True,
    "active": True,
    "description": "new description"
  }
  
  response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)
  
  # ensure we update successfully and fields (not including ID) are updated correctly
  assert response.status_code == 200
  assert_project(expected=new_data, actual=response.json(), check_id=False)
  
def test_id_put_project_different_int_id_xml_expected_behaviour(before_each):
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
  
  # ensure we update successfully and fields (including ID) are updated correctly
  assert response.status_code == 200
  assert xml_to_json(response.content) != {"id": "200", "title": "new title", "completed": "true", "active": "true", "description": "new description"}
  
def test_id_put_project_different_int_id_xml_actual_behaviour(before_each):
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
  
  # ensure we update successfully and fields (not including ID) are updated correctly
  assert response.status_code == 200
  assert_project(expected=xml_to_json(new_data).get("project"), actual=xml_to_json(response.content).get("project"))

def test_id_post_project_with_new_int_id_json_expected_behaviour(before_each):
  test_project = test_projects[0]

  id = int(test_project.get("id")) + 1
  
  project = {
    "id": id,
    "title": "New title",
    "completed": True,
    "active": True,
    "description": "New description"
  }
  
  # project should've been updated with new id
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", json=project)
  assert response.status_code == 200
  response_project = response.json()
  assert response_project != {"id": f"{id}", "title": "New title", "completed": "true", "active": "true", "description": "New description"}
  
  # ensure that only one project exists in the system. it should've had new id
  response = httpx.get(projects_url)
  assert response.status_code == 200
  assert len(response.json().get("projects")) == 1
  assert response.json().get("projects")[0].get("id") != f"{id}"

def test_id_post_project_with_new_int_id_json_actual_behaviour(before_each):
  test_project = test_projects[0]

  id = int(test_project.get("id")) + 1
  
  project = {
    "id": id,
    "title": "New title",
    "completed": True,
    "active": True,
    "description": "New description"
  }
  
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", json=project)
  assert response.status_code == 200
  
  response_project = response.json()
  
  assert_project(expected=project, actual=response_project, check_id=False)
  
  # ensure that only one project exists in the system and it has the old id
  response = httpx.get(projects_url)
  assert response.status_code == 200
  assert len(response.json().get("projects")) == 1
  assert response.json().get("projects")[0].get("id") == test_project.get("id")

def test_id_post_project_with_new_int_id_xml_expected_behaviour(before_each):
  test_project = test_projects[0]

  id = int(test_project.get("id")) + 1
  
  xml_data = f'''
                <project>
                <id>{id}</id>
                <active>true</active>
                <description>updated description</description>
                <completed>false</completed>
                <title>updated title</title>
                </project>
                '''
  # project should've been updated to have new id
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS)
  assert response.status_code == 200
  response_project = xml_to_json(response.content).get("project")
  assert response_project != {"id": f"{id}", "title": "New title", "completed": "true", "active": "true", "description": "New description"}
  
  # ensure that only one project exists in the system. it should've had new id
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 1
  assert xml_to_json(response.content).get("projects")[0].get("id") != f"{id}"

def test_id_post_project_with_new_int_id_xml(before_each):
  test_project = test_projects[0]

  id = int(test_project.get("id")) + 1
  
  xml_data = f'''
                <project>
                <id>{id}</id>
                <active>true</active>
                <description>updated description</description>
                <completed>false</completed>
                <title>updated title</title>
                </project>
                '''
  
  response = httpx.post(f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS)
  assert response.status_code == 200
  
  response_project = xml_to_json(response.content).get("project")
  
  assert_project(expected=xml_to_json(xml_data).get("project"), actual=response_project, check_id=False)
  
  # ensure that only one project exists in the system and it has the old id
  response = httpx.get(projects_url, headers=XML_HEADERS)
  assert response.status_code == 200
  assert len(xml_to_json(response.content).get("projects")) == 1
  assert xml_to_json(response.content).get("projects")[0].get("id") == test_project.get("id")
    