from flask import Flask, render_template, redirect, url_for, request, jsonify  # Added jsonify import
from models import db, Task
from forms import TaskForm
from bst import BST

# Stack to keep track of actions for undo/redo
action_history = []  # Action history for undo
redo_stack = []  # Stack for redo actions
tasks_bst = BST()  # Initialize the BST at the top level of your file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    populate_bst_with_tasks()  # Populate BST with initial tasks

def populate_bst_with_tasks():
    """Fetch tasks from the database and insert their titles into the BST."""
    tasks = Task.query.all()  # Fetch all tasks from the database
    for task in tasks:
        tasks_bst.insert(task.title)  # Insert each task title into the BST

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        # Create and add the new task
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data
        )
        db.session.add(new_task)
        db.session.commit()
        
        # Insert task title into the BST
        tasks_bst.insert(new_task.title)  # Insert the title into the BST

        # Log the action for undo
        action_history.append(('add', new_task))
        
        return redirect(url_for('index'))

    search_query = request.args.get('search', '')
    tasks = Task.query.filter(Task.title.contains(search_query) | Task.description.contains(search_query)).order_by(Task.priority).all()

    return render_template('tasks.html', form=form, tasks=tasks, search_query=search_query)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        # Create a copy of the task data before deletion
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority
        }
        db.session.delete(task)
        db.session.commit()
        
        # Log the action for undo, storing task data
        action_history.append(('delete', task_data))

        # Optionally, remove task title from the BST (implement remove method if needed)
        # tasks_bst.remove(task.title)

    return redirect(url_for('index'))

@app.route('/undo')
def undo():
    if action_history:
        last_action = action_history.pop()  # Get the last action
        action_type = last_action[0]

        if action_type == 'add':
            # Undo the addition by deleting the task
            task = last_action[1]
            db.session.delete(task)
            db.session.commit()
            redo_stack.append(('delete', task))  # Push the action to redo stack
            
        elif action_type == 'delete':
            # Undo the deletion by adding the task back
            task_data = last_action[1]
            restored_task = Task(
                id=task_data['id'],
                title=task_data['title'],
                description=task_data['description'],
                priority=task_data['priority']
            )
            db.session.add(restored_task)  # Add the deleted task back
            db.session.commit()
            redo_stack.append(('add', restored_task))  # Push the action to redo stack
            
    return redirect(url_for('index'))

@app.route('/redo')
def redo():
    if redo_stack:
        last_action = redo_stack.pop()  # Get the last action to redo
        action_type = last_action[0]
        
        if action_type == 'add':
            # Redo the addition
            task = last_action[1]
            db.session.add(task)
            db.session.commit()
            action_history.append(('add', task))  # Push the action back to the undo stack
            
        elif action_type == 'delete':
            # Redo the deletion
            task = last_action[1]
            db.session.delete(task)
            db.session.commit()
            action_history.append(('delete', task))  # Push the action back to the undo stack
            
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    task = Task.query.get(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        # Log the current state of the task before update for undo functionality
        old_task = Task(title=task.title, description=task.description, priority=task.priority)
        
        # Update the task with new data
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        db.session.commit()

        # Log the action for undo
        action_history.append(('update', old_task, task))  # Log old task and updated task
        return redirect(url_for('index'))

    return render_template('tasks.html', form=form, tasks=Task.query.all(), updating=True, task=task)

# Add the autocomplete endpoint
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '')
    suggestions = tasks_bst.search_prefix(prefix)  # Use the BST to find suggestions
    return jsonify(suggestions)  # Return suggestions as JSON

if __name__ == '__main__':
    app.run(debug=True, port=5003)
