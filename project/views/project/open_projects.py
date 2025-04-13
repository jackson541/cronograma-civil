from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QListWidgetItem
)
from PyQt5.QtCore import Qt

from project.models import Project


class NotConcludedProjectsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Projetos em andamento:")
        layout.addWidget(self.label)

        self.project_list = QListWidget()
        self.project_list.itemClicked.connect(self.view_project_details)
        layout.addWidget(self.project_list)

        # Add button to open ListClientScreen
        self.list_clients_button = QPushButton("Clientes")
        self.list_clients_button.clicked.connect(self.main_window.show_list_client_screen)
        layout.addWidget(self.list_clients_button)
        
        self.list_clients_button = QPushButton("Projetos concluidos")
        self.list_clients_button.clicked.connect(self.main_window.show_concluded_projects_screen)
        layout.addWidget(self.list_clients_button)

        self.list_clients_button = QPushButton("Adicionar projeto")
        self.list_clients_button.clicked.connect(self.main_window.show_add_project_screen)
        layout.addWidget(self.list_clients_button)

        self.setLayout(layout)
        self.load_projects()

    def load_projects(self):
        self.project_list.clear()
        projects = self.session.query(Project).filter(Project.concluded == False).all()
        for project in projects:
            item = QListWidgetItem(project.name)
            item.setData(Qt.UserRole, project.id)
            self.project_list.addItem(item)

    def view_project_details(self, item):
        project_id = item.data(Qt.UserRole)
        self.main_window.show_project_details_screen(project_id)



