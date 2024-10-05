from thingifier_tests.todos.conftest import *


class TestTodosIdPut:
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
