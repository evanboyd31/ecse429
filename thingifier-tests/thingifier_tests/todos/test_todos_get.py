from thingifier_tests.todos.conftest import *


class TestTodosGet:
    def test_get_todos_should_return_all_todos(self):
        res = httpx.get(todos_url)
        actual = res.json()
        assert res.status_code == 200
        assert contain_the_same_todos(actual, default_todos)
