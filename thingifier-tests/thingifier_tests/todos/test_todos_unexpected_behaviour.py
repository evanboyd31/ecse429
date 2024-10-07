from thingifier_tests.todos.conftest import *


class TestTodosIdPutUnexpected:
    def test_put_todos_id_actually_overwrites_todo_with_that_id_instead_of_updating_the_todo(
        self,
    ):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
        }

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        res_json = res.json()

        assert res.status_code == 200
        assert res_json["title"] == body["title"]
        assert res_json["description"] == old_todo["description"]
        assert res_json["doneStatus"] == old_todo["description"]

    def test_put_todos_id_xml_actually_overwrites_todo_with_that_id_instead_of_updating_the_todo(
        self,
    ):
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
        assert todo["description"] == old_todo["description"]
        assert todo["doneStatus"] == "false"

    def test_put_todos_id_with_integer_id_works_but_actually_does_not_change_the_id(
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
        assert res_json["id"] == body["id"]

    def test_put_todos_id_xml_with_integer_id_works_but_actually_does_not_change_the_id(
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
        assert todo["id"] == 100

    def test_put_todos_id_without_a_title_actually_fails_to_update_the_todo_instead_of_updating_it(
        self,
    ):
        body = {
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
        }

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.put(todos_url + "/" + str(id), json=body)
        res_json = res.json()

        assert res.status_code == 200
        assert res_json["description"] == old_todo["description"]

    def test_put_todos_id_xml_without_a_title_fails_to_update_the_todo_instead_of_updating_it(
        self,
    ):
        body = """
        <todo><description>Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'</description></todo>
        """

        body_dict = xml_to_dict(body)["todo"]

        old_todo = default_todos["todos"][0]
        id = old_todo["id"]

        res = httpx.put(todos_url + "/" + str(id), content=body, headers=XML_HEADERS)
        todo = xml_to_dict(res.content)["todo"]

        assert res.status_code == 200
        assert todo["description"] == old_todo["description"]
