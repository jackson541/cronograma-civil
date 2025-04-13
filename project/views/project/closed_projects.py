from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt

from project.models import Project


class ConcludedProjectsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Projetos concluidos")
        layout = QVBoxLayout()

        self.label = QLabel("Projetos concluidos:")
        layout.addWidget(self.label)

        self.project_list = QListWidget()
        layout.addWidget(self.project_list)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_project_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.load_projects()

    def load_projects(self):
        self.project_list.clear()
        projects = self.session.query(Project).filter(Project.concluded == True).all()
        for project in projects:
            self.project_list.addItem(f"{project.name} (ID: {project.id})")

