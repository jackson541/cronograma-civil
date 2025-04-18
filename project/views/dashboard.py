from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from project.views.project.open_projects import NotConcludedProjectsScreen
from project.views.project.closed_projects import ConcludedProjectsScreen
from project.views.project.add_project import AddProjectScreen
from project.views.project.project_details import ProjectDetailsScreen
from project.views.project.edit_project import EditProjectScreen
from project.views.client.new_client import NewClientScreen
from project.views.client.list_clients import ListClientScreen
from project.views.client.edit_client import EditClientScreen
from project.views.service.create_service import CreateServiceScreen
from project.views.service.service_details import ServiceDetailsScreen
from project.views.service.edit_service import EditServiceScreen
from project.views.task.add_task import CreateTaskScreen
from project.views.task.task_details import TaskDetailsScreen
from project.views.task.edit_task import EditTaskScreen


class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Project Manager")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create screens
        self.project_screen = NotConcludedProjectsScreen(self.session, self)
        self.new_client_screen = NewClientScreen(self.session, self)
        self.list_client_screen = ListClientScreen(self.session, self)
        self.closed_projects_screen = ConcludedProjectsScreen(self.session, self)
        self.add_project_screen = AddProjectScreen(self.session, self)
        self.project_details_screen = ProjectDetailsScreen(self.session, self)
        self.create_service_screen = CreateServiceScreen(self.session, self)
        self.service_details_screen = ServiceDetailsScreen(self.session, self)
        self.create_task_screen = CreateTaskScreen(self.session, self)
        self.task_details_screen = TaskDetailsScreen(self.session, self)
        self.edit_client_screen = EditClientScreen(self.session, self)
        self.edit_project_screen = EditProjectScreen(self.session, self)
        self.edit_service_screen = EditServiceScreen(self.session, self)
        self.edit_task_screen = EditTaskScreen(self.session, self)

        # Add screens to the stack
        self.stack.addWidget(self.project_screen)       # index 0
        self.stack.addWidget(self.new_client_screen)    # index 1
        self.stack.addWidget(self.list_client_screen)   # index 2
        self.stack.addWidget(self.closed_projects_screen)
        self.stack.addWidget(self.add_project_screen)
        self.stack.addWidget(self.project_details_screen)
        self.stack.addWidget(self.create_service_screen)
        self.stack.addWidget(self.service_details_screen)
        self.stack.addWidget(self.create_task_screen)
        self.stack.addWidget(self.task_details_screen)
        self.stack.addWidget(self.edit_client_screen)
        self.stack.addWidget(self.edit_project_screen)
        self.stack.addWidget(self.edit_service_screen)
        self.stack.addWidget(self.edit_task_screen)


        # Show the first screen
        self.stack.setCurrentIndex(0)

    def show_project_screen(self):
        self.project_screen.load_projects()
        self.stack.setCurrentIndex(0)

    def show_new_client_screen(self):
        self.stack.setCurrentIndex(1)

    def show_list_client_screen(self):
        self.list_client_screen.load_clients()
        self.stack.setCurrentIndex(2)

    def show_concluded_projects_screen(self):
        self.closed_projects_screen.load_projects()
        self.stack.setCurrentIndex(3)

    def show_add_project_screen(self):
        self.add_project_screen.load_clients()
        self.stack.setCurrentIndex(4)

    def show_project_details_screen(self, project_id):
        self.project_details_screen.load_project(project_id)
        self.stack.setCurrentWidget(self.project_details_screen)

    def show_create_service_screen(self, project_id):
        self.create_service_screen.load_project(project_id)
        self.stack.setCurrentWidget(self.create_service_screen)

    def show_service_details_screen(self, service_id):
        self.service_details_screen.load_service(service_id)
        self.stack.setCurrentWidget(self.service_details_screen)

    def show_create_task_screen(self, service_id):
        self.create_task_screen.load_service(service_id)
        self.stack.setCurrentWidget(self.create_task_screen)

    def show_task_details_screen(self, task_id):
        self.task_details_screen.load_task(task_id)
        self.stack.setCurrentWidget(self.task_details_screen)

    def show_edit_client_screen(self, client_id):
        self.edit_client_screen.load_client(client_id)
        self.stack.setCurrentWidget(self.edit_client_screen)

    def show_edit_project_screen(self, project_id):
        self.edit_project_screen.load_project(project_id)
        self.stack.setCurrentWidget(self.edit_project_screen)

    def show_edit_service_screen(self, service_id):
        self.edit_service_screen.load_service(service_id)
        self.stack.setCurrentWidget(self.edit_service_screen)

    def show_edit_task_screen(self, task_id):
        self.edit_task_screen.load_task(task_id)
        self.stack.setCurrentWidget(self.edit_task_screen)
