import pytest
import httpx
import thingifier_tests.test_common as common


projects_url = "http://localhost:4567/projects"

XML_HEADERS = {
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}

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
  
import json
import xmltodict

import xmltodict

def xml_to_json(xml_content):
    """
    Convert XML content to a JSON-like dictionary structure using xmltodict.
    Handles cases for successful responses and errors.
    """
    # Convert XML to an OrderedDict
    data_dict = xmltodict.parse(xml_content)

    # Check for error indicators in the parsed data
    if 'errorMessages' in data_dict:
        return {'errorMessages': data_dict['errorMessages']}  # Handle the error case

    # Initialize projects as an empty list
    projects = []

    # Check if 'projects' is in the parsed data
    if 'projects' in data_dict:
        projects = data_dict['projects'].get('project', [])
        
        # Ensure projects is a list
        if isinstance(projects, dict):  # If there's only one project, convert to a list
            projects = [projects]
          
        return {'projects': projects}
    else:
      return data_dict


def json_to_xml(json_dict):
    """
    Convert a JSON dictionary to an XML string.
    """
    try:
        # Convert the JSON dict to an XML string
        xml_str = xmltodict.unparse(json_dict, pretty=True)
        return xml_str
    except Exception as e:
        print(f"Error converting to XML: {e}")
        return None
