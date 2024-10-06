from thingifier_tests.interop.conftest import *


class TestInteropIdPost:
    def test_post_todos_id_projects_should_return_201(self):
        todo = default["todos"][1]
        project = default["projects"][1]
        res = httpx.post(todos_url + "/" + todo["id"] + "/tasksof", json={"id": project["id"]})
        assert res.status_code == 201
    
    def test_post_todos_id_categories_should_return_201(self):
        todo = default["todos"][1]
        category = default["categories"][1]
        res = httpx.post(todos_url + "/" + todo["id"] + "/categories", json={"id": category["id"]})
        assert res.status_code == 201

    def test_post_projects_id_todos_should_return_201(self):
        project = default["projects"][1]
        todo = default["todos"][1]
        res = httpx.post(projects_url + "/" + project["id"] + "/tasks", json={"id": todo["id"]})
        assert res.status_code == 201
    
    def test_post_projects_id_categories_should_return_201(self):
        project = default["projects"][1]
        category = default["categories"][1]
        res = httpx.post(projects_url + "/" + project["id"] + "/categories", json={"id": category["id"]})
        assert res.status_code == 201

    def test_post_categories_id_todos_should_return_201(self):
        category = default["categories"][1]
        todo = default["todos"][1]
        res = httpx.post(categories_url + "/" + category["id"] + "/todos", json={"id": todo["id"]})
        assert res.status_code == 201

    def test_post_categories_id_projects_should_return_201(self):
        category = default["categories"][1]
        project = default["projects"][1]
        res = httpx.post(categories_url + "/" + category["id"] + "/projects", json={"id": project["id"]})
        assert res.status_code == 201