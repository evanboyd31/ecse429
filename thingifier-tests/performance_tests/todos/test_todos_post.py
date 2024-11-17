from performance_tests.todos.conftest import *


class TestTodosPost:
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
