from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QComboBox, QMessageBox
)

from project.models import Project, ProjectTemplate, Client, Service, Task
from project.utils.funcs import compute_critical_path

class CreateFromTemplateScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.template = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Criar Projeto a partir do Modelo")
        layout = QVBoxLayout()

        # Project Name
        layout.addWidget(QLabel("Nome do Projeto:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Client Dropdown
        layout.addWidget(QLabel("Cliente:"))
        self.client_dropdown = QComboBox()
        layout.addWidget(self.client_dropdown)

        # Buttons
        self.save_button = QPushButton("Criar Projeto")
        self.save_button.clicked.connect(self.create_project)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_template_details)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_template(self, template_id):
        self.template = self.session.query(ProjectTemplate).get(template_id)
        if not self.template:
            QMessageBox.critical(self, "Erro", "Modelo não encontrado.")
            self.close()
            return
        self.load_clients()

    def load_clients(self):
        self.client_dropdown.clear()
        clients = self.session.query(Client).all()
        for client in clients:
            self.client_dropdown.addItem(client.name, client.id)

    def create_project(self):
        if not self.template:
            return

        name = self.name_input.text().strip()
        client_id = self.client_dropdown.currentData()

        if not name:
            QMessageBox.warning(self, "Erro de Validação", "O nome do projeto não pode estar vazio.")
            return

        # Create the project
        project = Project(
            name=name,
            client_id=client_id,
            template_id=self.template.id,
        )
        self.session.add(project)
        self.session.commit()  

        # Bulk create all services first
        services_to_create = []
        for template_service in self.template.services:
            service = Service(
                name=template_service.name,
                project_id=project.id,
                days_to_complete=template_service.days_to_complete,
                chart_data=template_service.chart_data
            )
            services_to_create.append(service)

        self.session.bulk_save_objects(services_to_create)
        self.session.commit()

        # Bulk create all tasks
        tasks_to_create = []
        new_services = list(self.session.query(Service).filter(Service.project_id == project.id).all())
        for template_service in self.template.services:
            new_service = list(filter(lambda x: x.name == template_service.name, new_services))[0]
            for template_task in template_service.tasks:
                task = Task(
                    name=template_task.name,
                    days_to_complete=template_task.days_to_complete,
                    service_id=new_service.id
                )
                tasks_to_create.append(task)

        self.session.bulk_save_objects(tasks_to_create)
        self.session.commit()

        # Set up service dependencies
        for template_service in self.template.services:
            new_service = list(filter(lambda x: x.name == template_service.name, new_services))[0]
            for dep in template_service.dependencies:
                dep_service = list(filter(lambda x: x.name == dep.name, new_services))[0]
                new_service.dependencies.append(dep_service)

        # Set up task dependencies 
        for template_service in self.template.services:
            new_service = list(filter(lambda x: x.name == template_service.name, new_services))[0]
            new_tasks = list(self.session.query(Task).filter(Task.service_id == new_service.id).all())
            for template_task in template_service.tasks:
                new_task = list(filter(lambda x: x.name == template_task.name, new_tasks))[0]
                for dep in template_task.dependencies:
                    dep_task = list(filter(lambda x: x.name == dep.name, new_tasks))[0]
                    new_task.dependencies.append(dep_task)

        self.session.commit()

        # calculate critical path for services
        if project.services:
            for service in project.services:
                if service.tasks:
                    path, levels, dist = compute_critical_path(service.tasks)
                    service.chart_data = {
                        "path": path,
                        "levels": levels,
                    }
                    service.days_to_complete = dist
        
            self.session.commit()

        # calculate critical path for project
        if project.services:
            path, levels, dist = compute_critical_path(project.services)
            project.chart_data = {
                "path": path,
                "levels": levels,
            }
            project.days_to_complete = dist
            self.session.commit()

        QMessageBox.information(self, "Sucesso", "Projeto criado com sucesso!")
        self.main_window.show_project_details_screen(project.id)

    def back_to_template_details(self):
        if self.template:
            self.main_window.show_template_details_screen(self.template.id) 