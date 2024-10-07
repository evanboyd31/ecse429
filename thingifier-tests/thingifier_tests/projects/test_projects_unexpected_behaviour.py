import httpx
from thingifier_tests.projects.conftest import *


def test_post_project_with_string_boolean_fails_to_create_project_json(before_each):
    """
    In the provided JSON input in the API documentation, the Boolean variables for a project,
    completed and active, are represented as strings. This test illustrates the
    expected behaviour according to the API documentation, but ultimately fails.
    """
    project = {
        "title": "title",
        "completed": "false",
        "active": "true",
        "description": "description",
    }

    # the response message should've had message 201 and returned the created project
    response = httpx.post(projects_url, json=project)

    id = response.json().get("id")
    project.update({"id": id})

    assert response.status_code == 201
    assert response.json() == project

    response = httpx.get(projects_url)
    # one project should've been added, so 2 projects would exist in the system
    assert len(response.json().get("projects")) == 2


def test_post_project_with_string_boolean_fails_to_create_project_xml(before_each):
    """
    In the provided JSON input in the API documentation, the Boolean variables for a project,
    completed and active, are represented as strings. This test illustrates the
    expected behaviour according to the API documentation, but ultimately fails.
    """
    xml_data = """
        <project>
          <title type="string">type</title>
          <completed type="string">false</completed>
          <active type="string">false</active>
          <description type="string">description</description>
        </project>
    """

    # the response message should've had message 201 and returned the created project
    response = httpx.post(projects_url, data=xml_data, headers=XML_HEADERS)

    expected_project = xml_to_json(xml_data)
    expected_project.get("project").update({"id": response.json().get("id")})

    assert response.status_code == 201
    assert xml_to_json(response.content) == expected_project

    response = httpx.get(projects_url, headers=XML_HEADERS)
    # only one project should exist in the system: the project created in before_each
    assert len(xml_to_json(response.content).get("projects")) == 2


def test_id_post_project_with_new_id_fails_to_update_project_id_json(before_each):
    """
    In the provided example JSON input in the API documentation, ID is a permitted
    request body variable for a project. Therefore, it is expected that the
    ID can be updated if we are allowed to assign a new ID to a project through this endpoint,
    but ultimately fails
    """
    test_project = test_projects[0]

    id = int(test_project.get("id")) + 1

    project = {
        "id": id,
        "title": "New title",
        "completed": True,
        "active": True,
        "description": "New description",
    }

    # project should've been updated with new id
    response = httpx.post(f"{projects_url}/{test_project.get("id")}", json=project)
    assert response.status_code == 200
    response_project = response.json()
    assert response_project == {
        "id": f"{id}",
        "title": "New title",
        "completed": "true",
        "active": "true",
        "description": "New description",
    }

    # ensure that only one project exists in the system. it should've had new id
    response = httpx.get(projects_url)
    assert response.status_code == 200
    assert len(response.json().get("projects")) == 1
    assert response.json().get("projects")[0].get("id") == f"{id}"


def test_id_post_project_with_new_id_fails_to_update_project_id_xml(before_each):
    """
    In the provided example JSON input in the API documentation, ID is a permitted
    request body variable for a project. Therefore, it is expected that the
    ID can be updated if we are allowed to assign a new ID to a project through this endpoint,
    but ultimately fails
    """
    test_project = test_projects[0]

    id = int(test_project.get("id")) + 1

    xml_data = f"""
              <project>
              <id>{id}</id>
              <active>true</active>
              <description>updated description</description>
              <completed>false</completed>
              <title>updated title</title>
              </project>
              """
    # project should've been updated to have new id
    response = httpx.post(
        f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS
    )
    assert response.status_code == 200
    response_project = xml_to_json(response.content).get("project")
    assert response_project == {
        "id": f"{id}",
        "title": "New title",
        "completed": "true",
        "active": "true",
        "description": "New description",
    }

    # ensure that only one project exists in the system. it should've had new id
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert response.status_code == 200
    assert len(xml_to_json(response.content).get("projects")) == 1
    assert xml_to_json(response.content).get("projects")[0].get("id") == f"{id}"


def test_id_put_project_with_string_boolean_fails_to_update_project_json(before_each):
    """
    In the provided JSON input in the API documentation, the Boolean variables for a project,
    completed and active, are represented as strings. This test illustrates the
    expected behaviour according to the API documentation, but ultimately fails.
    """
    test_project = test_projects[0]
    new_data = {
        "title": "new title",
        "completed": "true",
        "active": "true",
        "description": "new description",
    }

    response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=new_data)

    # expected that the project would be updated
    new_data.update({"id": test_project.get("id")})
    assert response.status_code == 200
    assert response.json() == new_data

    # only one project should exist in the system after update
    response = httpx.get(projects_url)
    assert len(response.json().get("projects")) == 1


def test_id_put_project_with_string_boolean_fails_to_update_project_xml(before_each):
    test_project = test_projects[0]
    new_data = """
             <project>
              <active type="string">true</active>
              <description>new description</description>
              <completed type="string">true</completed>
              <title>new title</title>
             </project>
            """

    response = httpx.put(
        f"{projects_url}/{test_project.get("id")}", data=new_data, headers=XML_HEADERS
    )

    # ensure we get error message and that none of the fields are updated
    expected = xml_to_json(new_data)
    expected.data.get("project").update({"id": test_project.get("id")})
    assert response.status_code == 400
    assert xml_to_json(response.content) == expected

    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert len(xml_to_json(response.content).get("projects")) == 1


def test_id_put_project_with_new_id_fails_to_update_project_id_json(before_each):
    """
    In the provided example JSON input in the API documentation, ID is a permitted
    request body variable for a project. Therefore, it is expected that the
    ID can be updated if we are allowed to assign a new ID to a project through this endpoint,
    but ultimately fails
    """
    test_project = test_projects[0]

    id = int(test_project.get("id")) + 1

    project = {
        "id": id,
        "title": "New title",
        "completed": True,
        "active": True,
        "description": "New description",
    }

    # project should've been updated with new id
    response = httpx.put(f"{projects_url}/{test_project.get("id")}", json=project)
    assert response.status_code == 200
    response_project = response.json()
    assert response_project == {
        "id": f"{id}",
        "title": "New title",
        "completed": "true",
        "active": "true",
        "description": "New description",
    }

    # ensure that only one project exists in the system. it should've had new id
    response = httpx.get(projects_url)
    assert response.status_code == 200
    assert len(response.json().get("projects")) == 1
    assert response.json().get("projects")[0].get("id") == f"{id}"


def test_id_put_project_with_new_id_fails_to_update_project_id_xml(before_each):
    """
    In the provided example JSON input in the API documentation, ID is a permitted
    request body variable for a project. Therefore, it is expected that the
    ID can be updated if we are allowed to assign a new ID to a project through this endpoint,
    but ultimately fails
    """
    test_project = test_projects[0]

    id = int(test_project.get("id")) + 1

    xml_data = f"""
              <project>
              <id>{id}</id>
              <active>true</active>
              <description>updated description</description>
              <completed>false</completed>
              <title>updated title</title>
              </project>
              """
    # project should've been updated to have new id
    response = httpx.put(
        f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS
    )
    assert response.status_code == 200
    response_project = xml_to_json(response.content).get("project")
    assert response_project == {
        "id": f"{id}",
        "title": "New title",
        "completed": "true",
        "active": "true",
        "description": "New description",
    }

    # ensure that only one project exists in the system. it should've had new id
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert response.status_code == 200
    assert len(xml_to_json(response.content).get("projects")) == 1
    assert xml_to_json(response.content).get("projects")[0].get("id") == f"{id}"
