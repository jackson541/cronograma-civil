from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox

from project.models import Task


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

        self.save_button = QPushButton("Salvar alteração")
        self.save_button.clicked.connect(self.save_task)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_service_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.days_label)
        layout.addWidget(self.days_input)
        layout.addWidget(self.save_button)
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
        
        self.task.name = name
        self.task.days_to_complete = int(days)

        self.session.commit()
        QMessageBox.information(self, "Salvo", "Tarefa atualizada.")
        self.back_to_service_details()

    def back_to_service_details(self):
        if self.task:
            self.main_window.show_service_details_screen(self.task.service.id)
