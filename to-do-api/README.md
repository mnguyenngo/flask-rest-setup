# To Do API

[Flask RESTful Documentation](http://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api)

___

## Usage

### Creating Resources
```python
# Todo
# shows a single todo item and lets you updatae or delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        """Return the specified todo item given the todo_id"""
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        """Deletes an existing task"""
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        # 204: SUCCESS; NO FURTHER CONTENT
        return '', 204

    def put(self, todo_id):
        """Updates existing task"""

        # parser
        abort_if_todo_doesnt_exist(todo_id)
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        # 201: CREATED
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        """Return the current TODO dictionary"""
        return TODOS

    def post(self):
        """Adds task to TODO"""
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        # 201: CREATED
        return TODOS[todo_id], 201
```

### Routing to your Resources
Route the URL to the resource classes.
```python
# Setup the Api resource routing here
api.add_resource(TodoList, '/todos')
# <todo_id> is passed as an argument to the methods of the Todo class
api.add_resource(Todo, '/todos/<todo_id>')
```

### Request Argument Parsing
[Request Parsing Docs](https://flask-restful.readthedocs.io/en/0.3.5/reqparse.html)

##### Setup
Create a parser object and add the argument name 'task':
```python
# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('task')
```

##### Make Request (User)


In terminal:
```bash
curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v
```

With Python using Requests:
```python
requests.put('http://localhost:5000/todos/todo1', data={'task': 'Remember the milk'}).json()
```

##### Parsing Request (API)
args is a dictionary of the data that is passed through requests or curl.
```python
args = parser.parse_args()
task = {'task': args['task']}
# add task to the TODOS dictionary
TODOS[todo_id] = task
```


### Aborting a Request
#### Function Definition
```python
def abort_if_todo_doesnt_exist(todo_id):
    """Abort request if todo_id does not exist in TODOS"""
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))
```

#### Implement in a request method
```python
def delete(self, todo_id):
    """Deletes an existing task"""
    abort_if_todo_doesnt_exist(todo_id)
    del TODOS[todo_id]
    # 204: SUCCESS; NO FURTHER CONTENT
    return '', 204
```
