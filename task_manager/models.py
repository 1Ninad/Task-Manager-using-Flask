from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    priority = db.Column(db.Integer, nullable=False)  # New field for priority

    def __repr__(self):
        return f'<Task {self.title}, Priority {self.priority}>'