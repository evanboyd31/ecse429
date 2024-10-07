from thingifier_tests.interop.conftest import *
import xmltodict


class TestInteropIdUnexpected:
    def test_post_todos_id_projects_should_create_link_xml(self):
        todo = default["todos"][1]
        project = default["projects"][1]
        xml_data = "<project><id>" + project["id"] + "</id></project>"
        res = httpx.post(
            todos_url + "/" + todo["id"] + "/tasksof",
            data=xml_data,
            headers=XML_HEADERS,
        )
        assert res.status_code == 201
        res = httpx.get(todos_url + "/" + todo["id"] + "/tasksof", headers=XML_HEADERS)
        assert (
            xmltodict.parse(res.content)["projects"]["project"]["id"] == project["id"]
        )

    def test_post_todos_id_categories_should_create_link_xml(self):
        todo = default["todos"][1]
        category = default["categories"][1]
        xml_data = "<category><id>" + category["id"] + "</id></category>"
        res = httpx.post(
            todos_url + "/" + todo["id"] + "/categories",
            data=xml_data,
            headers=XML_HEADERS,
        )
        assert res.status_code == 201
        res = httpx.get(
            todos_url + "/" + todo["id"] + "/categories", headers=XML_HEADERS
        )
        assert (
            xmltodict.parse(res.content)["categories"]["category"]["id"]
            == category["id"]
        )

    def test_post_projects_id_todos_should_create_link_xml(self):
        project = default["projects"][1]
        todo = default["todos"][1]
        xml_data = "<todo><id>" + todo["id"] + "</id></todo>"
        res = httpx.post(
            projects_url + "/" + project["id"] + "/tasks",
            data=xml_data,
            headers=XML_HEADERS,
        )
        assert res.status_code == 201
        res = httpx.get(
            projects_url + "/" + project["id"] + "/tasks", headers=XML_HEADERS
        )
        assert xmltodict.parse(res.content)["todos"]["todo"]["id"] == todo["id"]

    def test_post_projects_id_categories_should_create_link_xml(self):
        project = default["projects"][1]
        category = default["categories"][1]
        xml_data = "<category><id>" + category["id"] + "</id></category>"
        res = httpx.post(
            projects_url + "/" + project["id"] + "/categories",
            data=xml_data,
            headers=XML_HEADERS,
        )
        assert res.status_code == 201
        res = httpx.get(
            projects_url + "/" + project["id"] + "/categories", headers=XML_HEADERS
        )
        assert (
            xmltodict.parse(res.content)["categories"]["category"]["id"]
            == category["id"]
        )

    def test_post_categories_id_todos_should_create_link_xml(self):
        category = default["categories"][1]
        todo = default["todos"][1]
        xml_data = "<todo><id>" + todo["id"] + "</id></todo>"
        res = httpx.post(
            categories_url + "/" + category["id"] + "/todos",
            data=xml_data,
            headers=XML_HEADERS,
        )
        assert res.status_code == 201
        res = httpx.get(
            categories_url + "/" + category["id"] + "/todos", headers=XML_HEADERS
        )
        assert xmltodict.parse(res.content)["todos"]["todo"]["id"] == todo["id"]

    def test_post_categories_id_projects_should_create_link_xml(self):
        category = default["categories"][1]
        project = default["projects"][1]
        xml_data = "<project><id>" + project["id"] + "</id></project>"
        res = httpx.post(
            categories_url + "/" + category["id"] + "/projects",
            data=xml_data,
            headers=XML_HEADERS,
        )
        assert res.status_code == 201
        res = httpx.get(
            categories_url + "/" + category["id"] + "/projects", headers=XML_HEADERS
        )
        assert (
            xmltodict.parse(res.content)["projects"]["project"]["id"] == project["id"]
        )
