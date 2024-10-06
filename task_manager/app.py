from flask import Flask, render_template, redirect, url_for, request
from models import db, Task
from forms import TaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        print(f"Title: {form.title.data}, Description: {form.description.data}, Priority: {form.priority.data}")  # Debug
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data
        )
        db.session.add(new_task)
        db.session.commit()
        print("New task added.")  # Debug
        return redirect(url_for('index'))

    search_query = request.args.get('search', '')
    tasks = Task.query.filter(Task.title.contains(search_query) | Task.description.contains(search_query)).order_by(Task.priority).all()
    print(f"Tasks retrieved: {tasks}")  # Debug

    return render_template('tasks.html', form=form, tasks=tasks, search_query=search_query)


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    task = Task.query.get(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data  # Update priority
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('tasks.html', form=form, tasks=Task.query.all(), updating=True, task=task)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
