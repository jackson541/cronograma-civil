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

        self.template_name_label = QLabel("Nome do Modelo: ")
        layout.addWidget(self.template_name_label)

        self.max_days = QLabel()
        layout.addWidget(self.max_days)

        # Graphical representation of services
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.add_service_button = QPushButton("Adicionar Serviço")
        self.add_service_button.clicked.connect(self.go_to_add_service)
        layout.addWidget(self.add_service_button)

        self.create_project_button = QPushButton("Criar Projeto a partir do Modelo")
        self.create_project_button.clicked.connect(self.create_project_from_template)
        layout.addWidget(self.create_project_button)

        self.delete_button = QPushButton("Excluir Modelo")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_template)
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_template_list_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_template(self, template_id):
        self.template = self.session.query(ProjectTemplate).get(template_id)
        if not self.template:
            self.template_name_label.setText("Modelo não encontrado.")
            return
        
        self.setWindowTitle(self.template.name)

        self.template_name_label.setText(f"Nome do Modelo: {self.template.name}")
        self.max_days.setText(f"Dias do caminho crítico: {self.template.days_to_complete}")

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
        
    def delete_template(self):
        if not self.template:
            return
        self.main_window.show_delete_template_screen(self.template.id) 