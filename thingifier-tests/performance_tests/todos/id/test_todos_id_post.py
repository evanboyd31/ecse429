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

    def test_post_todos_id_xml_should_update_the_todo_with_that_id(self):
        body = """
                <todo>
                  <description>Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'</description>
                </todo>"""
        body_dict = xml_to_dict(body)["todo"]

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.post(todos_url + "/" + str(id), content=body, headers=XML_HEADERS)
        todo = xml_to_dict(res.content)["todo"]

        assert res.status_code == 200
        assert todo["title"] == old_todo["title"]
        assert todo["description"] == body_dict["description"]
        assert todo["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + todo["id"]).json()
        assert from_api["todos"][0] == todo

    def test_post_todos_id_with_doneStatus_string_should_fail(self):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": "false",
        }

        id = default_todos["todos"][0]["id"]

        res = httpx.post(todos_url + "/" + str(id), json=body)
        error_messages = res.json()["errorMessages"]

        assert res.status_code == 400
        assert len(error_messages) == 1
        assert error_messages[0] == "Failed Validation: doneStatus should be BOOLEAN"
