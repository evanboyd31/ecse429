import httpx

url : str = "http://localhost:4567/"

def test_lol():
    assert 1 == 1

class TestGrouping():
    def test_group1(self):
        assert True

    def not_run(self):
        assert False

def will_not_be_run():
    assert 1 == 2


class TestTodos():
    def test_get_todos(self):
        response : httpx.Response = httpx.get(url + "todos")
        expected : dict = {'todos': [{'id': '2', 'title': 'file paperwork', 'doneStatus': 'false', 'description': '', 'tasksof': [{'id': '1'}]}, {'id': '1', 'title': 'scan paperwork', 'doneStatus': 'false', 'description': '', 'categories': [{'id': '1'}], 'tasksof': [{'id': '1'}]}]}
        assert response.json() == expected 
