from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene,
    QPushButton, QListWidgetItem
)

from PyQt5.QtCore import Qt

from project.models import Project
from project.utils.funcs import generate_graph


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

        self.max_days = QLabel()
        layout.addWidget(self.max_days)

        self.edit_project_button = QPushButton("Editar")
        self.edit_project_button.clicked.connect(self.go_to_edit_project)
        layout.addWidget(self.edit_project_button)

        # Graphical representation of tasks
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

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

        self.max_days.setText(f"Caminho crítico dias: {self.project.days_to_complete}")

        self.scene.clear()
        if self.project.services:
            generate_graph(
                self.scene, 
                self.project.services, 
                self.main_window.show_service_details_screen, 
                self.project.chart_data
            )

    def go_to_add_service(self):
        if self.project:
            self.main_window.show_create_service_screen(self.project.id)

    def go_to_edit_project(self):
        if self.project:
            self.main_window.show_edit_project_screen(self.project.id)

