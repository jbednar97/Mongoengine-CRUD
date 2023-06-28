from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ.get('MONGO_URI', 'mongodb://localhost:27017/todo_db')
}
db = MongoEngine(app)


class Todo(db.Document):
    task = db.StringField(unique=True)
    description = db.StringField()
    done = db.BooleanField()


@app.route("/")
def index():
    return 'This is JSON based backend'


@app.route('/todos')
def list_todos():
    todos = Todo.objects.all()
    return jsonify(todos)


@app.route('/create-todo', methods=['POST'])
def create_todo():
    task = request.form.get("task")
    description = request.form.get('description', False)

    todo = Todo(task=task, description=description, done=False)
    try:
        todo.save()
        return jsonify({'message': 'Todo created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete-todo/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.objects.get_or_404(id=todo_id)
    todo.delete()
    return f'Todo {todo.task} deleted successfully'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
