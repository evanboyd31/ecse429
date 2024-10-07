from thingifier_tests.interop.conftest import *
import xmltodict

class TestInteropIdGet:
    def test_get_todos_id_projects_should_get_the_associated_project(self):
        todo = default["todos"][0]
        expected = default["projects"][0]["title"]
        res = httpx.get(todos_url + "/" + todo["id"] + "/tasksof")
        actual = res.json()["projects"][0]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_get_todos_id_projects_should_get_the_associated_project_xml(self):
        todo = default["todos"][0]
        expected = default["projects"][0]["title"]
        res = httpx.get(todos_url + "/" + todo["id"] + "/tasksof", headers={"Accept": "application/xml"})
        actual = xmltodict.parse(res.content)["projects"]["project"]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_get_todos_id_categories_should_get_the_associated_categories(self):
        todo = default["todos"][0]
        expected = default["categories"][0]["title"]
        res = httpx.get(todos_url + "/" + todo["id"] + "/categories")
        actual = res.json()["categories"][0]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_get_todos_id_categories_should_get_the_associated_categories_xml(self):
        todo = default["todos"][0]
        expected = default["categories"][0]["title"]
        res = httpx.get(todos_url + "/" + todo["id"] + "/categories", headers={"Accept": "application/xml"})
        actual = xmltodict.parse(res.content)["categories"]["category"]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_get_projects_id_todos_should_get_the_associated_todos(self):
        project = default["projects"][0]
        expected = default["todos"][0]["title"]
        res = httpx.get(projects_url + "/" + project["id"] + "/tasks")
        actual = res.json()["todos"][0]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_get_projects_id_todos_should_get_the_associated_todos_xml(self):
        project = default["projects"][0]
        expected = default["todos"][0]["title"]
        res = httpx.get(projects_url + "/" + project["id"] + "/tasks", headers={"Accept": "application/xml"})
        actual = xmltodict.parse(res.content)["todos"]["todo"]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_get_projects_id_categories_should_get_the_associated_categories(self):
        project = default["projects"][0]
        expected = default["categories"][0]["title"]
        res = httpx.get(projects_url + "/" + project["id"] + "/categories")
        actual = res.json()["categories"][0]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual
    
    def test_get_projects_id_categories_should_get_the_associated_categories_xml(self):
        project = default["projects"][0]
        expected = default["categories"][0]["title"]
        res = httpx.get(projects_url + "/" + project["id"] + "/categories", headers={"Accept": "application/xml"})
        actual = xmltodict.parse(res.content)["categories"]["category"]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual
    
    def test_get_categories_id_todos_should_get_the_associated_todos(self):
        category = default["categories"][0]
        expected = default["todos"][0]["title"]
        res = httpx.get(categories_url + "/" + category["id"] + "/todos")
        actual = res.json()["todos"][0]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual
    
    def test_get_categories_id_todos_should_get_the_associated_todos_xml(self):
        category = default["categories"][0]
        expected = default["todos"][0]["title"]
        res = httpx.get(categories_url + "/" + category["id"] + "/todos", headers={"Accept": "application/xml"})
        actual = xmltodict.parse(res.content)["todos"]["todo"]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_get_categories_id_projects_should_get_the_associated_projects(self):
        category = default["categories"][0]
        expected = default["projects"][0]["title"]
        res = httpx.get(categories_url + "/" + category["id"] + "/projects")
        actual = res.json()["projects"][0]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual
    
    def test_get_categories_id_projects_should_get_the_associated_projects_xml(self):
        category = default["categories"][0]
        expected = default["projects"][0]["title"]
        res = httpx.get(categories_url + "/" + category["id"] + "/projects", headers={"Accept": "application/xml"})
        actual = xmltodict.parse(res.content)["projects"]["project"]["title"]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual
