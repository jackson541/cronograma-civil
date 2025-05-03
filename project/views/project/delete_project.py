from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox

from project.models import Project, Service, Task


class DeleteProjectScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.project = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Excluir Projeto")
        layout = QVBoxLayout()

        # Title at the top with larger font
        self.title_label = QLabel("EXCLUIR PROJETO")
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: red;")
        layout.addWidget(self.title_label)

        self.name_label = QLabel()
        self.client_label = QLabel()
        self.question_label = QLabel("Tem certeza de que deseja excluir esse projeto?")
        self.warning_label = QLabel("Isto excluirá todos os serviços e tarefas associados ao projeto.")
        self.warning_label.setStyleSheet("color: red;")

        self.delete_button = QPushButton("Excluir Projeto")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_project)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_project_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.client_label)
        layout.addWidget(self.question_label)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_project(self, project_id):
        self.project = self.session.query(Project).get(project_id)
        if not self.project:
            QMessageBox.critical(self, "Erro", "Projeto não encontrado.")
            self.main_window.show_project_screen()
            return
        
        self.setWindowTitle(f"Excluir Projeto: {self.project.name}")
        self.name_label.setText(f"Nome: {self.project.name}")
        self.client_label.setText(f"Cliente: {self.project.client.name}")

    def delete_project(self):
        if not self.project:
            self.main_window.show_project_screen()
            return
            
        # Delete all related services and tasks
        for service in self.project.services:
            # Delete all tasks associated with this service
            for task in service.tasks:
                self.session.delete(task)
            # Delete the service itself
            self.session.delete(service)
            
        # Delete the project
        self.session.delete(self.project)
        self.session.commit()
        
        QMessageBox.information(self, "Concluído", "Projeto excluído com sucesso.")
        self.main_window.show_project_screen()

    def back_to_project_details(self):
        if self.project:
            self.main_window.show_project_details_screen(self.project.id)
        else:
            self.main_window.show_project_screen() 