import httpx
from thingifier_tests.todos.conftest import *


class TestTodosPut:
    def test_put_todos_should_not_be_allowed(self):
        response = httpx.put(todos_url)
        assert response.status_code == 405
        assert todos_has_not_changed()

    def test_put_todos_xml_should_not_be_allowed(self):
        response = httpx.put(todos_url, headers=XML_HEADERS)
        assert response.status_code == 405
        assert todos_has_not_changed()

    def test_put_todos_with_filter_should_not_be_allowed(self):
        response = httpx.put(
            f"{todos_url}?title={default_todos["todos"][0].get("title")}"
        )
        assert response.status_code == 405
        assert todos_has_not_changed()

    def test_put_project_using_filter_xml(self):
        response = httpx.put(
            f"{todos_url}?title={default_todos["todos"][0].get("title")}",
            headers=XML_HEADERS,
        )
        assert response.status_code == 405
        assert todos_has_not_changed()
