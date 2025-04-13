from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QListWidgetItem
)
from PyQt5.QtCore import Qt


from project.models import Project


class ProjectDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.project = None  # Set this before showing
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.project_name_label = QLabel("Project Name: ")
        layout.addWidget(self.project_name_label)

        self.project_status_label = QLabel("Status: ")
        layout.addWidget(self.project_status_label)

        layout.addWidget(QLabel("Services:"))
        self.services_list = QListWidget()
        self.services_list.itemClicked.connect(self.view_service_details)
        layout.addWidget(self.services_list)

        self.add_service_button = QPushButton("Adicionar serviço")
        self.add_service_button.clicked.connect(self.go_to_add_service)
        layout.addWidget(self.add_service_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_project_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_project(self, project_id):
        self.project = self.session.query(Project).get(project_id)
        if not self.project:
            self.project_name_label.setText("Project not found.")
            return
        
        self.setWindowTitle(self.project.name)

        self.project_name_label.setText(f"Project Name: {self.project.name}")
        status = "Concluded" if self.project.concluded else "In Progress"
        self.project_status_label.setText(f"Status: {status}")

        self.services_list.clear()
        for service in self.project.services:
            item = QListWidgetItem(service.name)
            item.setData(Qt.UserRole, service.id)
            self.services_list.addItem(item)

    def view_service_details(self, item):
        service_id = item.data(Qt.UserRole)
        self.main_window.show_service_details_screen(service_id)

    def go_to_add_service(self):
        if self.project:
            self.main_window.show_create_service_screen(self.project.id)

