import time
import httpx
import os
import subprocess

import pytest

url_header : str = "http://localhost:4567/"
dummy_values = {"todo":{"title": "ea commodo consequat", "doneStatus": True, "description": "m dolor sit amet, co"}, "project":{"title": "n reprehenderit in v",  "completed": True,"active": True, "description": "dolor in reprehender"}, "category":{"title": "e irure dolor in rep","description": "ostrud exercitationa"}}
system_state = {"todos":[], "projects":[], "categories":[]}

#Runs once before all tests in the module
@pytest.fixture(scope="module")
def setup_module():
    print("Setting up before all tests in the categories module")
    if make_sure_system_ready() != True:
        print("The system is not ready to be tested.")
        assert False
    save_system_state()
    remove_all()    #Clear all
    yield
    print("Tearing down after all tests in the categories module")
    restore_system_state()

def remove_all():
    todos = httpx.get(url_header + "todos").json()['todos']
    categories = httpx.get(url_header + "categories").json()['categories']
    projects = httpx.get(url_header + "projects").json()['projects']
    
    for todo in todos:
        httpx.delete(url_header + "todos/" + todo['id'])
    for category in categories:
        httpx.delete(url_header + "categories/" + category['id'])
    for project in projects:
        httpx.delete(url_header + "projects/" + project['id'])

def create_one_of_each():
    httpx.post(url_header + "todos", json=dummy_values["todo"])
    httpx.post(url_header + "projects", json=dummy_values["project"])
    httpx.post(url_header + "categories", json=dummy_values["category"])

def save_system_state():
    system_state["todos"] = []
    system_state["projects"] = []
    system_state["categories"] = []

    todos = httpx.get(url_header + "todos").json()['todos']
    categories = httpx.get(url_header + "categories").json()['categories']
    projects = httpx.get(url_header + "projects").json()['projects']

    system_state['todos'] = todos
    system_state['categories'] = categories
    system_state['projects'] = projects

def restore_system_state():
    for todo in system_state['todos']:
        del todo["id"]
        httpx.post(url_header + "todos", json=todo)
    
    for project in system_state['projects']:
        del project["id"]
        httpx.post(url_header + "projects", json=project)
    
    for category in system_state['categories']:
        del category["id"]
        httpx.post(url_header + "categories", json=category)

def make_sure_system_ready():
    try:
        response = httpx.get(url_header + "todos")
        if response.status_code == 200:
            return True
    except httpx.ConnectError as error:
        return False
    
    return False
