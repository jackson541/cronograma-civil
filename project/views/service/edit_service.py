from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

from project.models import Service
from project.utils.funcs import compute_critical_path


class EditServiceScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit("")

        layout.addWidget(QLabel("Depends on (select services):"))
        self.dependencies_list = QListWidget()
        self.dependencies_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.dependencies_list)

        self.save_button = QPushButton("Salvar alteração")
        self.save_button.clicked.connect(self.save_service)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_service_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_service(self, service_id):
        self.service_id = service_id
        self.service = self.session.query(Service).get(service_id)
        if not self.service:
            QMessageBox.critical(self, "Error", "service not found.")
            self.close()
            return
        
        self.name_input.setText(self.service.name)
        self.populate_dependencies()

    def populate_dependencies(self):
        self.dependencies_list.clear()
        for service in self.service.project.services:
            if service.id != self.service.id:  # Don't show the current service
                item = QListWidgetItem(service.name)
                item.setData(Qt.UserRole, service.id)
                item.setCheckState(Qt.Checked if service in self.service.dependencies else Qt.Unchecked)
                self.dependencies_list.addItem(item)

    def save_service(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "service name cannot be empty.")
            return

        # Check for cycles in dependencies
        selected_items = []
        for i in range(self.dependencies_list.count()):
            item = self.dependencies_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_items.append(item.data(Qt.UserRole))

        if self.would_create_cycle(self.service.id, selected_items):
            QMessageBox.warning(self, "Ciclo detectado", "Não é possível criar depedências cíclicas.")
            return
        
        self.service.name = name

        # Update dependencies
        self.service.dependencies.clear()
        for dep_id in selected_items:
            dep_service = self.session.query(Service).get(dep_id)
            self.service.dependencies.append(dep_service)

        self.session.commit()

        path, levels, dist = compute_critical_path(self.service.project.services)        

        self.service.project.days_to_complete = dist
        self.service.project.chart_data = {
            "path": path,
            "levels": levels,
        }
        self.session.commit()
        
        QMessageBox.information(self, "Salvo", "Serviço atualizado.")
        self.back_to_service_details()

    def would_create_cycle(self, service_id, dependencies):
        from collections import defaultdict
        graph = defaultdict(list)
        
        # Build complete graph including all services and their dependencies
        all_services = self.service.project.services
        for service in all_services:
            if service.id != service_id:  # Skip the current service being edited
                for dep in service.dependencies:
                    graph[dep.id].append(service.id)
        
        # Add the new proposed dependencies
        for dep_id in dependencies:
            if dep_id == service_id:  # Self-dependency check
                return True
            graph[dep_id].append(service_id)
        
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
        if self.service:
            self.main_window.show_service_details_screen(self.service.id)
