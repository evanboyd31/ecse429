from thingifier_tests.todos.conftest import *


class TestTodosHead:
    def test_head_todos_should_return_headers(self):
        res = httpx.head(todos_url)
        headers = res.headers
        assert res.status_code == 200
        assert headers["content-type"] == "application/json"
        assert headers["transfer-encoding"] == "chunked"
        assert headers["server"] == "Jetty(9.4.z-SNAPSHOT)"
