from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    """Abort request if todo_id does not exist in TODOS"""
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you updatae or delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        """Return the specified todo item given the todo_id

        Example:
            # In the terminal
            $ curl http://localhost:5000/todos/todo1

            OR

            # Python
            requests.get('http://localhost:5000/todos/todo1').json()
        """
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        """Deletes an existing task

        Example:
            # In the terminal
            $ curl http://localhost:5000/todos/todo1 -X DELETE -v

            OR

            # Python
            requests.delete('http://localhost:5000/todos/todo4')
        """
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        # 204: SUCCESS; NO FURTHER CONTENT
        return '', 204

    def put(self, todo_id):
        """Updates existing task

        Example:
            # In the terminal
            $ curl http://localhost:5000/todos/todo1 -d "task=Remember the milk" -X PUT -v

            OR

            # Python
            requests.put('http://localhost:5000/todos/todo1',
                         data={'task': 'Remember the milk'}).json()
        """

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
        """Return the current TODO dictionary

        Example:
            # In the terminal
            $ curl http://localhost:5000/todos

            OR

            # Python
            requests.get('http://localhost:5000/todos').json()
        """
        return TODOS

    def post(self):
        """Adds task to TODO

        Example:
            # In the terminal
            $ curl http://localhost:5000/todos -d "task=Remember the milk" -X POST -v

            OR

            # Python
            requests.post('http://localhost:5000/todos',
                         data={'task': 'Remember the milk'}).json()
        """
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        # 201: CREATED
        return TODOS[todo_id], 201


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
