from thingifier_tests.todos.conftest import *


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

    def test_post_todos_with_filter_should_create_a_todo(self):
        body = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": False,
        }

        res = httpx.post(f"{todos_url}?title=Whatever", json=body)
        res_json = res.json()

        assert res.status_code == 201
        assert res_json["title"] == body["title"]
        assert res_json["description"] == body["description"]
        assert res_json["doneStatus"] == "false"

        from_api = httpx.get(todos_url + "/" + res_json["id"]).json()
        assert from_api["todos"][0] == res_json

    def test_post_todos_xml_should_create_a_todo(self):
        body_dict = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": True,
        }

        body = """
                <todo>
                  <title>Listen to Sabrina Carpenter's Latest Album</title>
                  <description>Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'</description>
                  <doneStatus>true</doneStatus>
                </todo>"""

        res: httpx.Response = httpx.post(todos_url, content=body, headers=XML_HEADERS)
        res_dict: dict = xml_to_dict(res.content)["todo"]
        print(res_dict)

        assert res.status_code == 201
        assert res_dict["title"] == body_dict["title"]
        assert res_dict["description"] == body_dict["description"]
        assert res_dict["doneStatus"] == "true"

        from_api = httpx.get(todos_url + "/" + res_dict["id"]).json()
        assert from_api["todos"][0] == res_dict

    def test_post_todos_xml_with_filter_should_create_a_todo(self):
        body_dict = {
            "title": "Listen to Sabrina Carpenter's Latest Album",
            "description": "Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'",
            "doneStatus": True,
        }

        body = """
                <todo>
                  <title>Listen to Sabrina Carpenter's Latest Album</title>
                  <description>Go listen to Sabrina Carpenter's newest album, 'Short n' Sweet.'</description>
                  <doneStatus>true</doneStatus>
                </todo>"""

        res: httpx.Response = httpx.post(
            f"{todos_url}?title=Whatever", content=body, headers=XML_HEADERS
        )
        res_dict: dict = xml_to_dict(res.content)["todo"]
        print(res_dict)

        assert res.status_code == 201
        assert res_dict["title"] == body_dict["title"]
        assert res_dict["description"] == body_dict["description"]
        assert res_dict["doneStatus"] == "true"

        from_api = httpx.get(todos_url + "/" + res_dict["id"]).json()
        assert from_api["todos"][0] == res_dict

    def test_post_todos_with_malformed_json_should_give_status_code_400(self):
        body = '{"title": "Listen to Sabrina Carpenter\'s Latest Album"'
        res = httpx.post(todos_url, content=body)

        assert res.status_code == 400
