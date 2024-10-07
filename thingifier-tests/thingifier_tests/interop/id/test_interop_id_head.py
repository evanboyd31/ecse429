from thingifier_tests.interop.conftest import *


class TestInteropIdHead():
    def test_head_todos_id_projects_should_return_200(self):
        todo = default["todos"][0]
        res = httpx.head(todos_url + "/" + todo["id"] + "/tasksof")
        assert res.status_code == 200
    
    def test_head_todos_id_categories_should_return_200(self):
        todo = default["todos"][0]
        res = httpx.head(todos_url + "/" + todo["id"] + "/categories")
        assert res.status_code == 200

    def test_head_projects_id_todos_should_return_200(self):
        project = default["projects"][0]
        res = httpx.head(projects_url + "/" + project["id"] + "/tasks")
        assert res.status_code == 200

    def test_head_projects_id_categories_should_return_200(self):
        project = default["projects"][0]
        res = httpx.head(projects_url + "/" + project["id"] + "/categories")
        assert res.status_code == 200

    def test_head_categories_id_todos_should_return_200(self):
        category = default["categories"][0]
        res = httpx.head(categories_url + "/" + category["id"] + "/todos")
        assert res.status_code == 200

    def test_head_categories_id_projects_should_return_200(self):
        category = default["categories"][0]
        res = httpx.head(categories_url + "/" + category["id"] + "/projects")
        assert res.status_code == 200

    