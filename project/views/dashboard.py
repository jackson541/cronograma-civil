from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from project.views.project.open_projects import NotConcludedProjectsScreen
from project.views.project.closed_projects import ConcludedProjectsScreen
from project.views.project.add_project import AddProjectScreen
from project.views.project.project_details import ProjectDetailsScreen
from project.views.project.edit_project import EditProjectScreen
from project.views.project.delete_project import DeleteProjectScreen

from project.views.client.new_client import NewClientScreen
from project.views.client.list_clients import ListClientScreen
from project.views.client.edit_client import EditClientScreen
from project.views.client.client_details import ClientDetailsScreen
from project.views.client.delete_client import DeleteClientScreen

from project.views.service.create_service import CreateServiceScreen
from project.views.service.service_details import ServiceDetailsScreen
from project.views.service.edit_service import EditServiceScreen
from project.views.service.delete_service import DeleteServiceScreen

from project.views.task.add_task import CreateTaskScreen
from project.views.task.edit_task import EditTaskScreen
from project.views.task.delete_task import DeleteTaskScreen

from project.views.templates.template_list import TemplateListScreen
from project.views.templates.add_template import AddTemplateScreen
from project.views.templates.template_details import TemplateDetailsScreen
from project.views.templates.create_from_template import CreateFromTemplateScreen
from project.views.templates.add_template_service import AddTemplateServiceScreen
from project.views.templates.delete_template import DeleteTemplateScreen


class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Gerenciador de Projetos")

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
        self.edit_client_screen = EditClientScreen(self.session, self)
        self.client_details_screen = ClientDetailsScreen(self.session, self)
        self.delete_client_screen = DeleteClientScreen(self.session, self)
        self.edit_project_screen = EditProjectScreen(self.session, self)
        self.edit_service_screen = EditServiceScreen(self.session, self)
        self.edit_task_screen = EditTaskScreen(self.session, self)
        self.delete_task_screen = DeleteTaskScreen(self.session, self)
        self.delete_service_screen = DeleteServiceScreen(self.session, self)
        self.delete_project_screen = DeleteProjectScreen(self.session, self)
        
        # Template screens
        self.template_list_screen = TemplateListScreen(self.session, self)
        self.add_template_screen = AddTemplateScreen(self.session, self)
        self.template_details_screen = TemplateDetailsScreen(self.session, self)
        self.create_from_template_screen = CreateFromTemplateScreen(self.session, self)
        self.add_template_service_screen = AddTemplateServiceScreen(self.session, self)
        self.delete_template_screen = DeleteTemplateScreen(self.session, self)

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
        self.stack.addWidget(self.edit_client_screen)
        self.stack.addWidget(self.client_details_screen)
        self.stack.addWidget(self.delete_client_screen)
        self.stack.addWidget(self.edit_project_screen)
        self.stack.addWidget(self.edit_service_screen)
        self.stack.addWidget(self.edit_task_screen)
        self.stack.addWidget(self.delete_task_screen)
        self.stack.addWidget(self.delete_service_screen)
        self.stack.addWidget(self.delete_project_screen)
        self.stack.addWidget(self.template_list_screen)
        self.stack.addWidget(self.add_template_screen)
        self.stack.addWidget(self.template_details_screen)
        self.stack.addWidget(self.create_from_template_screen)
        self.stack.addWidget(self.add_template_service_screen)
        self.stack.addWidget(self.delete_template_screen)

        # Show the first screen
        self.show_project_screen()

    def show_project_screen(self):
        self.project_screen.load_clients()
        self.project_screen.load_projects()
        self.stack.setCurrentIndex(0)

    def show_new_client_screen(self):
        self.stack.setCurrentIndex(1)

    def show_list_client_screen(self):
        self.list_client_screen.load_clients()
        self.stack.setCurrentWidget(self.list_client_screen)
        
    def show_client_details_screen(self, client_id):
        self.client_details_screen.load_client(client_id)
        self.stack.setCurrentWidget(self.client_details_screen)
        
    def show_delete_client_screen(self, client_id):
        self.delete_client_screen.load_client(client_id)
        self.stack.setCurrentWidget(self.delete_client_screen)

    def show_concluded_projects_screen(self):
        self.closed_projects_screen.load_clients()
        self.closed_projects_screen.load_projects()
        self.stack.setCurrentIndex(3)

    def show_add_project_screen(self):
        self.add_project_screen.load_clients()
        self.stack.setCurrentIndex(4)

    def show_project_details_screen(self, project_id):
        self.project_details_screen.load_project(project_id)
        self.stack.setCurrentWidget(self.project_details_screen)
        
    def show_delete_project_screen(self, project_id):
        self.delete_project_screen.load_project(project_id)
        self.stack.setCurrentWidget(self.delete_project_screen)

    def show_create_service_screen(self, project_id):
        self.create_service_screen.load_project(project_id)
        self.stack.setCurrentWidget(self.create_service_screen)

    def show_service_details_screen(self, service_id):
        self.service_details_screen.load_service(service_id)
        self.stack.setCurrentWidget(self.service_details_screen)

    def show_create_task_screen(self, service_id):
        self.create_task_screen.load_service(service_id)
        self.stack.setCurrentWidget(self.create_task_screen)

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

    def show_delete_task_screen(self, task_id):
        self.delete_task_screen.load_task(task_id)
        self.stack.setCurrentWidget(self.delete_task_screen)

    def show_delete_service_screen(self, service_id):
        self.delete_service_screen.load_service(service_id)
        self.stack.setCurrentWidget(self.delete_service_screen)
        
    def show_delete_template_screen(self, template_id):
        self.delete_template_screen.load_template(template_id)
        self.stack.setCurrentWidget(self.delete_template_screen)

    def show_template_list_screen(self):
        self.template_list_screen.load_templates()
        self.stack.setCurrentWidget(self.template_list_screen)

    def show_add_template_screen(self):
        self.stack.setCurrentWidget(self.add_template_screen)

    def show_template_details_screen(self, template_id):
        self.template_details_screen.load_template(template_id)
        self.stack.setCurrentWidget(self.template_details_screen)

    def show_create_template_service_screen(self, template_id):
        self.create_service_screen.load_project(template_id)
        self.stack.setCurrentWidget(self.create_service_screen)

    def show_create_project_from_template_screen(self, template_id):
        self.create_from_template_screen.load_template(template_id)
        self.stack.setCurrentWidget(self.create_from_template_screen)

    def show_add_template_service_screen(self, template_id):
        self.add_template_service_screen.load_template(template_id)
        self.stack.setCurrentWidget(self.add_template_service_screen)
