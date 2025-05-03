from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

from project.models import Client, Project


class DeleteClientScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.client = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Excluir Cliente")
        layout = QVBoxLayout()

        # Title at the top with larger font
        self.title_label = QLabel("EXCLUIR CLIENTE")
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: red;")
        layout.addWidget(self.title_label)

        self.name_label = QLabel()
        layout.addWidget(self.name_label)

        self.question_label = QLabel("Tem certeza de que deseja excluir este cliente?")
        layout.addWidget(self.question_label)
        
        self.warning_label = QLabel("ATENÇÃO: Todas as informações associadas a este cliente serão perdidas!")
        self.warning_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.warning_label)
        
        # List of client's projects to be deleted
        self.projects_label = QLabel("Os seguintes projetos serão excluídos:")
        layout.addWidget(self.projects_label)
        
        self.projects_list = QListWidget()
        layout.addWidget(self.projects_list)

        # Action buttons
        self.delete_button = QPushButton("Excluir Cliente")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_client)
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_client)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_client(self, client_id):
        self.client = self.session.query(Client).get(client_id)
        if not self.client:
            QMessageBox.critical(self, "Erro", "Cliente não encontrado.")
            self.main_window.show_list_client_screen()
            return
        
        self.setWindowTitle(f"Excluir Cliente: {self.client.name}")
        self.name_label.setText(f"Nome: {self.client.name}")
        
        # Load client's projects to show what will be deleted
        self.load_projects()
    
    def load_projects(self):
        if not self.client:
            return
            
        self.projects_list.clear()
        if not self.client.projects:
            self.projects_label.setText("Este cliente não possui projetos.")
            return
            
        self.projects_label.setText(f"Os seguintes projetos de {self.client.name} serão excluídos:")
        for project in self.client.projects:
            status = "Concluído" if project.concluded else "Em andamento"
            item = QListWidgetItem(f"{project.name} - {status}")
            item.setData(Qt.UserRole, project.id)
            self.projects_list.addItem(item)

    def delete_client(self):
        if not self.client:
            self.main_window.show_list_client_screen()
            return
        
        # Check if client has projects
        if self.client.projects:
            # Delete all associated projects and their related items
            for project in self.client.projects:
                # Delete services and tasks
                for service in project.services:
                    # Delete tasks
                    for task in service.tasks:
                        self.session.delete(task)
                    # Delete service
                    self.session.delete(service)
                # Delete project
                self.session.delete(project)
        
        # Delete the client
        self.session.delete(self.client)
        self.session.commit()
        
        QMessageBox.information(self, "Concluído", "Cliente excluído com sucesso.")
        self.main_window.show_list_client_screen()

    def back_to_client(self):
        if self.client:
            self.main_window.show_client_details_screen(self.client.id)
        else:
            self.main_window.show_list_client_screen() 