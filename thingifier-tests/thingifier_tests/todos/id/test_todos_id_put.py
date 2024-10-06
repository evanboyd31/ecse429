from thingifier_tests.todos.conftest import *


class TestTodosIdPut:
    def test_put_todos_id_with_string_id_in_body_should_fail(self):
        body = {
            "id": "This is a string",
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": False,
        }

        id = default_todos["todos"][0]["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        error_messages = res.json()["errorMessages"]

        assert res.status_code == 400
        assert len(error_messages) == 1
        assert error_messages[0] == "Failed Validation: id should be ID"

    def test_put_todos_id_with_doneStatus_string_should_fail(self):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": "false",
        }

        id = default_todos["todos"][0]["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        error_messages = res.json()["errorMessages"]

        assert res.status_code == 400
        assert len(error_messages) == 1
        assert error_messages[0] == "Failed Validation: doneStatus should be BOOLEAN"


class TestTodosIdPutBug:
    def test_put_todos_id_should_replace_the_todo_with_that_id_bug(self):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
        }

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        res_json = res.json()

        assert res.status_code == 200
        assert res_json["title"] == body["title"]
        assert res_json["description"] == ""
        assert res_json["description"] != old_todo["description"]
        assert res_json["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + res_json["id"]).json()
        assert from_api["todos"][0] == res_json
        assert from_api["todos"][0] != old_todo

    def test_put_todos_id_xml_should_replace_the_todo_with_that_id_bug(self):
        body = """
                <todo>
                  <title>Listen to Sabrina Carpenter's Latest Album</title>
                </todo>"""
        body_dict = xml_to_dict(body)["todo"]

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.put(todos_url + "/" + str(id), content=body, headers=XML_HEADERS)
        todo = xml_to_dict(res.content)["todo"]

        assert res.status_code == 200
        assert todo["title"] == body_dict["title"]
        assert todo["description"] == None
        assert todo["description"] != old_todo["description"]
        assert todo["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + todo["id"]).json()
        from_api_todo = from_api["todos"][0]
        assert from_api_todo != old_todo
        if from_api_todo["description"] == "":
            from_api_todo["description"] = None
        assert from_api["todos"][0] == todo

    def test_put_todos_id_with_integer_id_in_body_should_work_but_not_change_id_bug(
        self,
    ):
        body = {
            "id": 100,
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": False,
        }

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        res_json = res.json()

        assert res.status_code == 200
        assert res_json["id"] == old_todo["id"]
        assert res_json["id"] != body["id"]

        from_api = httpx.get(todos_url + "/" + res_json["id"]).json()
        assert from_api["todos"][0] == res_json

    def test_put_todos_id_xml_with_integer_id_in_body_should_work_but_not_change_id_bug(
        self,
    ):
        body = """
        <todo>
        <id>100</id>
        <title>Listen to Sabrina Carpenter's Latest Album</title>
        </todo>
        """

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.put(todos_url + "/" + str(id), content=body, headers=XML_HEADERS)
        todo = xml_to_dict(res.content)["todo"]

        assert res.status_code == 200
        assert todo["id"] == old_todo["id"]
        assert todo["id"] != 100

        from_api = httpx.get(todos_url + "/" + old_todo["id"]).json()
        from_api_todo = from_api["todos"][0]
        assert from_api_todo != old_todo
        if from_api_todo["description"] == "":
            from_api_todo["description"] = None
        assert from_api["todos"][0] == todo

    def test_put_todos_id_without_a_title_should_fail_bug(self):
        body = {
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
        }

        id = default_todos["todos"][0]["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        error_messages = res.json()["errorMessages"]

        assert res.status_code == 400
        assert len(error_messages) == 1
        assert error_messages[0] == "title : field is mandatory"

    def test_put_todos_id_xml_without_a_title_should_fail_bug(self):
        body = """
        <todo><description>Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'</description></todo>
        """

        id = default_todos["todos"][0]["id"]

        res = httpx.put(todos_url + "/" + str(id), content=body, headers=XML_HEADERS)
        res_json = xml_to_dict(res.content)
        error_messages = res_json["errorMessages"]

        assert res.status_code == 400
        assert error_messages["errorMessage"] == "title : field is mandatory"
