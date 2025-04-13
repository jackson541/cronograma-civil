from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

from project.models import Task

class TaskDetailsScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.task = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Task Details")
        layout = QVBoxLayout()

        self.task_name_label = QLabel("Task: ")
        layout.addWidget(self.task_name_label)

        self.service_label = QLabel("Service: ")
        layout.addWidget(self.service_label)

        self.project_label = QLabel("Project: ")
        layout.addWidget(self.project_label)

        self.days_label = QLabel("Days to complete: ")
        layout.addWidget(self.days_label)

        self.dependencies_label = QLabel()
        self.dependencies_label.setOpenExternalLinks(False)
        self.dependencies_label.linkActivated.connect(self.handle_link_click)
        layout.addWidget(QLabel("Depends on:"))
        layout.addWidget(self.dependencies_label)

        self.dependents_label = QLabel()
        self.dependents_label.setOpenExternalLinks(False)
        self.dependents_label.linkActivated.connect(self.handle_link_click)
        layout.addWidget(QLabel("Dependents:"))
        layout.addWidget(self.dependents_label)

        self.back_button = QPushButton("← Back to Service Details")
        self.back_button.clicked.connect(self.back_to_service)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_task(self, task_id):
        self.task = self.session.query(Task).get(task_id)
        if not self.task:
            self.task_name_label.setText("Task not found.")
            return

        self.task_name_label.setText(f"Task: {self.task.name}")
        self.service_label.setText(f"Service: {self.task.service.name}")
        self.project_label.setText(f"Project: {self.task.service.project.name}")
        self.days_label.setText(f"Days to complete: {self.task.days_to_complete}")

        # Dependencies
        if self.task.dependencies:
            dep_links = ", ".join(
                f"<a href='task:{dep.id}'>{dep.name}</a>" for dep in self.task.dependencies
            )
            self.dependencies_label.setText(dep_links)
        else:
            self.dependencies_label.setText("None")

        # Dependents
        if self.task.dependents:
            dep_on_links = ", ".join(
                f"<a href='task:{d.id}'>{d.name}</a>" for d in self.task.dependents
            )
            self.dependents_label.setText(dep_on_links)
        else:
            self.dependents_label.setText("None")

    def handle_link_click(self, link):
        if link.startswith("task:"):
            task_id = int(link.split(":")[1])
            self.main_window.show_task_details_screen(task_id)

    def back_to_service(self):
        if self.task:
            self.main_window.show_service_details_screen(self.task.service_id)
