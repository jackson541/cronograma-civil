from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QCheckBox

from project.models import Service
from project.utils.funcs import compute_critical_path


class DeleteServiceScreen(QWidget):
    def __init__(self, session, main_window):
        super().__init__()
        self.session = session
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel()
        self.question_label = QLabel("Tem certeza de que deseja excluir esse serviço?")

        self.delete_button = QPushButton("Apagar serviço")
        self.delete_button.setStyleSheet("background-color: red; color: white;")
        self.delete_button.clicked.connect(self.delete_service)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.back_to_project_details)

        layout.addWidget(self.name_label)
        layout.addWidget(self.question_label)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_service(self, service_id):
        self.service_id = service_id
        self.service = self.session.query(Service).get(service_id)
        if not self.service:
            QMessageBox.critical(self, "Error", "service not found.")
            self.close()
            return
        
        self.name_label.setText(f"Nome: {self.service.name}")

    def delete_service(self):
        self.session.delete(self.service)
        for task in self.service.tasks:
            self.session.delete(task)
        self.session.commit()

        path, levels, dist = compute_critical_path(self.service.project.services)        

        self.service.project.days_to_complete = dist
        self.service.project.chart_data = {
            "path": path,
            "levels": levels,
        }
        self.session.commit()
        
        QMessageBox.information(self, "Removido", "Serviço apagado.")
        self.back_to_project_details()

    def back_to_project_details(self):
        if self.service:
            self.main_window.show_project_details_screen(self.service.project.id)

