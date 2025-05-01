from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt

from project.models import ProjectTemplate, Service
from project.utils.funcs import compute_critical_path

class AddTemplateServiceScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.template = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Service to Template")
        layout = QVBoxLayout()

        self.template_label = QLabel("Template: ")
        layout.addWidget(self.template_label)

        self.service_name_input = QLineEdit()
        self.service_name_input.setPlaceholderText("Service name")
        layout.addWidget(self.service_name_input)

        layout.addWidget(QLabel("Dependencies (select services):"))
        self.dependencies_list = QListWidget()
        self.dependencies_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.dependencies_list)

        self.save_button = QPushButton("Add Service")
        self.save_button.clicked.connect(self.save_service)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_to_template_details)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_template(self, template_id):
        self.template = self.session.query(ProjectTemplate).get(template_id)
        if self.template:
            self.template_label.setText(f"Template: {self.template.name}")
            self.service_name_input.clear()
            self.populate_dependencies()

    def populate_dependencies(self):
        self.dependencies_list.clear()
        for service in self.template.services:
            item = QListWidgetItem(service.name)
            item.setData(Qt.UserRole, service.id)
            item.setCheckState(Qt.Unchecked)
            self.dependencies_list.addItem(item)

    def save_service(self):
        name = self.service_name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Service name cannot be empty.")
            return

        new_service = Service(
            name=name,
            template_id=self.template.id,
        )

        # Add selected dependencies
        for index in range(self.dependencies_list.count()):
            item = self.dependencies_list.item(index)
            if item.checkState() == Qt.Checked:
                dep_service_id = item.data(Qt.UserRole)
                dep_service = self.session.query(Service).get(dep_service_id)
                new_service.dependencies.append(dep_service)

        self.session.add(new_service)
        self.session.commit()

        # Update template's critical path
        path, levels, dist = compute_critical_path(self.template.services)
        self.template.days_to_complete = dist
        self.template.chart_data = {
            "path": path,
            "levels": levels,
        }
        self.session.commit()

        QMessageBox.information(self, "Success", "Service added successfully!")
        self.main_window.show_template_details_screen(self.template.id)

    def back_to_template_details(self):
        if self.template:
            self.main_window.show_template_details_screen(self.template.id) 