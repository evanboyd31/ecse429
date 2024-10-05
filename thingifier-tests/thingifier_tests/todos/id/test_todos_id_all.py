from thingifier_tests.todos.conftest import *


class TestTodosIdAll:
    def test_all_todos_id_with_nonexistent_id_should_give_a_404_status_code(self):
        id = default_todos["todos"][0]["id"]
        common.remove_all()
        calls = [httpx.get, httpx.head, httpx.put, httpx.post, httpx.delete]
        for call in calls:
            res = call(todos_url + "/" + str(id))
            assert res.status_code == 404

    def test_all_todos_id_xml_with_nonexistent_id_should_give_a_404_status_code(self):
        id = default_todos["todos"][0]["id"]
        common.remove_all()
        calls = [httpx.get, httpx.head, httpx.put, httpx.post, httpx.delete]
        for call in calls:
            res = call(todos_url + "/" + str(id), headers=XML_HEADERS)
            assert res.status_code == 404
