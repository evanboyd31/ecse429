from thingifier_tests.todos.conftest import *


class TestTodosIdHead():
    def test_head_todos_id_should_return_headers(self):
        todo = default_todos["todos"][0]
        res = httpx.head(todos_url + "/" + str(todo["id"]))
        headers = res.headers
        assert res.status_code == 200
        assert headers["content-type"] == "application/json"
        assert headers["transfer-encoding"] == "chunked"
        assert headers["server"] == "Jetty(9.4.z-SNAPSHOT)"
