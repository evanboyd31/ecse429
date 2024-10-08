import httpx
from thingifier_tests.projects.conftest import *


def test_id_post_project_should_update_project_json(before_each):
    test_project = test_projects[0]

    id = test_project.get("id")

    updated_project = {
        "title": "updated title",
        "completed": True,
        "active": True,
        "description": "updated description",
    }
    response = httpx.put(f"{projects_url}/{id}", json=updated_project)

    assert response.status_code == 200
    response_project = response.json()

    updated_project.update({"id": id})
    assert_project(expected=updated_project, actual=response_project, check_id=True)

    # ensure only a single project exists in the system
    response = httpx.get(projects_url)
    assert response.status_code == 200
    assert len(response.json().get("projects", [])) == 1


def test_id_post_project_should_update_project_xml(before_each):
    test_project = test_projects[0]

    id = test_project.get("id")

    xml_data = """
                <project>
                <active>true</active>
                <description>updated description</description>
                <completed>false</completed>
                <title>updated title</title>
                </project>
                """
    response = httpx.put(f"{projects_url}/{id}", data=xml_data, headers=XML_HEADERS)

    assert response.status_code == 200
    response_project = xml_to_json(response.content).get("project")

    expected = xml_to_json(xml_data).get("project")
    expected.update({"id": f"{id}"})

    assert_project(expected=expected, actual=response_project, check_id=False)

    # ensure only a single project exists in the system
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert response.status_code == 200
    assert len(xml_to_json(response.content).get("projects")) == 1


def test_id_post_project_with_new_id_string_should_not_update_project_json(before_each):
    test_project = test_projects[0]

    id = str(int(test_project.get("id")) + 1)

    response = httpx.post(f"{projects_url}/{test_project.get("id")}", json={"id": id})
    assert response.status_code == 400
    assert response.json() == {"errorMessages": ["Failed Validation: id should be ID"]}

    # ensure that only one project exists in the system and it has the old id
    response = httpx.get(projects_url)
    assert response.status_code == 200
    assert len(response.json().get("projects")) == 1
    assert response.json().get("projects")[0].get("id") == test_project.get("id")


def test_id_post_project_with_new_id_string_should_not_update_project_xml(before_each):
    test_project = test_projects[0]

    id = str(int(test_project.get("id")) + 1)

    xml_data = f"""
                <project>
                <id type="string">{id}</id>
                <active>true</active>
                <description>updated description</description>
                <completed>false</completed>
                <title>updated title</title>
                </project>
              """

    response = httpx.post(
        f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS
    )
    assert response.status_code != 200
    assert xml_to_json(response.content) != {
        "id": id,
        "title": "",
        "completed": "false",
        "active": "false",
        "description": "",
    }

    # ensure that only one project exists in the system and it has the old id
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert response.status_code == 200
    assert len(xml_to_json(response.content).get("projects")) == 1
    assert xml_to_json(response.content).get("projects")[0].get(
        "id"
    ) == test_project.get("id")


def test_id_post_project_with_new_int_id_should_not_update_project_json(before_each):
    test_project = test_projects[0]

    id = int(test_project.get("id")) + 1

    project = {
        "id": id,
        "title": "New title",
        "completed": True,
        "active": True,
        "description": "New description",
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


def test_id_post_project_with_new_int_id_should_not_update_project_xml(before_each):
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

    response = httpx.post(
        f"{projects_url}/{test_project.get("id")}", data=xml_data, headers=XML_HEADERS
    )
    assert response.status_code == 200

    response_project = xml_to_json(response.content).get("project")

    assert_project(
        expected=xml_to_json(xml_data).get("project"),
        actual=response_project,
        check_id=False,
    )

    # ensure that only one project exists in the system and it has the old id
    response = httpx.get(projects_url, headers=XML_HEADERS)
    assert response.status_code == 200
    assert len(xml_to_json(response.content).get("projects")) == 1
    assert xml_to_json(response.content).get("projects")[0].get(
        "id"
    ) == test_project.get("id")
