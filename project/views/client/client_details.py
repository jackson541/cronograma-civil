from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt

from project.models import Client, Project


class ClientDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.client = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Detalhes do Cliente")
        layout = QVBoxLayout()

        # Client information
        self.client_name_label = QLabel("Cliente: ")
        layout.addWidget(self.client_name_label)
        
        # Projects list
        self.projects_label = QLabel("Projetos deste cliente:")
        layout.addWidget(self.projects_label)
        
        self.projects_list = QListWidget()
        self.projects_list.itemClicked.connect(self.view_project_details)
        layout.addWidget(self.projects_list)
        
        # Action buttons
        self.edit_button = QPushButton("Editar Cliente")
        self.edit_button.clicked.connect(self.edit_client)
        layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Excluir Cliente")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_client)
        layout.addWidget(self.delete_button)
        
        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_list_client_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_client(self, client_id):
        self.client = self.session.query(Client).get(client_id)
        if not self.client:
            self.client_name_label.setText("Cliente não encontrado.")
            return
        
        self.setWindowTitle(f"Cliente: {self.client.name}")
        self.client_name_label.setText(f"Nome: {self.client.name}")
        
        # Load client's projects
        self.load_projects()
    
    def load_projects(self):
        if not self.client:
            return
            
        self.projects_list.clear()
        if not self.client.projects:
            self.projects_label.setText("Este cliente não possui projetos.")
            return
            
        self.projects_label.setText(f"Projetos de {self.client.name}:")
        for project in self.client.projects:
            status = "Concluído" if project.concluded else "Em andamento"
            item = QListWidgetItem(f"{project.name} - {status}")
            item.setData(Qt.UserRole, project.id)
            self.projects_list.addItem(item)
    
    def view_project_details(self, item):
        project_id = item.data(Qt.UserRole)
        self.main_window.show_project_details_screen(project_id)
        
    def edit_client(self):
        if self.client:
            self.main_window.show_edit_client_screen(self.client.id)
            
    def delete_client(self):
        if self.client:
            self.main_window.show_delete_client_screen(self.client.id) 