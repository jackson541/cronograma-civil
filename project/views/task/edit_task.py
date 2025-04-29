from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

from project.models import Task
from project.utils.funcs import compute_critical_path


class EditTaskScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit("")

        self.days_label = QLabel("Dias para completar:")
        self.days_input = QLineEdit("")

        layout.addWidget(QLabel("Depends on (select tasks):"))
        self.dependencies_list = QListWidget()
        self.dependencies_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.dependencies_list)

        self.save_button = QPushButton("Salvar alteração")
        self.save_button.clicked.connect(self.save_task)

        self.delete_button = QPushButton("Apagar tarefa")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.go_to_delete_task)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_service_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.days_label)
        layout.addWidget(self.days_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_task(self, task_id):
        self.task_id = task_id
        self.task = self.session.query(Task).get(task_id)
        if not self.task:
            QMessageBox.critical(self, "Error", "task not found.")
            self.close()
            return
        
        self.name_input.setText(self.task.name)
        self.days_input.setText(str(self.task.days_to_complete))
        self.populate_dependencies()

    def populate_dependencies(self):
        self.dependencies_list.clear()
        for task in self.task.service.tasks:
            if task.id != self.task.id:  # Don't show the current task
                item = QListWidgetItem(task.name)
                item.setData(Qt.UserRole, task.id)
                item.setCheckState(Qt.Checked if task in self.task.dependencies else Qt.Unchecked)
                self.dependencies_list.addItem(item)

    def save_task(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "task name cannot be empty.")
            return
        
        days = self.days_input.text().strip()

        if not days:
            QMessageBox.warning(self, "Validation Error", "task days cannot be empty.")
            return
        
        if not days.isdigit() or int(days) <= 0:
            QMessageBox.warning(self, "Validation Error", "Days to complete must be a positive number.")
            return

        # Check for cycles in dependencies
        selected_items = []
        for i in range(self.dependencies_list.count()):
            item = self.dependencies_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_items.append(item.data(Qt.UserRole))

        if self.would_create_cycle(self.task.id, selected_items):
            QMessageBox.warning(self, "Ciclo detectado", "Não é possível criar depedências cíclicas.")
            return
        
        self.task.name = name
        self.task.days_to_complete = int(days)

        # Update dependencies
        self.task.dependencies.clear()
        for dep_id in selected_items:
            dep_task = self.session.query(Task).get(dep_id)
            self.task.dependencies.append(dep_task)

        self.session.commit()

        path, levels, dist = compute_critical_path(self.task.service.tasks)        

        self.task.service.days_to_complete = dist
        self.task.service.chart_data = {
            "path": path,
            "levels": levels,
        }
        self.session.commit()

        path, levels, dist = compute_critical_path(self.task.service.project.services)        

        self.task.service.project.days_to_complete = dist
        self.task.service.project.chart_data = {
            "path": path,
            "levels": levels,
        }
        self.session.commit()

        QMessageBox.information(self, "Salvo", "Tarefa atualizada.")
        self.back_to_service_details()

    def would_create_cycle(self, task_id, dependencies):
        from collections import defaultdict
        graph = defaultdict(list)
        
        # Build complete graph including all tasks and their dependencies
        all_tasks = self.task.service.tasks
        for task in all_tasks:
            if task.id != task_id:  # Skip the current task being edited
                for dep in task.dependencies:
                    graph[dep.id].append(task.id)
        
        # Add the new proposed dependencies
        for dep_id in dependencies:
            if dep_id == task_id:  # Self-dependency check
                return True
            graph[dep_id].append(task_id)
        
        # Cycle detection using DFS
        def has_cycle(start_node):
            visited = set()
            path = set()
            
            def dfs(node):
                if node in path:
                    return True
                if node in visited:
                    return False
                    
                visited.add(node)
                path.add(node)
                
                for neighbor in graph[node]:
                    if dfs(neighbor):
                        return True
                        
                path.remove(node)
                return False
            
            return dfs(start_node)
        
        # Check for cycles starting from each dependency
        for dep_id in dependencies:
            if has_cycle(dep_id):
                return True
        return False

    def back_to_service_details(self):
        if self.task:
            self.main_window.show_service_details_screen(self.task.service.id)

    def go_to_delete_task(self):
        if self.task:
            self.main_window.show_delete_task_screen(self.task.id)
