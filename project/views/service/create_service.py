from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt

from project.models import Project, Service
from project.utils.funcs import compute_critical_path


class CreateServiceScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.project = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add New Service")
        layout = QVBoxLayout()

        self.project_label = QLabel("Projeto: ")
        layout.addWidget(self.project_label)

        self.service_name_input = QLineEdit()
        self.service_name_input.setPlaceholderText("Nome do serviço")
        layout.addWidget(self.service_name_input)

        layout.addWidget(QLabel("Serviços anteriores:"))
        self.dependencies_list = QListWidget()
        self.dependencies_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.dependencies_list)

        self.save_button = QPushButton("Adicionar")
        self.save_button.clicked.connect(self.save_service)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_project_details)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_project(self, project_id):
        self.project = self.session.query(Project).get(project_id)
        if self.project:
            self.project_label.setText(f"Projeto: {self.project.name}")
            self.service_name_input.clear()
            self.populate_dependencies()

    def populate_dependencies(self):
        self.dependencies_list.clear()
        for service in self.project.services:
            item = QListWidgetItem(service.name)
            item.setData(Qt.UserRole, service.id)
            item.setCheckState(Qt.Unchecked)
            self.dependencies_list.addItem(item)

    def save_service(self):
        name = self.service_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Service name cannot be empty.")
            return

        new_service = Service(name=name, project_id=self.project.id)

        # Add selected dependencies
        for index in range(self.dependencies_list.count()):
            item = self.dependencies_list.item(index)
            if item.checkState() == Qt.Checked:
                dep_service_id = item.data(Qt.UserRole)
                dep_service = self.session.query(Service).get(dep_service_id)
                new_service.dependencies.append(dep_service)

        self.session.add(new_service)
        self.session.commit()

        path, levels, dist = compute_critical_path(self.project.services)        

        self.project.days_to_complete = dist
        self.project.chart_data = {
            "path": path,
            "levels": levels,
        }
        self.session.commit()

        QMessageBox.information(self, "Sucesso", "Serviço adicionado!")
        self.main_window.show_project_details_screen(self.project.id)

    def back_to_project_details(self):
        if self.project:
            self.main_window.show_project_details_screen(self.project.id)
