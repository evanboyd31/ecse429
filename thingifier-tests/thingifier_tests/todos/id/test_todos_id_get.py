from thingifier_tests.todos.conftest import *


class TestTodosIdGet:
    def test_get_todos_id_should_get_the_todo_with_that_id(self):
        expected = default_todos["todos"][0]
        res = httpx.get(todos_url + "/" + expected["id"])
        actual = res.json()["todos"][0]
        assert res.status_code == 200
        assert expected == actual
