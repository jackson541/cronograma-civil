from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Boolean, JSON
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    projects = relationship('Project', back_populates='client')


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    concluded = Column(Boolean, default=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='projects')
    services = relationship('Service', back_populates='project')

# Association table for service dependencies
service_dependencies = Table(
    'service_dependencies', Base.metadata,
    Column('service_id', Integer, ForeignKey('services.id'), primary_key=True),
    Column('depends_on_id', Integer, ForeignKey('services.id'), primary_key=True)
)

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    days_to_complete = Column(Integer, default=0)
    chart_data = Column(JSON)
    project = relationship('Project', back_populates='services')
    tasks = relationship('Task', back_populates='service')

    # Self-referencing many-to-many
    dependencies = relationship(
        'Service',
        secondary=service_dependencies,
        primaryjoin=id==service_dependencies.c.service_id,
        secondaryjoin=id==service_dependencies.c.depends_on_id,
        backref='dependents'
    )


# Association table for task dependencies
task_dependencies = Table(
    'task_dependencies',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('depends_on_id', Integer, ForeignKey('tasks.id'), primary_key=True)
)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    days_to_complete = Column(Integer)
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship('Service', back_populates='tasks')

    # Tasks this task depends on
    dependencies = relationship(
        'Task',
        secondary=task_dependencies,
        primaryjoin=id==task_dependencies.c.task_id,
        secondaryjoin=id==task_dependencies.c.depends_on_id,
        backref='dependents'  # Tasks that depend on this task
    )


engine = create_engine('sqlite:///project.db')
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session instance
session = Session()
