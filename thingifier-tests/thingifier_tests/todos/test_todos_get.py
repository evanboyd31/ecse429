from httpx import head
from thingifier_tests.todos.conftest import *


class TestTodosGet:
    def test_get_todos_should_return_all_todos(self):
        res = httpx.get(todos_url)
        actual = res.json()
        assert res.status_code == 200
        print(actual)
        print("00000")
        print(default_todos)
        assert contain_the_same_todos(actual, default_todos)

    def test_get_todos_xml_should_return_all_todos(self):
        response = httpx.get(todos_url, headers=XML_HEADERS)
        assert response.status_code == 200
        actual = xml_to_dict(response.content).get("todos")
        assert contain_the_same_todos(actual, get_default_todos_for_xml())

    def test_get_todos_filter_by_title_should_return_todos_with_that_title(self):
        todo = default_todos["todos"][0]

        response = httpx.get(f"{todos_url}?title={todo.get("title")}")

        assert response.status_code == 200
        list_todos = response.json()["todos"]
        assert len(list_todos) == 1

        actual = list_todos[0]
        assert actual == todo

    def test_get_todos_xml_filter_by_title_should_return_todos_with_that_title(self):
        todo = default_todos["todos"][0]

        response = httpx.get(
            f"{todos_url}?title={todo.get("title")}", headers=XML_HEADERS
        )

        assert response.status_code == 200
        actual = xml_to_dict(response.content)["todos"]["todo"]

        assert actual == todo

    def test_get_todos_filter_by_description_should_return_todos_with_that_description(
        self,
    ):
        todo = default_todos["todos"][0]

        response = httpx.get(f"{todos_url}?description={todo.get("description")}")

        assert response.status_code == 200
        list_todos = response.json()["todos"]
        assert len(list_todos) == 1

        actual = list_todos[0]
        assert actual == todo

    def test_get_todos_xml_filter_by_description_should_return_todos_with_that_description(
        self,
    ):
        todo = default_todos["todos"][0]

        response = httpx.get(
            f"{todos_url}?description={todo.get("description")}", headers=XML_HEADERS
        )

        assert response.status_code == 200
        actual = xml_to_dict(response.content)["todos"]["todo"]

        assert actual == todo

    def test_get_todos_filter_by_id_should_return_todos_with_that_id(self):
        todo = default_todos["todos"][0]

        response = httpx.get(f"{todos_url}?id={todo.get("id")}")

        assert response.status_code == 200
        list_todos = response.json()["todos"]
        assert len(list_todos) == 1

        actual = list_todos[0]
        assert actual == todo

    def test_get_todos_xml_filter_by_id_should_return_todos_with_that_id(self):
        todo = default_todos["todos"][0]

        response = httpx.get(f"{todos_url}?id={todo.get("id")}", headers=XML_HEADERS)

        assert response.status_code == 200
        actual = xml_to_dict(response.content)["todos"]["todo"]

        assert actual == todo

    def test_get_todos_filter_by_multiple_should_return_todos_that_match_all_filters(
        self,
    ):
        todo = default_todos["todos"][0]

        response = httpx.get(
            f"{todos_url}?id={todo.get("id")}&description={todo.get("description")}"
        )

        assert response.status_code == 200
        list_todos = response.json()["todos"]
        assert len(list_todos) == 1

        actual = list_todos[0]
        assert actual == todo

    def test_get_todos_xml_filter_by_multiple_should_return_todos_that_match_all_filters(
        self,
    ):
        todo = default_todos["todos"][0]

        response = httpx.get(
            f"{todos_url}?id={todo.get("id")}&description={todo.get("description")}",
            headers=XML_HEADERS,
        )

        assert response.status_code == 200
        actual = xml_to_dict(response.content)["todos"]["todo"]

        assert actual == todo
