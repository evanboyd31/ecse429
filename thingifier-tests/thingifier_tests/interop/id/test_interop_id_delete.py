from thingifier_tests.interop.conftest import *


class TestInteropIdDelete:
    def test_delete_todos_id_projects_should_remove_link(self):
        todo = default["todos"][0]
        project = default["projects"][0]
        res = httpx.delete(todos_url + "/" + todo["id"] + "/tasksof/" + project["id"])
        assert res.status_code == 200
        res = httpx.get(todos_url + "/" + todo["id"] + "/tasksof")
        assert res.json()["projects"] == []

    def test_delete_todos_id_categories_should_remove_link(self):
        todo = default["todos"][0]
        category = default["categories"][0]
        res = httpx.delete(
            todos_url + "/" + todo["id"] + "/categories/" + category["id"]
        )
        assert res.status_code == 200
        res = httpx.get(todos_url + "/" + todo["id"] + "/categories")
        assert res.json()["categories"] == []

    def test_delete_projects_id_todos_should_remove_link(self):
        project = default["projects"][0]
        todo = default["todos"][0]
        res = httpx.delete(projects_url + "/" + project["id"] + "/tasks/" + todo["id"])
        assert res.status_code == 200
        res = httpx.get(projects_url + "/" + project["id"] + "/tasks")
        assert res.json()["todos"] == []

    def test_delete_projects_id_categories_should_remove_link(self):
        project = default["projects"][0]
        category = default["categories"][0]
        res = httpx.delete(
            projects_url + "/" + project["id"] + "/categories/" + category["id"]
        )
        assert res.status_code == 200
        res = httpx.get(projects_url + "/" + project["id"] + "/categories")
        assert res.json()["categories"] == []

    def test_delete_categories_id_todos_should_remove_link(self):
        category = default["categories"][0]
        todo = default["todos"][0]
        res = httpx.delete(
            categories_url + "/" + category["id"] + "/todos/" + todo["id"]
        )
        assert res.status_code == 200
        res = httpx.get(categories_url + "/" + category["id"] + "/todos")
        assert res.json()["todos"] == []

    def test_delete_categories_id_projects_should_remove_link(self):
        category = default["categories"][0]
        project = default["projects"][0]
        res = httpx.delete(
            categories_url + "/" + category["id"] + "/projects/" + project["id"]
        )
        assert res.status_code == 200
        res = httpx.get(categories_url + "/" + category["id"] + "/projects")
        assert res.json()["projects"] == []
