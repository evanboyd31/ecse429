import httpx
from thingifier_tests.todos.conftest import *

class TestTodosDelete:
  def test_delete_todos_should_not_be_allowed(self):
    response = httpx.delete(todos_url)
    assert response.status_code == 405
    assert todos_has_not_changed()

    
  def test_delete_todos_xml_should_not_be_allowed(self):
    response = httpx.delete(todos_url, headers=XML_HEADERS)
    assert response.status_code == 405
    assert todos_has_not_changed()
    

  def test_delete_todos_with_filter_should_not_be_allowed(before_each):
    response = httpx.delete(f"{todos_url}?title={default_todos["todos"][0].get("title")}")
    assert response.status_code == 405
    assert todos_has_not_changed()

    
  def test_delete_project_using_filter_xml(before_each):
    response = httpx.delete(f"{todos_url}?title={default_todos["todos"][0].get("title")}", headers=XML_HEADERS)
    assert response.status_code == 405
    assert todos_has_not_changed()
