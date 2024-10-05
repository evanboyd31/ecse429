import httpx
from thingifier_tests.projects.conftest import *

def test_id_post_project_json(before_each):
    test_project = test_projects[0]

    id = test_project.get("id")

    updated_project = {
        "title": "updated title",
        "completed": True,
        "active": True,
        "description": "updated description"
    }
    response = httpx.put(f"{projects_url}/{id}", json=updated_project)
    
    assert response.status_code == 200 
    response_project = response.json()
    
    updated_project.update({
      "id": id
    })
    assert_project(expected=updated_project, actual=response_project, check_id=True)
    
    # ensure only a single project exists in the system
    response = httpx.get(projects_url)
    assert response.status_code == 200
    assert len(response.json().get("projects", [])) == 1
    
def test_id_post_project_xml(before_each):
    test_project = test_projects[0]

    id = test_project.get("id")

    xml_data = '''
                <project>
                <active>true</active>
                <description>updated description</description>
                <completed>false</completed>
                <title>updated title</title>
                </project>
                '''
    response = httpx.put(f"{projects_url}/{id}", data=xml_data, headers=XML_HEADERS)
    
    assert response.status_code == 200 
    response_project = xml_to_json(response.content).get("project")
    
    expected = xml_to_json(xml_data).get("project")
    expected.update({
      "id": f"{id}"
    })
    
    assert_project(expected=expected, actual=response_project, check_id=False)
    
    # ensure only a single project exists in the system
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert response.status_code == 200
    assert len(xml_to_json(response.content).get("projects")) == 1