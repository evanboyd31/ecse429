import httpx
import pytest
import thingifier_tests.test_common as common

todos_url: str = "http://localhost:4567/todos"

# Note that ids will change every time
default_todos: dict = {
    "todos": [
        {
            "id": "???",
            "title": "Watch Sabrina Carpenter Concert Clips",
            "doneStatus": "false",
            "description": "",
        },
        {
            "id": "???",
            "title": "Buy Sabrina Carpenter Merch",
            "doneStatus": "false",
            "description": "",
        },
        {
            "id": "???",
            "title": "Buy Sabrina Carpenter Concert Tickets",
            "doneStatus": "false",
            "description": "",
        },
    ]
}


def contain_the_same_todos(todos1, todos2) -> bool:
    todos1 = todos1["todos"]
    todos2 = todos2["todos"]

    todos1 = sorted(todos1, key=lambda todo: todo["id"])
    todos2 = sorted(todos2, key=lambda todo: todo["id"])
    return todos1 == todos2


@pytest.fixture(autouse=True, scope="module")
def before_each():
    common.remove_all()
    titles: list[str] = [
        "Watch Sabrina Carpenter Concert Clips",
        "Buy Sabrina Carpenter Merch",
        "Buy Sabrina Carpenter Concert Tickets",
    ]

    def add_to_todos(title: str):
        res = httpx.post(todos_url, json={"title": title})
        todo = list(
            filter(lambda todo: todo["title"] == title, default_todos["todos"])
        )[0]
        todo["id"] = res.json()["id"]

    for title in titles:
        add_to_todos(title)


class TestTodos:
    def test_get_todos_should_return_all_todos(self):
        res = httpx.get(todos_url)
        actual = res.json()
        assert res.status_code == 200
        assert contain_the_same_todos(actual, default_todos)

    def test_head_todos_should_return_headers(self):
        res = httpx.head(todos_url)
        headers = res.headers
        assert res.status_code == 200
        assert headers["content-type"] == "application/json"
        assert headers["transfer-encoding"] == "chunked"
        assert headers["server"] == "Jetty(9.4.z-SNAPSHOT)"

    def test_post_todos_should_create_a_todo(self):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": False,
        }

        res = httpx.post(todos_url, json=body)
        res_json = res.json()

        assert res.status_code == 201
        assert res_json["title"] == body["title"]
        assert res_json["description"] == body["description"]
        assert res_json["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + res_json["id"]).json()
        assert from_api["todos"][0] == res_json


class TestTodosId:
    def test_get_todos_id_should_get_the_todo_with_that_id(self):
        expected = default_todos["todos"][0]
        res = httpx.get(todos_url + "/" + expected["id"])
        actual = res.json()["todos"][0]
        assert res.status_code == 200
        print(actual, expected)
        assert expected == actual

    def test_head_todos_id_should_return_headers(self):
        todo = default_todos["todos"][0]
        res = httpx.head(todos_url + "/" + str(todo["id"]))
        headers = res.headers
        assert res.status_code == 200
        assert headers["content-type"] == "application/json"
        assert headers["transfer-encoding"] == "chunked"
        assert headers["server"] == "Jetty(9.4.z-SNAPSHOT)"

    def test_post_todos_id_should_update_the_todo_with_that_id(self):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": False,
        }

        id = default_todos["todos"][0]["id"]

        res = httpx.post(todos_url + "/" + str(id), json=body)
        res_json = res.json()

        assert res.status_code == 200
        assert res_json["title"] == body["title"]
        assert res_json["description"] == body["description"]
        assert res_json["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + res_json["id"]).json()
        assert from_api["todos"][0] == res_json

    def test_put_todos_id_should_update_the_todo_with_that_id(self):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": False,
        }

        id = default_todos["todos"][0]["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        res_json = res.json()

        assert res.status_code == 200
        assert res_json["title"] == body["title"]
        assert res_json["description"] == body["description"]
        assert res_json["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + res_json["id"]).json()
        assert from_api["todos"][0] == res_json

    def test_delete_todos_id_should_remove_the_todo_with_that_id(self):
        id = default_todos["todos"][0]["id"]
        res = httpx.delete(todos_url + "/" + str(id))
        assert res.status_code == 200

        from_api = httpx.get(todos_url + "/" + "id")
        assert from_api.status_code == 404

    def test_todo_calls_with_id_404_if_id_does_not_exist(self):
        id = default_todos["todos"][0]["id"]
        common.remove_all()
        calls = [httpx.get, httpx.head, httpx.put, httpx.post, httpx.delete]
        for call in calls:
            res = call(todos_url + "/" + str(id))
            assert res.status_code == 404
