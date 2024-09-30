import time
import httpx
import os
import subprocess

url_header : str = "http://localhost:4567/"
dummy_values = {"todo":{"title": "ea commodo consequat", "doneStatus": "true", "description": "m dolor sit amet, co"}, "project":{"title": "n reprehenderit in v",  "completed": "true","active": "true", "description": "dolor in reprehender"}, "category":{"title": "e irure dolor in rep","description": "ostrud exercitationa"}}

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

def dummy_values_to_remove():
    httpx.post(url_header + "todos", json=dummy_values["todo"])
    httpx.post(url_header + "projects", json=dummy_values["project"])
    httpx.post(url_header + "categories", json=dummy_values["category"])