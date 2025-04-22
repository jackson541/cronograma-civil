from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox

from project.models import Task
from project.utils.funcs import compute_critical_path


class DeleteTaskScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel()
        self.question_label = QLabel("Tem certeza de que deseja excluir essa tarefa?")

        self.delete_button = QPushButton("Apagar tarefa")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_task)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_service_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.question_label)
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
        
        self.name_label.setText(f"Nome: {self.task.name}")

    def delete_task(self):
        self.session.delete(self.task)
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

        QMessageBox.information(self, "Removido", "Tarefa apagada.")
        self.back_to_service_details()

    def back_to_service_details(self):
        if self.task:
            self.main_window.show_service_details_screen(self.task.service.id)
