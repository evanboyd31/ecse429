from performance_tests.todos.conftest import *


class TestTodosIdDelete:
    def test_delete_todos_id_should_remove_the_todo_with_that_id(self):
        id = default_todos["todos"][0]["id"]
        res = httpx.delete(todos_url + "/" + str(id))
        assert res.status_code == 200

        from_api = httpx.get(todos_url + "/" + "id")
        assert from_api.status_code == 404
