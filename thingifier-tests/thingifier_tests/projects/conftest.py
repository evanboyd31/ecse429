import pytest
import httpx
import thingifier_tests.test_common as common
import xmltodict

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
    
  assert (actual.get("title") if actual.get("title") is not None else "") == expected.get("title", "")
  assert actual.get("completed") == ("true" if expected.get("completed") in [True, "true"] else "false")
  assert actual.get("active") == ("true" if expected.get("active") in [True, "true"] else "false")
  assert (actual.get("description") if actual.get("description") is not None else "") == expected.get("description", "")
  

def xml_to_json(xml_content):
    """
    Convert XML content to a JSON-like dictionary structure using xmltodict.
    Handles cases for successful responses and errors.
    """
    if not xml_content:
      return {}
      
    # Convert XML to an OrderedDict
    data_dict = xmltodict.parse(xml_content)

    # Check for error indicators in the parsed data
    if 'errorMessages' in data_dict:
      errors = data_dict['errorMessages'].get('errorMessage', [])
      
      # Ensure projects is a list
      if not isinstance(errors, list):  # If there's only one project, convert to a list
          errors = [errors]
      return {'errorMessages': errors}  # Handle the error case

    # Initialize projects as an empty list
    projects = []

    # Check if 'projects' is in the parsed data
    if 'projects' in data_dict:
        projects = data_dict['projects'].get('project', []) if data_dict["projects"] is not None else []
        
        # Ensure projects is a list
        if not isinstance(projects, list):  # If there's only one project, convert to a list
            projects = [projects]
          
        return {'projects': projects}
    
    return data_dict


import xml.etree.ElementTree as ET
from typing import Any, Dict

def get_xml_type(value: Any) -> str:
    """
    Determine the XML schema type for a given Python value.
    
    Args:
        value (Any): The value for which to determine the type.
    
    Returns:
        str: The corresponding XML schema type as a string.
    """
    if isinstance(value, str):
        return "xs:string"
    elif isinstance(value, bool):
        return "xs:boolean"
    elif isinstance(value, int):
        return "xs:int"
    elif isinstance(value, float):
        return "xs:float"
    # Add more type checks as needed
    else:
        return "xs:string"  # Default type

def json_to_xml(json_dict: Dict[str, Any]) -> str:
    """
    Convert a JSON dictionary to an XML schema string.
    
    Args:
        json_dict (Dict[str, Any]): The JSON dictionary to convert.
        
    Returns:
        str: The resulting XML schema string.
    """
    # Create the root element
    schema = ET.Element("xs:schema", xmlns_xs="http://www.w3.org/2001/XMLSchema")

    # Create the 'project' element
    project_element = ET.SubElement(schema, "xs:element", name="project")
    complex_type = ET.SubElement(project_element, "xs:complexType")
    sequence = ET.SubElement(complex_type, "xs:sequence")

    # Create elements for each key in the dictionary
    for key, value in json_dict.items():
        type_annotation = get_xml_type(value)
        ET.SubElement(sequence, "xs:element", name=key, type=type_annotation)

    # Convert the ElementTree to a string
    xml_str = ET.tostring(schema, encoding="utf-8", xml_declaration=True).decode("utf-8")
    return xml_str

