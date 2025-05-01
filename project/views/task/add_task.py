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
        self.setWindowTitle("Adicionar Nova Tarefa")
        layout = QVBoxLayout()

        self.service_label = QLabel("Serviço: ")
        layout.addWidget(self.service_label)

        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Digite o nome da tarefa")
        layout.addWidget(self.task_name_input)

        self.days_input = QLineEdit()
        self.days_input.setPlaceholderText("Dias para completar")
        layout.addWidget(self.days_input)

        layout.addWidget(QLabel("Depende de (selecione as tarefas):"))
        self.dependencies_list = QListWidget()
        self.dependencies_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.dependencies_list)

        self.save_button = QPushButton("Salvar Tarefa")
        self.save_button.clicked.connect(self.save_task)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("← Voltar para Detalhes do Serviço")
        self.back_button.clicked.connect(self.back_to_service_details)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_service(self, service_id):
        self.service = self.session.query(Service).get(service_id)
        if self.service:
            self.service_label.setText(f"Serviço: {self.service.name}")
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
            QMessageBox.warning(self, "Erro de Validação", "O nome da tarefa não pode estar vazio.")
            return
        
        if not days_text.isdigit() or int(days_text) <= 0:
            QMessageBox.warning(self, "Erro de Validação", "Os dias para completar devem ser um número positivo.")
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

        if self.service.project:
            path, levels, dist = compute_critical_path(self.service.project.services)  
            self.service.project.days_to_complete = dist
            self.service.project.chart_data = {
                "path": path,
                "levels": levels,
            }      
        else:
            path, levels, dist = compute_critical_path(self.service.template.services)
            self.service.template.days_to_complete = dist
            self.service.template.chart_data = {
                "path": path,
                "levels": levels,
            }

        self.session.commit()

        QMessageBox.information(self, "Sucesso", "Tarefa adicionada com sucesso!")
        self.main_window.show_service_details_screen(self.service.id)

    def back_to_service_details(self):
        if self.service:
            self.main_window.show_service_details_screen(self.service.id)
