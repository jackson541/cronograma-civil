from collections import defaultdict

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt

from project.models import Task, Service
from project.utils.funcs import compute_critical_path


class CreateTaskScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.service = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add New Task")
        layout = QVBoxLayout()

        self.service_label = QLabel("Service: ")
        layout.addWidget(self.service_label)

        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name")
        layout.addWidget(self.task_name_input)

        self.days_input = QLineEdit()
        self.days_input.setPlaceholderText("Days to complete")
        layout.addWidget(self.days_input)

        layout.addWidget(QLabel("Depends on (select tasks):"))
        self.dependencies_list = QListWidget()
        self.dependencies_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.dependencies_list)

        self.save_button = QPushButton("Save Task")
        self.save_button.clicked.connect(self.save_task)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("← Back to Service Details")
        self.back_button.clicked.connect(self.back_to_service_details)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_service(self, service_id):
        self.service = self.session.query(Service).get(service_id)
        if self.service:
            self.service_label.setText(f"Service: {self.service.name}")
            self.task_name_input.clear()
            self.days_input.clear()
            self.populate_dependencies()

    def populate_dependencies(self):
        self.dependencies_list.clear()
        for task in self.service.tasks:
            item = QListWidgetItem(task.name)
            item.setData(Qt.UserRole, task.id)
            item.setCheckState(Qt.Unchecked)
            self.dependencies_list.addItem(item)

    def save_task(self):
        name = self.task_name_input.text().strip()
        days_text = self.days_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Task name cannot be empty.")
            return
        
        if not days_text.isdigit() or int(days_text) <= 0:
            QMessageBox.warning(self, "Validation Error", "Days to complete must be a positive number.")
            return
        
        # Use a temporary ID (not committed yet), could be any unused ID
        temp_id = -999
        selected_deps = [item.data(Qt.UserRole) for item in self.dependencies_list.selectedItems()]

        if self.dependencies_list.count() > 0 and self.would_create_cycle(temp_id, selected_deps, self.session):
            QMessageBox.warning(self, "Ciclo detectado", "Não é possível criar depedências cíclicas.")
            return

        days_to_complete = int(days_text)

        new_task = Task(
            name=name,
            days_to_complete=days_to_complete,
            service_id=self.service.id
        )

        for i in range(self.dependencies_list.count()):
            item = self.dependencies_list.item(i)
            if item.checkState() == Qt.Checked:
                dep_id = item.data(Qt.UserRole)
                dep_task = self.session.query(Task).get(dep_id)
                new_task.dependencies.append(dep_task)

        self.session.add(new_task)
        self.session.commit()

        path, levels, dist = compute_critical_path(self.service.tasks)        

        self.service.days_to_complete = dist
        self.service.chart_data = {
            "path": path,
            "levels": levels,
        }
        self.session.commit()

        path, levels, dist = compute_critical_path(self.service.project.services)        

        self.service.project.days_to_complete = dist
        self.service.project.chart_data = {
            "path": path,
            "levels": levels,
        }

        self.session.commit()

        QMessageBox.information(self, "Success", "Task added successfully!")
        self.main_window.show_service_details_screen(self.service.id)

    def would_create_cycle(self, new_task_id, dependencies, session):
        graph = defaultdict(list)
        visited = set()
        rec_stack = set()

        # Build graph from current tasks
        all_tasks = session.query(Task).all()
        for task in all_tasks:
            for dep in task.dependencies:
                graph[dep.id].append(task.id)

        # Add the new simulated dependency
        for dep in dependencies:
            graph[dep.id].append(new_task_id)

        # Standard cycle detection using DFS
        def has_cycle(v):
            visited.add(v)
            rec_stack.add(v)
            for neighbor in graph[v]:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(v)
            return False

        return has_cycle(new_task_id)


    def back_to_service_details(self):
        if self.service:
            self.main_window.show_service_details_screen(self.service.id)
