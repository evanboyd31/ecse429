from performance_tests.todos.conftest import *


class TestTodosIdPost:
    def test_post_todos_id_should_update_the_todo_with_that_id(self):
        body = {
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
        }

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.post(todos_url + "/" + str(id), json=body)
        res_json = res.json()

        assert res.status_code == 200
        assert res_json["title"] == old_todo["title"]
        assert res_json["description"] == body["description"]
        assert res_json["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + res_json["id"]).json()
        assert from_api["todos"][0] == res_json
