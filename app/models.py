from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    projectName = db.Column(db.String(100), nullable=False)
    clientId = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', back_populates='projects')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taskName = db.Column(db.String(100), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    dueDate = db.Column(db.DateTime, nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', back_populates='tasks')

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoiceNumber = db.Column(db.String(50), unique=True, nullable=False)
    fileUrl = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    dueDate = db.Column(db.DateTime, nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', back_populates='invoices')

Client.projects = db.relationship('Project', order_by=Project.id, back_populates='client')
Project.tasks = db.relationship('Task', order_by=Task.id, back_populates='project')
Project.invoices = db.relationship('Invoice', order_by=Invoice.id, back_populates='project')
