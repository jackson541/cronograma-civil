from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QListWidgetItem,
    QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt

from project.models import Project, Client


class NotConcludedProjectsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.selected_client_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Projetos em andamento:")
        layout.addWidget(self.label)
        
        # Add client filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por cliente:"))
        self.client_filter = QComboBox()
        self.client_filter.currentIndexChanged.connect(self.on_client_filter_changed)
        filter_layout.addWidget(self.client_filter)
        layout.addLayout(filter_layout)

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

        self.templates_button = QPushButton("Modelos de projeto")
        self.templates_button.clicked.connect(self.main_window.show_template_list_screen)
        layout.addWidget(self.templates_button)

        self.setLayout(layout)

    def load_clients(self):
        self.client_filter.clear()
        self.client_filter.addItem("Todos os clientes", None)
        clients = self.session.query(Client).all()
        for client in clients:
            self.client_filter.addItem(client.name, client.id)
            
    def on_client_filter_changed(self, index):
        self.selected_client_id = self.client_filter.itemData(index)
        self.load_projects()

    def load_projects(self):
        self.project_list.clear()
        query = self.session.query(Project).filter(Project.concluded == False)
        
        # Apply client filter if selected
        if self.selected_client_id is not None:
            query = query.filter(Project.client_id == self.selected_client_id)
            
        projects = query.all()
        for project in projects:
            item = QListWidgetItem(project.name)
            item.setData(Qt.UserRole, project.id)
            self.project_list.addItem(item)

    def view_project_details(self, item):
        project_id = item.data(Qt.UserRole)
        self.main_window.show_project_details_screen(project_id)



