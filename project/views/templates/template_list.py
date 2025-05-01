from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QLabel, 
    QPushButton, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt

from project.models import ProjectTemplate

class TemplateListScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Modelos de Projeto")
        layout = QVBoxLayout()

        self.label = QLabel("Modelos de Projeto:")
        layout.addWidget(self.label)

        self.template_list = QListWidget()
        self.template_list.itemClicked.connect(self.view_template_details)
        layout.addWidget(self.template_list)

        self.add_template_button = QPushButton("Adicionar Modelo")
        self.add_template_button.clicked.connect(self.main_window.show_add_template_screen)
        layout.addWidget(self.add_template_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.main_window.show_project_screen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.load_templates()

    def load_templates(self):
        self.template_list.clear()
        templates = self.session.query(ProjectTemplate).all()
        for template in templates:
            item = QListWidgetItem(template.name)
            item.setData(Qt.UserRole, template.id)
            self.template_list.addItem(item)

    def view_template_details(self, item):
        template_id = item.data(Qt.UserRole)
        self.main_window.show_template_details_screen(template_id) 