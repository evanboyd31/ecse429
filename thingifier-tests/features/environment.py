import httpx
from steps.shared_steps import *
projects = []
todos = []
categories = []

def before_all(context):
    response = httpx.get(url + "categories")
    categories.extend(response.json()['categories'])

    response = httpx.get(url + "projects")
    projects.extend(response.json()['projects'])

    response = httpx.get(url + "todos")
    todos.extend(response.json()['todos'])

def after_all(context):
    remove_all()
    for category in categories:
        body = {
            'title' : category['title'],
            'description' : category['description']
        }
        response = httpx.post(url + "categories", json=body)
        category['newId'] = response.json()['id']
    
    for project in projects:
        body = {
            'title' : project['title'],
            'completed' : project['completed'] == 'true',
            'active' : project['active'] == 'true',
            'description' : project['description']
        }
        response = httpx.post(url + "projects", json=body)
        project['newId'] = response.json()['id']
    
    for todo in todos:
        body = {
            'title' : todo['title'],
            'doneStatus' : todo['doneStatus'] == 'true',
            'description' : todo['description']
        }
        response = httpx.post(url + "todos", json=body)
        todo['newId'] = response.json()['id']
        
        for projectAssociated in todo.get('tasksof', []):
            newId = [proj['newId'] for proj in projects if proj['id'] == projectAssociated['id']][0]
            body = {
                'id' : newId
            }
            response = httpx.post(f'{url}/todos/{todo['newId']}/tasksof', json=body)
            
        for categoryAssociated in todo.get('categories', []):
            newId = [categ['newId'] for categ in categories if categ['id'] == categoryAssociated['id']][0]
            body = {
                'id' : newId
            }
            response = httpx.post(f'{url}/todos/{todo['newId']}/categories', json=body)
