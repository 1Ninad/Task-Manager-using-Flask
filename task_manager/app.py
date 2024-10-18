from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import db, Task
from forms import TaskForm
from bst import BST
from sorting import mergeSort
from stack import Stack

# Stack - undo
action_history = Stack()  
# Stack - redo
redo_stack = Stack()  
# BST - taskSearch
tasks_bst = BST()  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    populate_bst_with_tasks()

def populate_bst_with_tasks():
    tasks = Task.query.all()
    for task in tasks:
        tasks_bst.insert((task.title, task))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data
        )
        db.session.add(new_task)
        db.session.commit()
        tasks_bst.insert((new_task.title, new_task))  # BST - taskInsert
        action_history.push(('add', new_task))  # Stack - undoPush
        return redirect(url_for('index'))

    search_query = request.args.get('search', '')
    if search_query:
        tasks = tasks_bst.search(search_query)
        tasks = [task for _, task in tasks]
    else:
        tasks = Task.query.all()

    tasks = mergeSort(tasks, key=lambda task: task.priority)  # Sorting - taskSort

    return render_template('tasks.html', form=form, tasks=tasks, search_query=search_query)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority
        }
        db.session.delete(task)
        db.session.commit()
        action_history.push(('delete', task_data))  # Stack - undoPush
        tasks_bst.remove(task.title)  # BST - taskRemove

    return redirect(url_for('index'))

@app.route('/undo')
def undo():
    if not action_history.is_empty():
        last_action = action_history.pop()  # Stack - undoPop
        action_type = last_action[0]

        if action_type == 'add':
            task = last_action[1]
            db.session.delete(task)
            db.session.commit()
            redo_stack.push(('delete', task))  # Stack - redoPush
        elif action_type == 'delete':
            task_data = last_action[1]
            restored_task = Task(
                id=task_data['id'],
                title=task_data['title'],
                description=task_data['description'],
                priority=task_data['priority']
            )
            db.session.add(restored_task)
            db.session.commit()
            redo_stack.push(('add', restored_task))  # Stack - redoPush

    return redirect(url_for('index'))

@app.route('/redo')
def redo():
    if not redo_stack.is_empty():
        last_action = redo_stack.pop()  # Stack - redoPop
        action_type = last_action[0]

        if action_type == 'add':
            task = last_action[1]
            db.session.add(task)
            db.session.commit()
            action_history.push(('add', task))  # Stack - undoPush
        elif action_type == 'delete':
            task = last_action[1]
            db.session.delete(task)
            db.session.commit()
            action_history.push(('delete', task))  # Stack - undoPush

    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    task = Task.query.get(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        old_task = Task(title=task.title, description=task.description, priority=task.priority)
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        db.session.commit()
        action_history.push(('update', old_task, task))  # Stack - undoPush
        return redirect(url_for('index'))

    return render_template('tasks.html', form=form, tasks=Task.query.all(), updating=True, task=task)

if __name__ == '__main__':
    app.run(debug=True, port=5003)