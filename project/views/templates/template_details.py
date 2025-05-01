from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene,
    QPushButton, QListWidgetItem, QMessageBox
)

from PyQt5.QtCore import Qt

from project.models import ProjectTemplate
from project.utils.funcs import generate_graph

class TemplateDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.template = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.template_name_label = QLabel("Template Name: ")
        layout.addWidget(self.template_name_label)

        self.max_days = QLabel()
        layout.addWidget(self.max_days)

        # Graphical representation of services
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.add_service_button = QPushButton("Add Service")
        self.add_service_button.clicked.connect(self.go_to_add_service)
        layout.addWidget(self.add_service_button)

        self.create_project_button = QPushButton("Create Project from Template")
        self.create_project_button.clicked.connect(self.create_project_from_template)
        layout.addWidget(self.create_project_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.main_window.show_template_list_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_template(self, template_id):
        self.template = self.session.query(ProjectTemplate).get(template_id)
        if not self.template:
            self.template_name_label.setText("Template not found.")
            return
        
        self.setWindowTitle(self.template.name)

        self.template_name_label.setText(f"Template Name: {self.template.name}")
        self.max_days.setText(f"Critical path days: {self.template.days_to_complete}")

        self.scene.clear()
        if self.template.services:
            generate_graph(
                self.scene, 
                self.template.services, 
                self.main_window.show_service_details_screen, 
                self.template.chart_data
            )

    def go_to_add_service(self):
        if self.template:
            self.main_window.show_add_template_service_screen(self.template.id)

    def create_project_from_template(self):
        if not self.template:
            return
            
        self.main_window.show_create_project_from_template_screen(self.template.id) 